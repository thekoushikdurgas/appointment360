<?php

use Illuminate\Support\Facades\Route;
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
 Route::get('/clear-cache', function() {
        Artisan::call('config:clear');
        Artisan::call('cache:clear');
        return "Cache is cleared";
    });
Route::post('select2/meta-keywords', '\App\Http\Controllers\HelperController@select2MetaKeywords')->name('select2.meta_keywords');
Route::post('select2/category', '\App\Http\Controllers\HelperController@select2Category')->name('select2.category');

Route::post('upload-media', 'UploadController@uploadMedia')->name('admin.upload_media');

Route::group(['middleware' => 'unauth'], function () {
    Route::get('login', 'LoginController@login')->name('admin.login');
    Route::post('login', 'LoginController@doLogin')->name('admin.post_login');
    Route::get('forgot-password', 'LoginController@forgotPassword')->name('admin.forgot_password');
    Route::post('forgot-password', 'LoginController@sendResetPasswordLink')->name('admin.post_forgot_password');
    Route::get('reset-password/{token}', 'LoginController@showResetPassword')->name('admin.show_reset_password');
    Route::post('reset-password', 'LoginController@resetPassword')->name('admin.post_reset_passeword');
});

Route::group(['middleware' => 'auth:admin'], function () {

    Route::redirect('/', 'admin/dashboard', 301)->name('admin.index')->middleware('blockIP');

    Route::get('logout', 'LoginController@logout')->name('admin.logout');
    Route::get('dashboard', 'DashboardController@index')->name('admin.dashboard')->middleware('blockIP');

    //Admin Profile
    Route::prefix('admin')->group(function() {
        $adminController = '\App\Http\Controllers\Admin\AdminController@';
        Route::get('user-list', $adminController . 'listUsers')->name('user_list')->middleware('blockIP');
        Route::get('create', $adminController . 'createUser')->name('admin.user.create')->middleware('blockIP');
        Route::post('store', $adminController . 'store')->name('admin.user.post_data');
        Route::get('{user}/edit', $adminController . 'edit')->name('admin.user.edit');
        Route::get('{user}/column', $adminController . 'column')->name('admin.user.column');
        Route::post('store-column', $adminController . 'column_store')->name('admin.user.column_post_data');

        Route::post('{user}/change-status', $adminController . 'changeStatus')->name('admin.change_status');
    });
    Route::prefix('profile')->group(function() {

        $profileController = 'ProfileController@';

        Route::get('/', $profileController . 'index')->name('admin.profile')->middleware('blockIP');
        Route::post('store', $profileController . 'store')->name('admin.profile.post_data');
        Route::get('change-password', $profileController . 'changePassword')->name('admin.profile.change_password')->middleware('blockIP');
        Route::post('change-password/update', $profileController . 'updatePassword')->name('admin.profile.change_password.post_data');
    });

    //Parcel Type Route
    Route::prefix('parcel-type')->group(function() {

        $parcelTypeController = 'ParcelTypeController@';

        Route::get('/', $parcelTypeController . 'index')->name('admin.parcel_type');
        Route::post('ajax-data', $parcelTypeController . 'ajaxTableData')->name('admin.parcel_type.ajax_data');
        Route::get('create', $parcelTypeController . 'create')->name('admin.parcel_type.create');
        Route::get('{parcelType}/edit', $parcelTypeController . 'edit')->name('admin.parcel_type.edit');
        Route::post('store', $parcelTypeController . 'store')->name('admin.parcel_type.post_data');
        Route::post('{parcelType}/change-status', $parcelTypeController . 'changeStatus')->name('admin.parcel_type.change_status');
        Route::post('{parcelType}/delete', $parcelTypeController . 'delete')->name('admin.parcel_type.delete');
    });
    Route::prefix('contacts')->group(function() {

        $contactController = 'ContactsController@';

        Route::get('/', $contactController . 'index')->name('admin.contacts')->middleware('blockIP');
        Route::post('ajax-data', $contactController . 'ajaxTableData')->name('admin.contacts.ajax_data');
        Route::post('ajax-select', $contactController . 'ajaxData')->name('admin.contacts.ajax_select');
        Route::get('create', $contactController . 'create')->name('admin.contacts.create')->middleware('blockIP');
        Route::get('import_contacts', $contactController . 'import_contacts')->name('admin.contacts.import_contacts')->middleware('blockIP');
        Route::get('{contact}/edit', $contactController . 'edit')->name('admin.contacts.edit');
        Route::post('store', $contactController . 'store')->name('admin.contacts.post_data');
        Route::post('{contact}/delete', $contactController . 'delete')->name('admin.contacts.delete');
    });
	Route::post('/import-contacts','\App\Http\Controllers\Admin\ContactsController@importContacts')->name('contacts.import');
    Route::get('/contacts/import/progress', '\App\Http\Controllers\Admin\ContactsController@importProgress')->name('contacts.import.progress');
	Route::view('/upload-form', 'fileupload');
    Route::post('/upload-form/fileupload', '\App\Http\Controllers\Admin\ContactsController@upload')->name('uploadusers');
    Route::post('/search-form', '\App\Http\Controllers\Admin\ContactsController@search_form')->name('search-form');
    Route::post('/export', '\App\Http\Controllers\Admin\ContactsController@export_contact')->name('admin.contacts.export');
    Route::get('autocomplete', '\App\Http\Controllers\Admin\ContactsController@autocomplete')->name('autocomplete');
});
