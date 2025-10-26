@extends('layouts.app')
@section('title', 'Lead Settings')
@section('content')
<!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">-->
	<link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.7.0/css/all.css'>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
<script src="{{ asset('/assets/js/multiselect.js') }}"></script>
    <!-- ============================================================== -->
    <!-- Start Page Content here -->
    <!-- ============================================================== -->
<style>
/*
.form-group input[type="checkbox"] {
    display: none; 
}

.form-group input[type="checkbox"] + .btn-group > label span {
    width: 20px;
}

.form-group input[type="checkbox"] + .btn-group > label span:first-child {
    display: none;
}
.form-group input[type="checkbox"] + .btn-group > label span:last-child {
    display: inline-block;   
}

.form-group input[type="checkbox"]:checked + .btn-group > label span:first-child {
    display: inline-block;
}
.form-group input[type="checkbox"]:checked + .btn-group > label span:last-child {
    display: none;   
}
*/
#exampleModal1 .modal-content {
    margin-top: 50px;
}
#videoModal .modal-content {
    margin-top: 0 !important;
}
</style>

    <div class="content-page">
        <div class="content">
            <!-- Start Content-->
            <div class="container-fluid">
                <div class="row page-title">
                    <div class="col-md-12">
                        <nav aria-label="breadcrumb" class="float-right mt-1">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><a href="{{ route('dashboard') }}">Dashboard</a></li>
                                <li class="breadcrumb-item active" aria-current="page">Lead Settings</li>
                            </ol>
                        </nav>
                        <h4 class="mb-1 mt-0">Automated Assign Lead Settings</h4>
<p>Click the project from the <span style="color:red"> Left box </span> and select the team from <span style="color:red">Rigt box</span> to assign the leads automatically & 
accordingly</p>
                    </div>
                </div>

                <!-- end row -->
                <!-- Default switch -->
                <?php
	
		$autoAssign = isset($auto_assign->auto_assign_leads) ? $auto_assign->auto_assign_leads : 0; 
		?>
                
                <form method="post">
                    <div class="custom-control custom-switch">   
                    <input type="hidden" name="switchoff" value="{{$autoAssign}}" id="switchoff">    
                    <input type="checkbox" class="custom-control-input " id="customSwitches" {{ $autoAssign == "1" ? "checked" : ""}} onchange="mySwitchoff()">
                    <label class="custom-control-label" for="customSwitches">Switch On Your all leads</label>
                    <span id="sms" style="color: #fff;font-size: 16px;font-weight: 600;margin-left: 50px;background: #0eb94b;border-radius: 5px;"></span>
                    
                </form>
                </div><br>
                
                

                <div class="row">
                    @if(isset($autoAssign) && $autoAssign == "1")
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

                                <form action="<?php echo url('/auto-lead-assign'); ?>" method="post" name="save-admin" class="form-horizontal">
                                    @csrf
									<input type="hidden" name = "staffPriority" style="display:none" id="staffPriority" />
									<div class="container">
									<div class="row">
									<div class="col-md-4">
										<h3>Select Projects</h3><hr />
										<div style="overflow-y: scroll; height:200px;">
										<?php $i = 0; ?>
										@foreach ($projectList as $project)
										<div class="[ form-group ]"  >
            
            <div class="[ btn-group ]" style="left:30px"> 
                <label for="fancy-checkbox-default" class="[ btn btn-default ]">
				<input type="checkbox" value="{{$project->id}} | {{ucwords($project->project_name)}}" class="projects" name="project_lists[]" 
