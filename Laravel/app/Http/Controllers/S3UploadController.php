<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Aws\S3\S3Client;
use Illuminate\Support\Str;
use App\Jobs\ProcessLargeCSVJob;
use App\Jobs\StreamS3CSVLoadDataJob;
class S3UploadController extends Controller
{
    public function upload2_csv()
    {
		//StreamS3CSVLoadDataJob::dispatch("uploads/1ff76589-5e91-4a19-b812-c4afb59f630e_3519363_2M.csv");
        return view('csv_upload.upload2');

    }

    // Generate pre-signed URL for small file
    public function getPresignedUploadUrl(Request $request)
    {
        $request->validate([
            'fileName' => 'required|string',
            'fileType' => 'required|string'
        ]);

        $s3 = new S3Client([
            'version' => 'latest',
            'region' => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key' => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        $s3Key = 'uploads/' . Str::uuid() . '_' . $request->fileName;

        $cmd = $s3->getCommand('PutObject', [
            'Bucket' => env('AWS_BUCKET'),
            'Key' => $s3Key,
            'ContentType' => $request->fileType,
        ]);

        $requestUrl = $s3->createPresignedRequest($cmd, '+15 minutes');

        return response()->json([
            'url' => (string) $requestUrl->getUri(),
            's3Key' => $s3Key
        ]);
    }

    // Generate pre-signed URLs for multipart upload
    public function getMultipartPresignedUrls(Request $request)
    {
        $request->validate([
            'fileName' => 'required|string',
            'fileSize' => 'required|integer',
            'chunkSize' => 'required|integer',
        ]);

        $s3 = new S3Client([
            'version' => 'latest',
            'region' => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key' => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        $s3Key = 'uploads/' . Str::uuid() . '_' . $request->fileName;

        // Initiate multipart upload
        $multipart = $s3->createMultipartUpload([
            'Bucket' => env('AWS_BUCKET'),
            'Key' => $s3Key,
            'ACL' => 'private',
        ]);

        $uploadId = $multipart['UploadId'];
        $totalChunks = ceil($request->fileSize / $request->chunkSize);

        $urls = [];
        for ($i = 1; $i <= $totalChunks; $i++) {
            $cmd = $s3->getCommand('UploadPart', [
                'Bucket' => env('AWS_BUCKET'),
                'Key' => $s3Key,
                'UploadId' => $uploadId,
                'PartNumber' => $i,
            ]);

            $presigned = $s3->createPresignedRequest($cmd, '+15 minutes');
            $urls[] = (string) $presigned->getUri();
        }

        return response()->json([
            's3Key' => $s3Key,
            'uploadId' => $uploadId,
            'urls' => $urls
        ]);
    }

    // Complete multipart upload after browser uploads all chunks
    public function completeMultipartUpload(Request $request)
    {
        $request->validate([
            's3Key' => 'required|string',
            'uploadId' => 'required|string',
            'parts' => 'required|array',
        ]);

        $s3 = new S3Client([
            'version' => 'latest',
            'region' => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key' => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        $s3->completeMultipartUpload([
            'Bucket' => env('AWS_BUCKET'),
            'Key' => $request->s3Key,
            'UploadId' => $request->uploadId,
            'MultipartUpload' => ['Parts' => $request->parts]
        ]);

        // Queue CSV processing
        StreamS3CSVLoadDataJob::dispatch($request->s3Key);

        return response()->json([
            'success' => true,
            'message' => 'Multipart upload completed and job queued'
        ]);
    }

    // Trigger CSV processing for small files
    public function processCSV(Request $request)
    {
        $request->validate(['s3Key' => 'required|string']);
        ProcessLargeCSVJob::dispatch($request->s3Key);
        return response()->json(['success' => true, 'message' => 'CSV job queued']);
    }
}
