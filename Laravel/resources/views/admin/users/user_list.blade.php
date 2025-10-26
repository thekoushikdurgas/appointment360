@extends('admin.layouts.app')

@section('title')
All Users
@endsection

@section('content')
<div class="container-fluid">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">Users</h1>
        <a href="{{route('admin.user.create')}}" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
            <i class="fas fa-plus fa-sm text-white-50"></i> Create New
        </a>
    </div>
    <div class="row">
        <div class="col-lg-12">
            <div class="card shadow mb-4">
                <div class="card-header py-3">
                    <h6 class="m-0 font-weight-bold text-primary">Users Lists</h6>
                </div>
                <div class="card-body">
                    <div class="table-responsive">

                        <table id="users_table" class="table table-bordered" width="100%" cellspacing="0">
                            <thead>
                                <tr role="row">
                                    <th>#</th>
                                    <th>Name</th>
                                    <th class="user_email">Email</th>
                                    <th class="download_limit">Download Limit</th>
                                    <th class="user_status">Status</th>
                                    <th class="user_action">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($users as $user)


                                <tr>
                                    <td>{{$loop->iteration}}</td>
                                    <td> {{$user->name}}</td>
                                    <td> {{$user->email}}</td>
                                    <td> {{$user->download_limit}}</td>
                                    <td> 
                                        @if ($user->is_active==1 || $user->is_active==2)
                                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                                            <input type="checkbox" class="custom-control-input user_status_switch" @if ($user->is_active==1) checked="checked"  @endif id="switch_{{$user->id}}" data-id="{{$user->id}}">
                                                   <label class="custom-control-label" for="switch_{{$user->id}}"></label>
                                        </div>
                                        @else
                                        Deleted
                                        @endif
                                    </td>
                                    <td> 
                                        <a href="{{route('admin.user.edit', [$user->id])}}" class="on-default edit-row"><i class="fa fa-edit"></i></a>
                                        <a href="{{route('admin.user.column', [$user->id])}}" class="on-default edit-row"><i class="fas fa-cog"></i></a>
                                    </td>
                                </tr>

                                @endforeach

                            </tbody>

                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

@endsection
@section('js-footer')
<script>

    $("#users_table").dataTable();

    $(document).on("click", ".user_status_switch", function (e) {
        
        var data = {
            message: "It will change the status of the selected user !",
            slug: 'admin',
            datatable_id: 'users_table'
        };

        confirmUserStatusChange(this, e, data);



    });
function statusUserChangeFn( data ){
    console.log(data);
    $.ajax({
        url : serverUrl + data.slug +"/" + data.id +"/change-status",
        type : "post",
        headers : {
            "X-CSRF-TOKEN" : requestToken
        },
        success:function ( res ) {
            
            toastr.success(res.message);
           location.reload(true);
         
        },
        error: function () {
            toastr.error("Error ! Please try again");
        },
        complete: function (){

        }
    })
}

function confirmUserStatusChange ( el, e, data ){
    e.preventDefault();
    var $this = $(el);
    var id = $this.data("id");
    data.id = id;
   
    Swal.fire({
        title: 'Are you sure?',
        text: data.message,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, change it!'
        }).then((result) => {
            
        if (result.value) {
            statusUserChangeFn( data );
        }
    })
}


</script>    
@endsection
