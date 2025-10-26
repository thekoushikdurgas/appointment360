@extends('admin.layouts.app')

@section('title')
{{ !empty( $user->name ) ? "Edit User": 'Create User'}}

@endsection

@section('content')
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">{{ !empty( $user->name ) ? 'Edit '.$user->name : 'Create User'}}</h1>

    </div>
    @include('component.error-message')

    <div class="row">

        <div class="col-lg-12">

            <form action="{{route('admin.user.post_data')}}" method="POST">
                @csrf
                @if( $user->id )
                <input type="hidden" name="id" value="{{ $user->id }}">
                @endif
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary">{{ !empty( $user->id  ) ? 'Edit User' :'Create User'}}</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-12">

                                <div class="form-group">
                                    <label>
                                        Name
                                    </label>
                                    <input type="text" class="form-control" name="name" placeholder="Enter Name" value="{{old('name', $user->name)}}">
                                    @error('name')
                                    <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>

                                <div class="form-group">
                                    <label>
                                        Email
                                    </label>
                                    <input type="text" class="form-control" name="email" placeholder="Enter Email" value="{{old('email', $user->email)}}">
                                    @error('email')
                                    <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>
                                <div class="form-group">
                                    <label>
                                        Downloads limit
                                    </label>
                                    <input type="number" class="form-control" name="download_limit" placeholder="Enter Download Limit" value="{{old('download_limit', $user->download_limit)}}">
                                    @error('download_limit')
                                    <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>
                                @if( !$user->id )
                                <div class="form-group">
                                    <label>
                                        Password
                                    </label>
                                    <input type="password" class="form-control" name="password" placeholder="Enter Password" value="{{old('password', $user->password)}}">
                                    @error('password')
                                    <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>
                                <div class="form-group">
                                    <label>
                                        Re Password 
                                    </label>
                                    <input type="password" class="form-control" name="cpassword" placeholder="Enter Confirm Password" value="{{old('cpassword', $user->password)}}">
                                    @error('cpassword')
                                    <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>
                                @endif

                            </div>
                        </div>
                    </div>

                    <div class="card-footer">
                        <button type="submit" class="btn btn-primary">Submit</button>
                        <a href="{{ route('user_list')}}" class="btn btn-danger">Cancel</a>
                    </div>
                </div>
            </form>
        </div>
        
    </div>
</div>

@endsection
@section('js-footer')


@endsection