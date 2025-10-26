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

class ProcessLargeCSVJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public $timeout = 7200; // 2 hours
    public $tries = 3;

    protected $key;
    protected $chunkSize = 10000; // rows per chunk

    public function __construct($key)
    {
        $this->key = $key;
    }

    public function handle()
    {
        Log::info("Starting CSV import: {$this->key}");

        $s3 = new S3Client([
            'version' => 'latest',
            'region'  => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key'    => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        $tmpFile = storage_path('app/tmp_' . uniqid() . '.csv');

        // -----------------------
        // 1️⃣ Stream download from S3 to disk
        // -----------------------
        try {
            $s3->getObject([
                'Bucket' => env('AWS_BUCKET'),
                'Key' => $this->key,
                'SaveAs' => $tmpFile
            ]);
        } catch (\Exception $e) {
            Log::error("S3 download failed: " . $e->getMessage());
            throw $e;
        }

        // -----------------------
        // 2️⃣ Process CSV in chunks
        // -----------------------
        try {
            $handle = fopen($tmpFile, 'r');
            if (!$handle) {
                throw new \Exception("Cannot open CSV file: {$tmpFile}");
            }

            // Read header row
            $header = fgetcsv($handle);

            $rows = [];
            $rowCount = 0;

            while (($data = fgetcsv($handle)) !== false) {
                $rows[] = $data;
                $rowCount++;

                // Insert in chunks
                if ($rowCount % $this->chunkSize === 0) {
                    $this->insertChunk($header, $rows);
                    $rows = [];
                }
            }

            // Insert remaining rows
            if (!empty($rows)) {
                $this->insertChunk($header, $rows);
            }

            fclose($handle);
            Log::info("CSV import completed successfully: {$this->key}");
        } catch (\Exception $e) {
            Log::error("CSV import failed: " . $e->getMessage());
            throw $e;
        } finally {
            if (file_exists($tmpFile)) {
                unlink($tmpFile); // clean up
            }
        }
    }

    /**
     * Insert a chunk of rows into the database
     */
    protected function insertChunk(array $header, array $rows)
    {
        $table = 'contacts'; // your table

        // Prepare rows as associative arrays
        $data = array_map(function($row) use ($header) {
            return array_combine($header, $row);
        }, $rows);

        // Bulk insert
        DB::table($table)->insert($data);

        Log::info("Inserted chunk of " . count($rows) . " rows");
    }
}
