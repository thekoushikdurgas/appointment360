<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\RazorpayPaymentController;
use App\Http\Controllers\CSVUploadController;
use App\Http\Controllers\S3UploadController;

use App\Http\Controllers\ContactController;


/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/
Route::get('storage/image/{width}/{height}/{image_path}', 'Admin\UploadController@readMedia')->where('image_path', '.*')->name('admin.media.fetch');
Route::get('media/image/{image_path}', 'Admin\UploadController@readOriginalMedia')->where('image_path', '.*')->name('admin.media.original');

Route::get('/', function () {
    return view('admin.dashboard');
});
Route::get('payment', [RazorpayPaymentController::class, 'index']);
Route::post('payment', [RazorpayPaymentController::class, 'store'])->name('razorpay.payment.store');
Route::get('/subscribe', 'SubscriptionController@showForm');
Route::post('/subscribe', 'SubscriptionController@subscribe');
Route::post('/callbacksubscriptions', 'SubscriptionController@callbacksubscriptions');

Route::get('/upload-csv', [CSVUploadController::class, 'form']);

// Chunked upload routes
Route::post('/csv-upload/init', [CSVUploadController::class, 'initializeChunkedUpload'])->name('csv.upload.init');
Route::post('/csv-upload/chunk', [CSVUploadController::class, 'uploadChunk'])->name('csv.upload.chunk');
Route::post('/csv-upload/complete', [CSVUploadController::class, 'completeChunkedUpload'])->name('csv.upload.complete');
Route::post('/csv-upload/cancel', [CSVUploadController::class, 'cancelChunkedUpload'])->name('csv.upload.cancel');

// Legacy single upload route (backward compatibility)
Route::post('/upload-csv', [CSVUploadController::class, 'ajaxUpload'])->name('upload.csv.ajax');

Route::post('/get-upload-url', [CSVUploadController::class, 'getUploadUrl']);
Route::post('/start-import-job', [CSVUploadController::class, 'startImportJob']);
Route::get('/check-job-status', [CSVUploadController::class, 'checkJobStatus']);
Route::post('/process-uploaded-csv', [CSVUploadController::class, 'processUploadedCSV']);



Route::get('/upload2-csv', [S3UploadController::class, 'upload2_csv']);



Route::get('/upload2-csv', [S3UploadController::class, 'upload2_csv'])->name('upload.upload2_csv');
Route::post('/upload/get-presigned-url', [S3UploadController::class, 'getPresignedUploadUrl'])->name('upload.getPresignedUploadUrl');
Route::post('/upload/process-csv', [S3UploadController::class, 'processCSV'])->name('upload.processCSV');

// New routes for multipart pre-signed upload
Route::post('/upload/get-multipart-presigned-urls', [S3UploadController::class, 'getMultipartPresignedUrls'])->name('upload.getMultipartPresignedUrls');
Route::post('/upload/complete-multipart-upload', [S3UploadController::class, 'completeMultipartUpload'])->name('upload.completeMultipartUpload');

Route::get('/contact', [ContactController::class, 'index'])->name('contact.index');
Route::get('/contact/data', [ContactController::class, 'fetchData'])->name('contact.data');
Route::get('/contacts/fetch', [ContactController::class, 'fetchContacts'])->name('contacts.fetch');
Route::get('/filter-options', [ContactController::class, 'filterOptions'])->name('filter.options');