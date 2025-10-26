@extends('layouts.app')
@section('title', 'Edit Admins')
@section('content')

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
                                <li class="breadcrumb-item"><a href="<?php echo url('/manage-admins'); ?>"> Manage Admins User </a></li>
                                <li class="breadcrumb-item active" aria-current="page">User's</li>
                            </ol>
                        </nav>
                        <h4 class="mb-1 mt-0">Edit User</h4>
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

                                <form action="<?php echo url('/edit-sells-post/'.$admindata->id); ?>" method="post" name="edit-admins-post" class="form-horizontal">
                                    @csrf
                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Name <span class="required">*</span></label>
                                        <div class="col-6">
                                            <input type="text" name="name" class="form-control" placeholder="Name" required value="{{ $admindata->name }}">
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Email <span class="required">*</span></label>
                                        <div class="col-6">
                                            <input type="email" name="email" class="form-control" placeholder="Email" required value="{{ $admindata->email }}" readonly>
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Mobile <span class="required">*</span></label>
                                        <div class="col-6">
                                            <input type="text" name="phone_no" class="form-control" placeholder="Mobile" required value="{{ $admindata->phone_no }}">
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label for="inputPassword5" class="col-3 col-form-label">Status <span class="required">*</span></label>
                                        <div class="col-6">
                                            <select name="status" class="custom-select mb-2" required>
                                                <option value="1" @if($admindata->status == 1) selected @endif>Active</option>
                                                <option value="2" @if($admindata->status == 2) selected @endif>In-Active</option>
                                            </select>
                                        </div>
                                    </div>
									
									<div class="form-group row mb-3">
                                        <label for="inputPassword5" class="col-3 col-form-label">Change Password <span class="required">*</span></label>
                                        <div class="col-6">
                                           Yes <input type="radio" onclick="javascript:yesnoCheck();" name="yesno" id="yesCheck" value="1" > No <input type="radio" 
onclick="javascript:yesnoCheck();" name="yesno" id="noCheck" checked value="2"><br>
											<div id="ifYes" style="visibility:hidden">
											   <strong> Password : </strong> <input type="text" name="pwd" class="form-control" 
placeholder="Enter Password"  value=""><br>
											</div>
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
                        <?php echo date('Y'); ?> &copy; Realauto. All Rights Reserved. Crafted with <i class='uil uil-heart text-danger font-size-12'></i> by <a href="#" 
target="_blank">Realauto</a>
                    </div>
                </div>
            </div>
        </footer>
        <!-- end Footer -->
    </div>

    <!-- ============================================================== -->
    <!-- End Page content -->
    <!-- ============================================================== -->

<script>
function yesnoCheck() {
    if (document.getElementById('yesCheck').checked) {
        document.getElementById('ifYes').style.visibility = 'visible';
    } else  {
		document.getElementById('ifYes').style.visibility = 'hidden';
	}
}
function showApi(key, value) {
	//alert(key)
	
	if (key == "sms") {
		if(value=="1") {
			$("#sms-api-key").show();
			//document.getElementById("sms-api-key").style.visibility = 'visible';
		} else {
			$("#sms-api-key").hide();
			//document.getElementById("sms-api-key").style.visibility = 'hidden';
		}
	}
	
	if (key == "email") {
		if(value=="1") {
			$("#email-api-key").show();
			//document.getElementById("email-api-key").style.visibility = 'visible';
		} else {
			$("#email-api-key").hide();
			//document.getElementById("email-api-key").style.visibility = 'hidden';
		}
	}
	if (key == "whatsapp") {
		if(value=="1") {
			$("#whatsapp-api-key").show();
			document.getElementById("whatsapp-api-key").style.visibility = 'visible';
		} else {
			$("#whatsapp-api-key").hide();
			document.getElementById("whatsapp-api-key").style.visibility = 'hidden';
		}
	}
	
}
</script>
@endsection
