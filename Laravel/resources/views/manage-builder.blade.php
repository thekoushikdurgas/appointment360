@extends('layouts.app')
@section('title', 'Add New Sells')
@section('content')
<style>
.switch {
  position: relative;
  display: inline-block;
  width: 83px;
  height: 28px;
}
.switch input {display:none;}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ca2222;
  -webkit-transition: .4s;
  transition: .4s;
   border-radius: 34px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width:22px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #2ab934;
}
input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}
input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(55px);
}
/*------ ADDED CSS ---------*/
.slider:after
{
 content:'OFF';
 color: white;
 display: block;
 position: absolute;
 transform: translate(-50%,-50%);
 top: 50%;
 left: 50%;
 font-size: 10px;
 font-family: Verdana, sans-serif;
}
input:checked + .slider:after
{  
  content:'ON';
}
</style>

    <!-- ============================================================== -->
    <!-- Start Page Content here -->
    <!-- ============================================================== -->

    <div class="content-page">
        <div class="content">
            <!-- Start Content-->
            <div class="container-fluid">
                <div class="row page-title">
                    <div class="col-md-12">
                        <nav aria-label="breadcrumb" class="float-right mt-1">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><a href="{{ route('dashboard') }}">Dashboard</a></li>
                                <li class="breadcrumb-item active" aria-current="page">Add Sells</li>
                            </ol>
                        </nav>
                        <h4 class="mb-1 mt-0">Add Team</h4>
                    </div>
                </div>

                <!-- end row -->
                <div class="row">
                    <div class="col-xl-12">
                        <div class="card">
                            <div class="card-body">

                                @if(Session::has('message'))
                                    <div class="alert alert-success alert-block">
                                        <button type="button" class="close" data-dismiss="alert">×</button>
                                        <strong>{!! session('message') !!}</strong>
                                    </div>
                                @endif

                                @if ($errors->any())
                                    <div class="alert alert-danger">
                                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                                        <ul>
                                            @foreach ($errors->all() as $error)
                                                <li>{{ $error }}</li>
                                            @endforeach
                                        </ul>
                                    </div>
                                @endif

                                <form action="{{route('save-sells')}}" method="post" name="save-admin" class="form-horizontal">
                                    @csrf

                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Name <span class="required">*</span></label>
                                        <div class="col-9">
                                            <input type="text" name="name" class="form-control" placeholder="Name" required>
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Email <span class="required">*</span></label>
                                        <div class="col-9">
                                            <input type="email" value="" name="email" class="form-control" placeholder="Email" required>
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Mobile <span class="required">*</span></label>
                                        <div class="col-9">
                                            <input type="text" name="phone_no" class="form-control" placeholder="Mobile" required>
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputPassword3" class="col-3 col-form-label">Password <span class="required">*</span></label>
                                        <div class="col-9">
                                            <input type="password" name="password" class="form-control" placeholder="Password" required>
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputPassword5" class="col-3 col-form-label">Re Password <span class="required">*</span></label>
                                        <div class="col-9">
                                            <input type="password" name="cpassword" class="form-control" placeholder="Retype Password" required>
                                        </div>
                                    </div>

                                    <div class="form-group mb-0 justify-content-end row">
                                        <div class="col-9">
                                            <button type="submit" class="btn btn-info">Submit</button>
                                            <a href="{{ route('manage-admins') }}"><button type="button" class="btn btn-success">Back</button></a>
                                        </div>
                                    </div>
                                </form>
                            </div>  <!-- end card-body -->
                        </div>  <!-- end card -->
						
						<div class="card">
						<div class="card-body">
						
							<?php
							
							if (count($staffList)>0) { ?>
                            <div class="table-responsive">
							<table id="idsssss" class="table dt-responsive">
								<thead>
									<tr>
										<!--<th>#</th>-->
										<th>Sl.no</th>
										<th>Name</th>
										<th>Mobile No</th>
										<th>Email</th>
										<th>Status</th>
										<th>Action</th>
                                        
									</tr>
								</thead>

								<tbody>
									<?php
									$i = 0;
									foreach($staffList as $key => $value) {
									//print_r($value); die;
									$i++;
									$status = "<span style='color:green'>Active</span>";
									if ($value->status == "2") {
										$status = "<span style='color:red'>IN Active</span>";
									}
									?>
										<tr>
											<td>{{$i}}</td>
											<td>{{$value->name}}</td>
											<td>{{$value->phone_no}}</td>
											
											<td>{{$value->email}}</td>
                      <td>
                      @if($value->status == 1)
                                <label class="switch" onchange="myActive({{$value->id}});">
                                <input type="hidden" name="status" id="active" value="2">
                                <input type="checkbox" checked>
                                <span class="slider round"></span>
                              </label>

                              @else
                              <label class="switch"  onclick="myStatus({{$value->id}});">
                                <input type="hidden" name="status" id="status" value="1">
                                <input type="checkbox" >
                                <span class="slider round"></span>
                              </label>
                          @endif
											<td>
											 <div class="icon-item">
                              <a href="{{ url('/edit-sells/'.$value->id) }}">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                              </a>
                              <a href="{{ url('/delete-sells/'.$value->id) }}" onclick="return deleteConfirm()">
                                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-delete"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>
                              </a>
                          
                          <td>
                             
                          </div>
											</td>
										</tr>
									<?php } ?>
								</tbody>
							</table>
							</td>
							<?php } else { ?>
						
							<table id="idsssss" class="table dt-responsive nowrap">
								<tr>
									<th colspan=4 style="text-align:center;"> No Record Found </th>
								</tr>
							</table>
						<?php } ?>

                                </div> <!-- end card body-->
                            </div> <!-- end card -->
							
                    </div>  <!-- end col -->
                </div>
                <!-- end row -->
            </div> <!-- container-fluid -->
        </div> <!-- content -->

        <!-- Footer Start -->
        <footer class="footer">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-12">
                        <?php echo date('Y'); ?> &copy; RealAuto. All Rights Reserved. Crafted with <i class='uil uil-heart text-danger font-size-12'></i> by <a href="#">RealAuto</a>
                    </div>
                </div>
            </div>
        </footer>
        <!-- end Footer -->
    </div>

    <!-- ============================================================== -->
    <!-- End Page content -->
    <!-- ============================================================== -->
    <script type="text/javascript">
        function myActive(id){
            var status = document.getElementById('active').value;
           
            $.ajax({
                 method: "POST",
                 url: "ajaxactive-staff/"+id,
                 data: {
                        _token: '<?php echo csrf_token();?>',
                        id: id,
                        status:status
                    },
                success: function (data) {
                        alert(data);
                        window.location.reload()
                    }    
            });
        }
        function myStatus(id){
            var status = document.getElementById('status').value;
           
            $.ajax({
                 method: "POST",
                 url: "ajaxactive-staff/"+id,
                 data: {
                        _token: '<?php echo csrf_token();?>',
                        id: id,
                        status:status
                    },
                success: function (data) {
                        alert(data);
                        window.location.reload()
                    }    
            });
        }
        
    </script>
@endsection