id="project{{$project->id}}" 
autocomplete="off" />
                  <!--  <span class="[ glyphicon glyphicon-ok ]"></span> -->
                   
                </label>
                <label for="fancy-checkbox-default" class="[ btn btn-default active ]">
					{{ucwords($project->project_name)}}
                </label>
            </div>
        </div>
		@endforeach
		</div>
		</div>
		<div class="col-md-4">
        <h3>Select Staff</h3><hr />
		<div style="overflow-y: scroll; height:200px;">
		<?php $j=0; ?>
		@foreach ($staffList as $rowstaff)
        <div class="[ form-group ]" >
            
            <div class="[ btn-group ]"  style="left:30px">
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default ]">
                     <input type="checkbox" class="staffs" value="{{$rowstaff->id}} | {{ucwords($rowstaff->name)}}" name="staff_list[]" id="staff{{++$j}}" autocomplete="off" />
					 <!-- <span class="[ glyphicon glyphicon-ok ]"></span>
					
					<span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
					-->
                </label>
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default active ]">
				{{ucwords($rowstaff->name)}}
                </label>
            </div>
        </div>
		@endforeach
		</div></div>
		<div class="col-md-4">
        <h3>Select Campaigns</h3><hr />
		<div style="overflow-y: scroll; height:200px;">
		<?php $j=0; ?>
		@foreach ($campaigns as $rowCampaigns)
        <div class="[ form-group ]" >
            
            <div class="[ btn-group ]"  style="left:30px">
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default ]">
                     <input type="radio" class="rowCampaigns" value="{{$rowCampaigns->id}}" name="campaigns" id="Campaigns" autocomplete="off" />
					 <!-- <span class="[ glyphicon glyphicon-ok ]"></span>
					
					<span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
					-->
                </label>
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default active ]">
				{{ucwords($rowCampaigns->campaigns_name)}}
                </label>
            </div>
        </div>
		@endforeach
		</div></div>
    </div>
	</div>
	
	<p>You have <span id="dynamic-project" style="color:blue">Not</span> selected Project & selected staff in order is <span id="dynamic-staff" style="color:blue">Not 
Assigned</span>
                                <!--    <div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Select Projects <span class="required">*</span></label>
                                        <div class="col-9">
											<select name="project_id" class="form-control custom-select mb-2" required>
												<option value="">Select Project</option>
												@foreach ($projectList as $rowstaff)
												<option value="{{ $rowstaff->id }}">{{ ucwords($rowstaff->project_name) }}</option>
												@endforeach
											</select>
										</div>
                                    </div>
                                   
									<div class="form-group row mb-3">
                                        <label for="inputEmail3" class="col-3 col-form-label">Select Executives <span class="required">*</span></label>
                                        <div class="col-9">
											<div class="container" style="margin-top: 20px;" id="multiselectlist">
												<div class="form-group col-sm-3">
													<label>Executives List</label>
													<select name="staff_id" class="form-control custom-select mb-2"  multiple 
id="multivalfrom" size="8">
														
														@foreach ($staffList as $rowstaff)
														<option value="{{ucwords($rowstaff->name).' | Id -'.$rowstaff->id}}">{{ 
ucwords($rowstaff->name) }}</option>
														@endforeach
													</select>
												</div>
												<div class="col-sm-1">
													<div class="btn-group-vertical w-100" style="width:100%">
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Move All" id="move_all_btn"><i class='fas fa-angle-double-right'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Move" id="move_btn"><i class='fas fa-angle-right'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Remove" id="remove_btn"><i class='fas fa-angle-left'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Remove All" id="remove_all_btn"><i class='fas fa-angle-double-left'></i></button>
													</div>	
												</div>
												<div class="form-group col-sm-3">
												<label>Assigned List</label>
													<select name="user-list[]" multiple class="form-control" id="multivalto" 
size="11" required>
													</select>
												</div>
												<div class="col-sm-1">
													<div class="btn-group-vertical" style="width:100%">
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Top" id="top_btn"><i class='fas fa-angle-double-up'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Up" id="up_btn"><i class='fas fa-angle-up'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Down" id="down_btn"><i class='fas fa-angle-down'></i></button>
														<button type="button" class="btn btn-default col-sm-12 btn-sm" 
