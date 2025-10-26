@extends('admin.layouts.app')

@section('title')
    {{ !empty( $contact->first_name ) ? $contact->first_name : 'Create Contact'}}
@endsection

@section('content')
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">{{ !empty( $contact->first_name ) ? $contact->first_name : 'Create Contact'}}</h1>

    </div>
    @include('component.error-message')
    
    <div class="row">
        
        <div class="col-lg-12">
            
            <form action="{{route('admin.contacts.post_data')}}" method="POST">
                @csrf
                @if( $contact->id )
                    <input type="hidden" name="id" value="{{ $contact->id }}">
                @endif
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="m-0 font-weight-bold text-primary">{{ !empty( $contact->id  ) ? 'Edit Parcel Type' :'Create Parcel Type'}}</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                                @foreach($columns  as $column)
                                 <div class="col-lg-6 form-group">
                                    <label>
                                       {{ucfirst(Str::replace('_', ' ', $column))}}
                                    </label>
                                    <input type="text" class="form-control {{$loop->index}}" name="{{$column}}" placeholder="Enter {{ucfirst(Str::replace('_', ' ', $column))}}" >
                                    @error($column)
                                        <div class="text-danger">{{$message}}</div>
                                    @enderror
                                </div>
                                @endforeach
                               
                        </div>
                    </div>
                    
                    <div class="card-footer">
                        <button type="submit" class="btn btn-primary">Submit</button>
                        <a href="{{ route('admin.contacts')}}" class="btn btn-danger">Cancel</a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

@endsection
@section('js-footer')
    
    <script src="{{url('assets/admin/js/parcel-type.js')}}"></script>
    
@endsection