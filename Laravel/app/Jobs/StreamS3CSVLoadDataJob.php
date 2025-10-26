<?php

namespace App\Jobs;

use Aws\S3\S3Client;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use App\Utils\CsvStreamWrapper;

class StreamS3CSVLoadDataJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $timeout = 7200; // 2 hours
    public $tries = 3;

    protected $key;

    public function __construct($key)
    {
        $this->key = $key;
    }

    public function handle()
    {
        Log::info("Starting LOAD DATA streaming import: {$this->key}");

        $s3 = new S3Client([
            'version' => 'latest',
            'region'  => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key'    => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        try {
            // Get the S3 object as a stream
            $result = $s3->getObject([
                'Bucket' => env('AWS_BUCKET'),
                'Key'    => $this->key,
            ]);

            $s3Stream = $result['Body']; // Guzzle stream

            // Create a temporary PHP stream for MySQL
            $tmpStream = fopen('php://temp', 'w+b');

            // Pipe the S3 stream into the PHP temp stream in chunks
            while (!$s3Stream->eof()) {
                fwrite($tmpStream, $s3Stream->read(1024 * 1024)); // 1MB chunks
            }

           rewind($tmpStream);

// ✅ Register custom wrapper only if not already registered
if (!in_array('csvstream', stream_get_wrappers())) {
    stream_wrapper_register('csvstream', CsvStreamWrapper::class);
}
CsvStreamWrapper::setStream($tmpStream);

            $table = 'contacts'; // target table

            // LOAD DATA LOCAL INFILE from the PHP stream
            $query = "
                LOAD DATA LOCAL INFILE 'csvstream://stream'
                INTO TABLE {$table}
                FIELDS TERMINATED BY ','
                ENCLOSED BY '\"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
				(first_name,last_name,title,company,company_name_for_emails,email,email_status,primary_email_catch_all_status,
                seniority,departments,work_direct_phone,home_phone,mobile_phone,corporate_phone,other_phone,stage,
                employees,industry,keywords,person_linkedin_url,website,company_linkedin_url,facebook_url,twitter_url,
                city,state,country,company_address,company_city,company_state,company_country,company_phone,
                technologies,annual_revenue,total_funding,latest_funding,latest_funding_amount,last_raised_at)
            ";
            DB::connection()->getPdo()->exec($query);
			$meta = stream_get_meta_data($tmpStream);
            fclose($tmpStream);
			// Optional cleanup if PHP stored it as a temp file on disk
			if (isset($meta['uri']) && file_exists($meta['uri']) && strpos($meta['uri'], '/tmp') === 0) {
				@unlink($meta['uri']);
			}

            Log::info("LOAD DATA streaming import completed successfully: {$this->key}");
        } catch (\Exception $e) {
            Log::error("LOAD DATA streaming import failed: " . $e->getMessage());
            throw $e;
        }
    }
}