title="Bottom" id="bottom_btn"><i class='fas fa-angle-double-down'></i></button>
													</div>
												</div>
											</div>
										</div>
										-->
										
										<div class="form-group mb-0 justify-content-end row">
											<div class="col-9" style="top:10px">
												<button type="submit" class="btn btn-info"><strong>Submit</strong></button>
												<!-- <a href="{{ route('manage-admins') }}"><button type="button" class="btn 
btn-success">Back</button></a> -->
											</div>
										</div>
                                </form>
                            </div><!-- end card-body -->
                            <!-- offswitch section start -->
                            <!-- end card-body --> <!-- end -->
                        </div>  <!-- end card -->
	<!--
<div class="container">
 <div class="[ col-xs-12 col-sm-6 ]">
        <h3>Select Projects</h3><hr />
		<div style="overflow-y: scroll; height:200px;">
		<?php $i = 0; ?>
		@foreach ($projectList as $project)
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-default[]" id="fancy-checkbox-default{{$i}}" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-default" class="[ btn btn-default ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-default" class="[ btn btn-default active ]">
					{{ucwords($project->project_name)}}
                </label>
            </div>
        </div>
		@endforeach
		
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-primary" id="fancy-checkbox-primary" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-primary" class="[ btn btn-primary ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-primary" class="[ btn btn-default active ]">
                    Primary Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-success" id="fancy-checkbox-success" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-success" class="[ btn btn-success ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-success" class="[ btn btn-default active ]">
                    Success Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-info" id="fancy-checkbox-info" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-info" class="[ btn btn-info ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-info" class="[ btn btn-default active ]">
                    Info Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-warning" id="fancy-checkbox-warning" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-warning" class="[ btn btn-warning ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-warning" class="[ btn btn-default active ]">
                    Warning Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-danger" id="fancy-checkbox-danger" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-danger" class="[ btn btn-danger ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-danger" class="[ btn btn-default active ]">
                    Danger Checkbox
                </label>
            </div>
        </div>
         <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-danger" id="fancy-checkbox-danger" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-danger" class="[ btn btn-danger ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-danger" class="[ btn btn-default active ]">
                    Danger Checkbox
                </label>
            </div>
        </div> <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-danger" id="fancy-checkbox-danger" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-danger" class="[ btn btn-danger ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-danger" class="[ btn btn-default active ]">
                    Danger Checkbox
                </label>
            </div>
        </div> <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-danger" id="fancy-checkbox-danger" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-danger" class="[ btn btn-danger ]">
                    <span class="[ glyphicon glyphicon-ok ]"></span>
                    <span> </span>
                </label>
                <label for="fancy-checkbox-danger" class="[ btn btn-default active ]">
                    Danger Checkbox
                </label>
            </div>
        </div>
		
    </div>
	
	</div>
-->
<!--
    <div class="[ col-xs-12 col-sm-6 ]">
        <h3>Select Staff</h3><hr />
		<div style="overflow-y: scroll; height:200px;width:400px">
		<?php $j=0; ?>
		@foreach ($staffList as $rowstaff)
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-default-custom-icons[]" id="fancy-checkbox-default-custom-icons{{++$j}}" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default ]">
                    
					
					<span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
					
                </label>
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default active ]">
				{{$rowstaff->name}}
                </label>
            </div>
        </div>
		@endforeach
		<!--
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-primary-custom-icons" id="fancy-checkbox-primary-custom-icons" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-primary-custom-icons" class="[ btn btn-primary ]">
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                </label>
                <label for="fancy-checkbox-primary-custom-icons" class="[ btn btn-default active ]">
                    Primary Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-success-custom-icons" id="fancy-checkbox-success-custom-icons" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-success-custom-icons" class="[ btn btn-success ]">
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                </label>
                <label for="fancy-checkbox-success-custom-icons" class="[ btn btn-default active ]">
                    Success Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-info-custom-icons" id="fancy-checkbox-info-custom-icons" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-info-custom-icons" class="[ btn btn-info ]">
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                </label>
                <label for="fancy-checkbox-info-custom-icons" class="[ btn btn-default active ]">
                    Info Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-warning-custom-icons" id="fancy-checkbox-warning-custom-icons" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-warning-custom-icons" class="[ btn btn-warning ]">
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                </label>
                <label for="fancy-checkbox-warning-custom-icons" class="[ btn btn-default active ]">
                    Warning Checkbox
                </label>
            </div>
        </div>
        <div class="[ form-group ]">
            <input type="checkbox" name="fancy-checkbox-danger-custom-icons" id="fancy-checkbox-danger-custom-icons" autocomplete="off" />
            <div class="[ btn-group ]">
                <label for="fancy-checkbox-danger-custom-icons" class="[ btn btn-danger ]">
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                </label>
                <label for="fancy-checkbox-danger-custom-icons" class="[ btn btn-default active ]">
                    Danger Checkbox
                </label>
            </div>
        </div>
		
    </div></div>
	</div>
