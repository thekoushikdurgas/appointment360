<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Cache;
use Aws\S3\S3Client;
use Illuminate\Support\Str;
use App\Jobs\ProcessLargeCSVJob;

class CSVUploadController extends Controller
{
    public function form()
    {
		//echo phpinfo(); die;
        return view('csv_upload.upload-csv');
    }

    /**
     * Initialize chunked upload and return upload ID
     */
    public function initializeChunkedUpload(Request $request)
    {
        try {
            $request->validate([
                'fileName' => 'required|string',
                'fileSize' => 'required|integer',
                'totalChunks' => 'required|integer'
            ]);

            $uploadId = Str::uuid()->toString();
            $s3Key = 'uploads/' . $uploadId . '.csv';

            // S3 client
            $s3 = new S3Client([
                'version' => 'latest',
                'region'  => env('AWS_DEFAULT_REGION'),
                'credentials' => [
                    'key'    => env('AWS_ACCESS_KEY_ID'),
                    'secret' => env('AWS_SECRET_ACCESS_KEY'),
                ],
            ]);

            // Initialize multipart upload
            $result = $s3->createMultipartUpload([
                'Bucket' => env('AWS_BUCKET'),
                'Key'    => $s3Key,
                'ACL'    => 'private',
            ]);

            $multipartUploadId = $result['UploadId'];

            // Store upload metadata in cache
            Cache::put("upload_{$uploadId}", [
                's3Key' => $s3Key,
                'multipartUploadId' => $multipartUploadId,
                'totalChunks' => $request->totalChunks,
                'uploadedChunks' => [],
                'fileName' => $request->fileName,
                'fileSize' => $request->fileSize
            ], now()->addHours(6));

            return response()->json([
                'success' => true,
                'uploadId' => $uploadId,
                'message' => 'Upload initialized'
            ]);

        } catch (\Exception $e) {
            Log::error('Failed to initialize chunked upload: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Initialization failed: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Upload a single chunk
     */
    public function uploadChunk(Request $request)
    {
        try {
            $request->validate([
                'uploadId' => 'required|string',
                'chunkIndex' => 'required|integer',
                'chunk' => 'required|file'
            ]);

            $uploadId = $request->uploadId;
            $chunkIndex = $request->chunkIndex;
            $chunk = $request->file('chunk');

            // Get upload metadata from cache
            $uploadData = Cache::get("upload_{$uploadId}");
            if (!$uploadData) {
                return response()->json([
                    'success' => false,
                    'message' => 'Upload session expired or not found'
                ], 404);
            }

            // S3 client
            $s3 = new S3Client([
                'version' => 'latest',
                'region'  => env('AWS_DEFAULT_REGION'),
                'credentials' => [
                    'key'    => env('AWS_ACCESS_KEY_ID'),
                    'secret' => env('AWS_SECRET_ACCESS_KEY'),
                ],
            ]);

            // Upload chunk as a part
            $result = $s3->uploadPart([
                'Bucket' => env('AWS_BUCKET'),
                'Key' => $uploadData['s3Key'],
                'UploadId' => $uploadData['multipartUploadId'],
                'PartNumber' => $chunkIndex + 1, // S3 parts are 1-indexed
                'Body' => fopen($chunk->getRealPath(), 'r')
            ]);

            // Store the ETag for this part
            $uploadData['uploadedChunks'][$chunkIndex] = [
                'PartNumber' => $chunkIndex + 1,
                'ETag' => $result['ETag']
            ];

            // Update cache
            Cache::put("upload_{$uploadId}", $uploadData, now()->addHours(6));

            return response()->json([
                'success' => true,
                'message' => "Chunk {$chunkIndex} uploaded",
                'uploadedChunks' => count($uploadData['uploadedChunks'])
            ]);

        } catch (\Exception $e) {
            Log::error("Failed to upload chunk {$request->chunkIndex}: " . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Chunk upload failed: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Complete the multipart upload
     */
    public function completeChunkedUpload(Request $request)
    {
        try {
            $request->validate([
                'uploadId' => 'required|string'
            ]);

            $uploadId = $request->uploadId;

            // Get upload metadata from cache
            $uploadData = Cache::get("upload_{$uploadId}");
            if (!$uploadData) {
                return response()->json([
                    'success' => false,
                    'message' => 'Upload session expired or not found'
                ], 404);
            }

            // Verify all chunks uploaded
            if (count($uploadData['uploadedChunks']) !== $uploadData['totalChunks']) {
                return response()->json([
                    'success' => false,
                    'message' => 'Not all chunks uploaded'
                ], 400);
            }

            // S3 client
            $s3 = new S3Client([
                'version' => 'latest',
                'region'  => env('AWS_DEFAULT_REGION'),
                'credentials' => [
                    'key'    => env('AWS_ACCESS_KEY_ID'),
                    'secret' => env('AWS_SECRET_ACCESS_KEY'),
                ],
            ]);

            // Sort parts by PartNumber
            $parts = array_values($uploadData['uploadedChunks']);
            usort($parts, function($a, $b) {
                return $a['PartNumber'] - $b['PartNumber'];
            });

            // Complete the multipart upload
            $result = $s3->completeMultipartUpload([
                'Bucket' => env('AWS_BUCKET'),
                'Key' => $uploadData['s3Key'],
                'UploadId' => $uploadData['multipartUploadId'],
                'MultipartUpload' => [
                    'Parts' => $parts
                ]
            ]);

            // Dispatch background job to process the CSV
            ProcessLargeCSVJob::dispatch($uploadData['s3Key']);

            // Clean up cache
            Cache::forget("upload_{$uploadId}");

            Log::info("CSV upload completed: {$uploadData['s3Key']}");

            return response()->json([
                'success' => true,
                'message' => '✅ File uploaded successfully. Import job queued.',
                's3Key' => $uploadData['s3Key']
            ]);

        } catch (\Exception $e) {
            Log::error('Failed to complete chunked upload: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Upload completion failed: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Cancel chunked upload
     */
    public function cancelChunkedUpload(Request $request)
    {
        try {
            $uploadId = $request->uploadId;
            $uploadData = Cache::get("upload_{$uploadId}");

            if ($uploadData) {
                // S3 client
                $s3 = new S3Client([
                    'version' => 'latest',
                    'region'  => env('AWS_DEFAULT_REGION'),
                    'credentials' => [
                        'key'    => env('AWS_ACCESS_KEY_ID'),
                        'secret' => env('AWS_SECRET_ACCESS_KEY'),
                    ],
                ]);

                // Abort the multipart upload
                $s3->abortMultipartUpload([
                    'Bucket' => env('AWS_BUCKET'),
                    'Key' => $uploadData['s3Key'],
                    'UploadId' => $uploadData['multipartUploadId']
                ]);

                // Clean up cache
                Cache::forget("upload_{$uploadId}");
            }

            return response()->json([
                'success' => true,
                'message' => 'Upload cancelled'
            ]);

        } catch (\Exception $e) {
            Log::error('Failed to cancel upload: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Cancellation failed: ' . $e->getMessage()
            ], 500);
        }
    }

    // Legacy single upload method (keeping for backward compatibility)
    public function ajaxUpload(Request $request)
    {
          try {
            $request->validate([
                'csv_file' => 'required|mimes:csv,txt|max:512000' // 500 MB max
            ]);

            $file = $request->file('csv_file');
            $filename = 'uploads/' . Str::uuid() . '.csv';

            // S3 client
            $s3 = new S3Client([
                'version' => 'latest',
                'region'  => env('AWS_DEFAULT_REGION'),
                'credentials' => [
                    'key'    => env('AWS_ACCESS_KEY_ID'),
                    'secret' => env('AWS_SECRET_ACCESS_KEY'),
                ],
            ]);

            // Upload file to S3
            $s3->putObject([
                'Bucket' => env('AWS_BUCKET'),
                'Key'    => $filename,
                'SourceFile' => $file->getRealPath(),
                'ACL' => 'private',
            ]);

            // Dispatch background job
            ProcessLargeCSVJob::dispatch($filename);

            return response()->json([
                'success' => true,
                'message' => '✅ File uploaded successfully. Import job queued.'
            ]);

        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json([
                'success' => false,
                'message' => $e->validator->errors()->first()
            ], 422);
        } catch (\Exception $e) {
            \Log::error('CSV upload failed: '.$e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'Server error: '.$e->getMessage()
            ], 500);
        }
    }
}
