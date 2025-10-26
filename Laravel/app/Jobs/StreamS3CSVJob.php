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

            rewind($tmpStream); // reset pointer for MySQL to read

            // Create a stream wrapper for LOAD DATA LOCAL INFILE
            stream_wrapper_register('csvstream', class_exists('CsvStreamWrapper', false) ? 'CsvStreamWrapper' : \App\Utils\CsvStreamWrapper::class);
            \App\Utils\CsvStreamWrapper::setStream($tmpStream);

            $table = 'contacts'; // target table

            // LOAD DATA LOCAL INFILE from the PHP stream
            $query = "
                LOAD DATA LOCAL INFILE 'csvstream://stream'
                INTO TABLE {$table}
                FIELDS TERMINATED BY ','
                ENCLOSED BY '\"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
            ";
            DB::connection()->getPdo()->exec($query);

            fclose($tmpStream);

            Log::info("LOAD DATA streaming import completed successfully: {$this->key}");
        } catch (\Exception $e) {
            Log::error("LOAD DATA streaming import failed: " . $e->getMessage());
            throw $e;
        }
    }
}