-->






	                    
						<div class="card">
						<div class="card-body">
						
							<?php
							
							if (count($assignedProjects)>0) { ?>
							<table id="idsssss1" class="table dt-responsive">
								<thead>
									<tr>
										<!--<th>#</th>-->
										<th>Sl.no</th>
										<th>Project Name</th>
										<th>Assignee Name</th>
										<th>Campaigns Name</th>
										<th>Action</th>	
									</tr>
								</thead>

								<tbody>
									<?php
									$i = 0;
									foreach($assignedProjects as $key => $value) {
									//print_r($value); die;
									$i++;

									?>
										<tr>
											<td>{{$i}}</td>
											<td>
											<?php
											foreach($projectList as $project) {
												
												if ($project->id == $value->project_id) {
													echo $project->project_name ;
													break;
												}
											}
											?>
											</td>
											<td>
											<?php
											$userIds = explode("|",$value->executive_ids);
											
											foreach($userIds as $user) {
												
												foreach($staffList as $staff) {
													
													if ($staff->id == $user) {
														
														echo $staff->name.",";
														
														
													}
												}
											}
											?>
											
											</td>
											<td>
											<?php
											if($value->campaigns_id != NULL){
											$Campaigns = \App\Models\Campaign::where([['id', $value->campaigns_id]])->first();

											echo $Campaigns->campaigns_name;
											}
											?>
											</td>
											<td>
											 <div class="icon-item">
                                                    <a href="#" onclick="edit({{$value->project_id}})">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 
2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                                                    </a>
                                                    <a href="{{ url('/delete-auto-assign/'.$value->id) }}" >
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-delete"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" 
x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>
                                                    </a>
                                                </div>
											</td>
										</tr>
									<?php } ?>
								</tbody>
							</table>
								
							<?php } else { ?>
						
							<table id="idsssss" class="table dt-responsive nowrap">
								<tr>
									<th colspan=4 style="text-align:center;"> No Record Found </th>
								</tr>
							</table>
						<?php } ?>

                                </div> <!-- end card body-->
                            </div> <!-- end card -->
							
                    </div>  <!-- end col -->@else
                    <div class="col-xl-12" style="pointer-events: none;opacity: 0.4;">
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

                                <form action="<?php echo url('/auto-lead-assign'); ?>" method="post" name="save-admin" class="form-horizontal">
                                    @csrf
                                    <input type="hidden" name = "staffPriority" style="display:none" id="staffPriority" />
                                    <div class="container">
                                    <div class="row">
                                    <div class="col-md-6">
                                        <h3>Select Projects</h3><hr />
                                        <div style="overflow-y: scroll; height:200px;">
                                        <?php $i = 0; ?>
                                        @foreach ($projectList as $project)
                                        <div class="[ form-group ]"  >
            
            <div class="[ btn-group ]" style="left:30px"> 
                <label for="fancy-checkbox-default" class="[ btn btn-default ]">
                <input type="checkbox" value="{{$project->id}} | {{ucwords($project->project_name)}}" class="projects" name="project_lists[]" 
