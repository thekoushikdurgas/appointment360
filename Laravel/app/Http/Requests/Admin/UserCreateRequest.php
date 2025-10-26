<?php

namespace App\Http\Requests\Admin;

use App\Models\AdminUser;
use App\Rules\CheckMediaExist;
use Illuminate\Contracts\Validation\Validator;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\ValidationException;

class UserCreateRequest extends FormRequest {

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize() {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules() {

        $rules = [
            'name' => 'required',
            'email' => 'required|email',
            'password' => 'min:6|required_with:cpassword|same:cpassword',
            'cpassword' => 'min:6'
        ];
        return $rules;
    }

}
