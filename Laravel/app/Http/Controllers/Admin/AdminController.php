<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\UserCreateRequest;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use App\Models\AdminUser;
use Illuminate\Support\Facades\Hash;

class AdminController extends Controller {

    function listUsers() {
        $users = AdminUser::all();
        // dd($user);
        return view('admin.users.user_list', compact('users'));
    }

    function createUser(AdminUser $user) {
        $Authuser = auth()->user();
        return view('admin.users.create', compact('user', 'Authuser'));
    }

    /**
     * @name edit
     * 
     */
    public function edit(AdminUser $user) {
        return view('admin.users.create', compact('user'));
    }

    public function column(AdminUser $user) {
        $columns = \DB::getSchemaBuilder()->getColumnListing('contacts');

        unset($columns[0]);
        unset($columns[53]);
        unset($columns[54]);
        unset($columns[55]);
        return view('admin.users.column', compact('user', 'columns'));
    }

    /**
     * @name store
     * 
     */
    public function store(UserCreateRequest $request) {
        $messageKey = 'success-message';
        $message = '';
        if ($request->has('id')) {
            $user = AdminUser::find($request->get('id'));
            $message = 'User has been updated successfully.';
        } else {
            $user = new AdminUser;
            $user->created_by = auth()->id();

            $user->password = Hash::make($request->get('password'));
            $user->is_active = 1;
            $user->role = 2;
            $message = 'User has been created successfully.';
        }

        $user->name = $request->get('name');
        $user->email = $request->get('email');
        $user->download_limit = $request->get('download_limit');


        $user->save();
        return redirect()->back()->with($messageKey, $message);
    }

    function column_store(Request $request) {
        $messageKey = 'success-message';
        $message = '';
        if ($request->has('id')) {
            $user = AdminUser::find($request->get('id'));
            $message = 'User has been updated successfully.';
           
             $user->column_allowed = json_encode($request->get('column_allowed'));
        


        $user->save();
        return redirect()->back()->with($messageKey, $message);
        } 

       
    }

    /**
     * @name changeStatus
     * 
     * Change status of Parcel Type
     * 
     */
    public function changeStatus(AdminUser $user) {
        if ($user->is_active == 1) {
            $user->is_active = 2;
        } else {

            $user->is_active = 1;
        }
        $user->save();
        $data = [
            'message' => 'Success ! User status changed successfully.'
        ];
        return response()->json($data, 200);
    }

}