id="project{{$project->id}}" 
autocomplete="off" />
                  <!--  <span class="[ glyphicon glyphicon-ok ]"></span> -->
                   
                </label>
                <label for="fancy-checkbox-default" class="[ btn btn-default active ]">
                    {{ucwords($project->project_name)}}
                </label>
            </div>
        </div>
        @endforeach
        </div>
        </div>
        <div class="col-md-6">
        <h3>Select Staff</h3><hr />
        <div style="overflow-y: scroll; height:200px;width:400px">
        <?php $j=0; ?>
        @foreach ($staffList as $rowstaff)
        <div class="[ form-group ]" >
            
            <div class="[ btn-group ]"  style="left:30px">
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default ]">
                     <input type="checkbox" class="staffs" value="{{$rowstaff->id}} | {{ucwords($rowstaff->name)}}" name="staff_list[]" id="staff{{++$j}}" autocomplete="off" />
                     <!-- <span class="[ glyphicon glyphicon-ok ]"></span>
                    
                    <span class="[ glyphicon glyphicon-plus ]"></span>
                    <span class="[ glyphicon glyphicon-minus ]"></span>
                    -->
                </label>
                <label for="fancy-checkbox-default-custom-icons" class="[ btn btn-default active ]">
                {{ucwords($rowstaff->name)}}
                </label>
            </div>
        </div>
        @endforeach
        </div></div>
    </div>
    </div>
    
    <p>You have <span id="dynamic-project" style="color:blue">Not</span> selected Project & selected staff in order is <span id="dynamic-staff" style="color:blue">Not 
Assigned</span>
                                        <div class="form-group mb-0 justify-content-end row">
                                            <div class="col-9" style="top:10px">
                                                <button type="submit" class="btn btn-info">Submit</button>
                                                <!-- <a href="{{ route('manage-admins') }}"><button type="button" class="btn 
