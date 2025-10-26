<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
 
    /**
     * @name login
     * 
     * Show a login page
     */
    public function index () {
        
        $data = [];
        $Authuser = auth()->user();
        // dd($Authuser);
         if( !is_null( $Authuser ) ){
           //  dd($Authuser);
                 return view('admin.dashboard', $data);
   
        }
        else{
           // dd('login');
            return view('admin.auth.login');
        }
    }
}
