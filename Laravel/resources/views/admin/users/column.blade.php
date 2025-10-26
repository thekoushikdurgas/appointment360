@extends('admin.layouts.app')

@section('title')
{{ !empty( $user->name ) ? "column": 'Create User'}}

@endsection

@section('content')
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Check Column for download</h1>

    </div>
    @include('component.error-message')

    <div class="row">

        <div class="col-lg-12">

            <form action="{{route('admin.user.column_post_data')}}" method="POST">
                @csrf
                @if( $user->id )
                <input type="hidden" name="id" value="{{ $user->id }}">
                @endif
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary">{{ !empty( $user->id  ) ? 'Check Column' :'Create User'}}</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
<?php

$columnData= $user->column_allowed;
$columanDataArray=json_decode($columnData);

?>
                            @foreach ($columns as $column)
                            <div class="col-lg-6">
                                <div class="custom-control custom-checkbox">
                                    <input id="checked-{{$column}}" name="column_allowed[]" class="custom-control-input" type="checkbox" <?php if(in_array($column,$columanDataArray)){echo"checked";} ?> value="{{$column}}" />
                                    <label for="checked-{{$column}}" class="custom-control-label">{{ucfirst(Str::replace('_', ' ', $column))}}</label>
                                </div>
                            </div>
                            @endforeach


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