btn-success">Back</button></a> -->
                                            </div>
                                        </div>
                                </form>
                            </div><!-- end card-body -->
                            <!-- offswitch section start -->
                            <!-- end card-body --> <!-- end -->
                        </div>  <!-- end card -->
   
                        <div class="card">
                        <div class="card-body">
                        
                            <?php
                            
                            if (count($assignedProjects)>0) { ?>
                            <table id="idsssss1" class="table dt-responsive">
                                <thead>
                                    <tr>
                                        <!--<th>#</th>-->
                                        <th>Sl.no</th>
                                        <th>Project Name</th>
                                        <th>Assignee Name</th>
                                        <th>Action</th> 
                                    </tr>
                                </thead>

                                <tbody>
                                    <?php
                                    $i = 0;
                                    foreach($assignedProjects as $key => $value) {
                                    //print_r($value); die;
                                    $i++;

                                    ?>
                                        <tr>
                                            <td>{{$i}}</td>
                                            <td>
                                            <?php
                                            foreach($projectList as $project) {
                                                
                                                if ($project->id == $value->project_id) {
                                                    echo $project->project_name ;
                                                    break;
                                                }
                                            }
                                            ?>
                                            </td>
                                            <td>
                                            <?php
                                            $userIds = explode("|",$value->executive_ids);
                                            
                                            foreach($userIds as $user) {
                                                
                                                foreach($staffList as $staff) {
                                                    
                                                    if ($staff->id == $user) {
                                                        
                                                        echo $staff->name.",";
                                                        
                                                        
                                                    }
                                                }
                                            }
                                            ?>
                                            
                                            </td>
                                            <td>
                                             <div class="icon-item">
                                                    <a href="#" onclick="edit({{$value->project_id}})">
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 
2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                                                    </a>
                                                    <a href="{{ url('/delete-auto-assign/'.$value->id) }}" >
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-delete"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" 
x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>
                                                    </a>
                                                </div>
                                            </td>
                                        </tr>
                                    <?php } ?>
                                </tbody>
                            </table>
                                
                            <?php } else { ?>
                        
                            <table id="idsssss" class="table dt-responsive nowrap">
                                <tr>
                                    <th colspan=4 style="text-align:center;"> No Record Found </th>
                                </tr>
                            </table>
                        <?php } ?>

                                </div> <!-- end card body-->
                            </div> <!-- end card -->
                            
                    </div>  <!-- end col -->@endif
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
<script>
    //switchoff buuton script start
    function mySwitchoff(){
        var switchoff = $('#switchoff').val();
        var formData = {_token: "{{ csrf_token() }}",switchoff:switchoff}; 
    $.ajax({
       type:'POST',
       url:"{{ url('switch') }}",
       data:formData,
       success:function(data){
            document.getElementById('sms').innerHTML = switchoff == "1" ? "Switch Off Successfully !" : "Switch ON Successfully !";
            $("#sms").css("padding","8px");
            setTimeout(function(){
               window.location.reload(1);
            }, 1000);
        }
    });
    }
    //switchon buuton script start
    function mySwitchon(){
        var switchoff = $('#switchon').val();
        var formData = {_token: "{{ csrf_token() }}",switchoff:switchoff}; 
    $.ajax({
       type:'POST',
       url:"{{ url('switch') }}",
       data:formData,
       success:function(data){
            document.getElementById('sms').innerHTML = "Switch On Successfully !";
            $("#sms").css("padding","8px");
            setTimeout(function(){
               window.location.reload(1);
           }, 1000);
        }
    });
    }
    //endcode
    
	$(document).ready(function(){
			assign_btn_action('multiselectlist');
		});
		
	$(".projects").on('click', function() {
		// in the handler, 'this' refers to the box clicked on
		var $box = $(this);
		if ($box.is(":checked")) {
		// the name of the box is retrieved using the .attr() method
		// as it is assumed and expected to be immutable
		var group = "input:checkbox[name='" + $box.attr("name") + "']";
		// the checked state of the group/box on the other hand will change
		// and the current value is retrieved using .prop() method
		$(group).prop("checked", false);
		$box.prop("checked", true);
		} else {
		$box.prop("checked", false);
		}
	});
	let list = [];
	let listIds = [];
	let listName =[];
	$(".staffs").on('click', function() {
		// in the handler, 'this' refers to the box clicked on
		var $box = $(this);
		
		if ($box.is(":checked")) {
			list.push($box.attr("value"))
			var text = $box.attr("value").split("|");
			listIds.push(text[0])
			listName.push(text[1])
		} else {
			const index = list.indexOf($box.attr("value"));
			
			if (index > -1) {
			  list.splice(index, 1);
			  var text = $box.attr("value").split("|");
			  var index1 = listIds.indexOf(text[0]);
			  var index2 = listName.indexOf(text[1]);
			  listIds.splice(index1, 1);
			  listName.splice(index2, 1);
			  
			}
		}
		document.getElementById("staffPriority").value = listIds
		var text = $box.attr("value").split("|");
		document.getElementById("dynamic-staff").innerHTML = listName
	console.log(list)	
	});
	
	$(".projects").on('click', function() {
		// in the handler, 'this' refers to the box clicked on
		var $box = $(this);
		
		if ($box.is(":checked")) {
			var text = $box.attr("value").split("|");
			document.getElementById("dynamic-project").innerHTML = text[1]
		}
		
			
	});

function edit(id) {
var checkProject = document.getElementById("project"+id);


    checkProject.checked = true;
var text = checkProject.value.split("|");
                        document.getElementById("dynamic-project").innerHTML = text[1]

}

	
</script>
    <!-- ============================================================== -->
    <!-- End Page content -->
    <!-- ============================================================== -->

@endsection


