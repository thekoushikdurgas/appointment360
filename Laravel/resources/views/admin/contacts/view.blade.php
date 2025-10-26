@extends('admin.layouts.app')

@section('title')
All Contacts
@endsection

@section('content')

<div class="fixed_height_section">
    <div class="container-fluid zp_GhGgo">
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
            <h1 class="h3 mb-0 text-gray-800">Contacts</h1>
            <span>
                <?php
                $Authuser = auth()->user();
                $download_limit = auth()->user()->download_limit;
                if (!is_null($Authuser)) {
                    if ($Authuser->role == 1) {
                        ?>
                        <a href="{{route('admin.contacts.create')}}" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-plus fa-sm text-white-50"></i> Create New
                        </a>
                        <a href="{{route('admin.contacts.import_contacts')}}" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-plus fa-sm text-white-50"></i> Import
                        </a>
                        <?php
                    }
                }
                ?>
                <a href="#" id="export_records" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                    <i class="fas fa-download fa-sm text-white-50"></i> Export selected
                </a>
            </span>
        </div>
        <div class="d-flex flex-column vh-71 overflow-hidden">
            <div class="row h-100  mx-0 overflow-hidden">
                <div class="container-fluid h-100">
                    <div class="row h-100">
                        <div class="col-lg-3 h-100">
                            <div class="card  h-100 shadow mb-4">
							
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary">Search</h6>
                                </div>
                                <div class="card-body overflow-hidden">

                                    <div class="col-md-12 h-100 px-0">


                                        <div class="panel-group wrap h-100 scrollable overflow-auto" id="accordion" role="tablist" aria-multiselectable="true">
                                            <!-- end of panel -->

                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingTwo">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                                            <i class="fas fa-id-badge"></i>   Name
                                                        </a>
                                                    </h4><small class="name-title"></small>
                                                </div>
                                                <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
                                                    <div class="panel-body">
                                                        <input type="text" class="form-control my-3" id="name_search" style="padding: 3px;" name="name_search" placeholder="Name" /> 
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- end of panel -->

                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingThree">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                                            <i class="fas fa-medal"></i>  Job Titles
                                                        </a>
                                                    </h4>
													<small class="job-title"></small>
                                                </div>
												<?php
												//echo"<pre>";print_r($filters['organizationNumEmployeesRanges']);
											//	echo"</pre>";
												
												?>
                                                <div id="collapseThree" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">
                                                    <div class="panel-body">
                                                        <select id="job_titles" class="js-example-basic-single form-control " name="job_titles" style="width: 100%" multiple="multiple">
                                                            @foreach($job_titles_list as $job_titles)
                                                            <option value="{{$job_titles->title}}"             {{ in_array(strtolower($job_titles->title), array_map('strtolower', $filters['personTitles'] ?? [])) ? 'selected' : '' }}>{{$job_titles->title}}</option>
                                                            @endforeach
                                                        </select>
                                                        <!--<input type="text" class="form-control my-3" style="padding: 3px;" name="job_titles"  placeholder="Job Title" />--> 
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- end of panel -->

                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingFour">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                                                            <i class="fas fa-building"></i> Company
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseFour" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingFour">
                                                    <div class="panel-body">
                                                        <select class="js-company form-control " name="company[]" style="width: 100%" multiple="multiple">

                                                        </select>
                                                        <!--<input type="text" class="form-control my-3" style="padding: 3px;" name="company"  placeholder="Company"  />--> 
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingLoc">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseLoc" aria-expanded="false" aria-controls="collapseLoc">
                                                            <i class="fas fa-map-marker-alt"></i>Location
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseLoc" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingLoc">
                                                    <div class="panel-body">
                                                       <?php
															$personLocations = !empty($filters['personLocations']) ? implode(",", $filters['personLocations']) : '';;
													  // print_r($filters['personLocations']);?>
                                                        <input type="text" class="form-control my-3" style="padding: 3px;" name="location" id="search_location" placeholder="Location" value="<?php echo $personLocations;  ?>	"  />
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingFive">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
                                                            <i class="fas fa-user-friends"></i> # Employees
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseFive" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingFive">
                                                    <div class="panel-body">
                                                        <div class="col">
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="0-10" {{ in_array('1,10', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckVerified">
                                                                <label class="form-check-label" for="flexCheckDefault">
                                                                    0-10
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input  employess_range" {{ in_array('11,20', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} type="checkbox" value="11-20" id="flexCheckGuessed" >
                                                                <label class="form-check-label" for="flexCheckGuessed">
                                                                    11-20
                                                                </label>
                                                            </div>
                                                            <div class="form-check"> 
                                                                <input class="form-check-input employess_range" type="checkbox" value="21-50" {{ in_array('21,50', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckUser" >
                                                                <label class="form-check-label" for="flexCheckUser">
                                                                    21-50
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input  employess_range" type="checkbox" value="51-100" {{ in_array('51,100', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNoData" >
                                                                <label class="form-check-label" for="flexCheckNoData">
                                                                    51-100
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="101-200" {{ in_array('101,200', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    101-200
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="201-500" {{ in_array('201,500', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    201-500
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="501-1000"  {{ in_array('501,1000', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    501-1000
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="1001-2000"  {{ in_array('1001,2000', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }}  id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    1001-2000
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="2001-5000" {{ in_array('2001,5000', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    2001-5000
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="5001-10000" {{ in_array('5001,10000', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }} id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    5001-10000
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input employess_range" type="checkbox" value="10001" {{ in_array('10001', $filters['organizationNumEmployeesRanges'] ?? []) ? 'checked' : '' }}  id="flexCheckNA" >
                                                                <label class="form-check-label" for="flexCheckNA">
                                                                    10001+
                                                                </label>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingSix">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseSix" aria-expanded="false" aria-controls="collapseSix">
                                                            <i class="fas fa-industry"></i> Industry
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseSix" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingSix">
                                                    <div class="panel-body">
                                                        <div class="col my-3">
                                                            <select class="js-industry form-control " name="industry" style="width: 100%" multiple="multiple">
															@foreach($industryList as $industry)
<option value="{{ $industry->name }}" 
    {{ isset($filters['organizationIndustryTagIds']) && in_array($industry->tag_id, $filters['organizationIndustryTagIds']) ? 'selected' : '' }}>
    {{ $industry->name }}
</option>                                                            @endforeach
                                                            </select>
                                                                <!--<input type="text" class="form-control my-3" style="padding: 3px;" name="industry" placeholder="Industry" />-->
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                            </div>
                                            <!--                            <div class="panel">
                                                                            <div class="panel-heading" role="tab" id="headingSeven">
                                                                                <h4 class="panel-title">
                                                                                    <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseSeven" aria-expanded="false" aria-controls="collapseSeven">
                                                                                        <i class="fas fa-chart-bar"></i> Buying Intent
                                                                                    </a>
                                                                                </h4>
                                                                            </div>
                                                                            <div id="collapseSeven" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingSeven">
                                                                                <div class="panel-body">
                                                                                    Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch.
                                                                                </div>
                                                                            </div>
                                                                        </div>-->
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingEight">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseEight" aria-expanded="false" aria-controls="collapseEight">
                                                            <i class="fas fa-mail-bulk"></i> Email Status
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseEight" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingEight">
                                                    <div class="panel-body">
                                                        <div class="col">
                                                                                                                    
                                                            
                                                            <div class="form-check">
                                                                <input class="form-check-input email_status" type="checkbox" value="Verified" id="flexCheckVerified"
                                                                       {{ in_array('verified', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckVerified">
                                                                    Verified
                                                                </label>
                                                            </div> 
															<div class="form-check">
                                                                <input class="form-check-input email_status" type="checkbox" value="Unverified" id="flexCheckVerified"
                                                                       {{ in_array('Unverified', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckVerified">
                                                                    Unverified
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input email_status" type="checkbox" value="Guessed" id="flexCheckGuessed"
                                                                       {{ in_array('guessed', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckGuessed">
                                                                    Guessed
                                                                </label>
                                                            </div>
                                                            <div class="form-check"> 
                                                                <input class="form-check-input email_status" type="checkbox" value="User Managed" id="flexCheckUser"
                                                                       {{ in_array('User Managed', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckUser">
                                                                    User Managed
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input email_status" type="checkbox" value="New Data Available" id="flexCheckNoData"
                                                                       {{ in_array('New Data Available', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckNoData">
                                                                    New Data Available
                                                                </label>
                                                            </div>
                                                            <div class="form-check">
                                                                <input class="form-check-input email_status" type="checkbox" value="N/A" id="flexCheckNA"
                                                                       {{ in_array('N/A', $filters['contactEmailStatusV2'] ?? []) ? 'checked' : '' }}>
                                                                       <label class="form-check-label" for="flexCheckNA">
                                                                    N/A
                                                                </label>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                            </div>
                                            <!--                            <div class="panel">
                                                                            <div class="panel-heading" role="tab" id="headingNine">
                                                                                <h4 class="panel-title">
                                                                                    <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseNine" aria-expanded="false" aria-controls="collapseNine">
                                                                                        <i class="fas fa-vector-square"></i> Scores
                                                                                    </a>
                                                                                </h4>
                                                                            </div>
                                                                            <div id="collapseNine" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingNine">
                                                                                <div class="panel-body">
                                                                                    Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch.
                                                                                </div>
                                                                            </div>
                                                                        </div>-->
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="headingTen">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTen" aria-expanded="false" aria-controls="collapseTen">
                                                            <i class="fas fa-microchip"></i> Technologies
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapseTen" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTen">
                                                    <div class="panel-body">
                                                        <select class="js-technologies form-control " name="keywords" style="width: 100%" multiple="multiple">

                                                        </select>

<!--                                        <input
                                            type="text"
                                            class="form-control p-4"
                                            data-role="tagsinput"
                                            />-->
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="heading11">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse11" aria-expanded="false" aria-controls="collapse11">
                                                            <i class="fas fa-dollar-sign"></i> Revenue
                                                        </a>
                                                    </h4>
                                                </div>
												 <?php
												 $revenueRangemax=$revenueRangemin='';
															if(!empty($filters['revenueRange']))
															{
																$revenueRangemax=$filters['revenueRange']['max'];
																$revenueRangemin=$filters['revenueRange']['min'];
															}

																
																
													  // print_r($filters['personLocations']);?>
                                                <div id="collapse11" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading11">
                                                    <div class="panel-body">
                                                        <div class="zp_iJMr1">
                                                            <div class="px-2">
                                                                <input type="number" id="min-rev" class="form-control typeahead" placeholder="Min" value="<?php echo $revenueRangemin; ?>"></div>
                                                            <span class="p-2">-</span>
                                                            <div class="px-2"><input type="number" class="form-control typeahead" id="max-rev" placeholder="Max" value="<?php echo $revenueRangemax; ?>">
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="panel">
                                                <div class="panel-heading" role="tab" id="heading12">
                                                    <h4 class="panel-title">
                                                        <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse12" aria-expanded="false" aria-controls="collapse12">
                                                            <i class="fas fa-money-check-alt"></i> LinkedIn URL
                                                        </a>
                                                    </h4>
                                                </div>
                                                <div id="collapse12" class="panel-collapse collapse" role="tabpanel" aria-labelledby="heading12">
                                                    <div class="panel-body">
                                                        <div class="col">
                                                           
                                                        <input type="text" class="form-control my-3" style="padding: 3px;" name="LinkedIn" id="search_linkedin" placeholder="LinkedIn URL" />


                                                        </div> 
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- end of panel -->

                                        </div>
                                        <!-- end of #accordion -->


                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-9 h-100">
                            <div class="card h-100 shadow mb-4">

                                <div class="card-body overflow-hidden py-0  px-1">
                                    <!--                                    <div class="d-sm-flex align-items-center justify-content-between"> <div> Select All</div>
                                                                        </div>-->

                                    <div class="">
                                        <div class="table-responsive h-100">



                                            <table id="contact_type_table" class="table table-bordered " width="100%" cellspacing="0" data-page-length='25'>
                                                <thead>
                                                    <tr class="">
                                                        <th rowspan="1" colspan="1" class="">
                                                            <div class="zp_rJZsu">
                                                                <span class="zp_FG0Vx"><input type="checkbox" id="select-all" onClick="toggleCheckboxes(this, 'contact_ids')" /></span>

                                                                <span class="zp_FG0Vx" style="padding-left: 12px;">
                                                                    <div class="zp_Yfixs column-sort-container">
                                                                        <span class="zp_V7agI">Name</span>

                                                                    </div>
                                                                </span>
                                                            </div>
                                                        </th>
                                                        <th rowspan="1" colspan="1"  class="" style="width: 150px;">
                                                            <span class="zp_FG0Vx">
                                                                <div class="zp_Yfixs column-sort-container">
                                                                    <span class="zp_V7agI">Title</span>

                                                                </div>
                                                            </span>
                                                            <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1"  class="">
                                                            <span class="zp_v1FRc">
                                                                <span class="zp_FG0Vx">
                                                                    <div class="zp_Yfixs column-sort-container">
                                                                        <span class="zp_V7agI">Company</span>

                                                                    </div>
                                                                </span>
                                                            </span>
                                                            <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1"  class="">Quick Actions <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1"  class="">Contact Location <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1" class="">
                                                            <span class="zp_FG0Vx">
                                                                <div class="zp_Yfixs column-sort-container">
                                                                    <span class="zp_V7agI"># Employees</span>

                                                                </div>
                                                            </span>
                                                            <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1"  class="">
                                                            <span class="zp_FG0Vx">
                                                                <div class="zp_Yfixs column-sort-container">
                                                                    <span class="zp_V7agI">Phone</span>

                                                                </div>
                                                            </span>
                                                            <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1" class="">
                                                            <span class="zp_FG0Vx">
                                                                <div class="zp_Yfixs column-sort-container">
                                                                    <span class="zp_V7agI">Industry</span>

                                                                </div>
                                                            </span>
                                                            <div class="zp_cArSn"></div>
                                                        </th>
                                                        <th rowspan="1" colspan="1" class="">Keywords <div class="zp_cArSn"></div>
                                                        </th>
                                                    </tr>                                </thead>
                                                <tbody class=""  id="tbggg">

                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<style>


    .panel {
        border-width: 0 0 1px 0;
        border-style: solid;
        border-color: #fff;
        background: none;
        box-shadow: none;
    }

    .panel:last-child {
        border-bottom: none;
    }

    .panel-group > .panel:first-child .panel-heading {
        border-radius: 4px 4px 0 0;
    }

    .panel-group .panel {
        border-radius: 0;
    }

    .panel-group .panel + .panel {
        margin-top: 0;
    }

    .panel-heading {
        border-radius: 0;
        border: none;
        color: #1a1a1a;
        padding: 0;
    }

    .panel-title a {
        display: block;
        color: #1a1a1a;
        padding: 15px;
        position: relative;
        font-size: 16px;
        font-weight: 400;
    }

    .panel-body {
        background: #fff;
    }

    .panel:last-child .panel-body {
        border-radius: 0 0 4px 4px;
    }

    .panel:last-child .panel-heading {
        border-radius: 0 0 4px 4px;
        transition: border-radius 0.3s linear 0.2s;
    }

    .panel:last-child .panel-heading.active {
        border-radius: 0;
        transition: border-radius linear 0s;
    }
    /* #bs-collapse icon scale option */

    .panel-heading a:before {
        content: '\f0d8';
        position: absolute;
        font-family: 'Font Awesome 5 Free';
        right: 5px;
        top: 10px;
        font-size: 24px;
        transition: all 0.5s;
        transform: scale(1);
        font-weight: 900;
    }

    .panel-heading.active a:before {
        content: ' ';
        transition: all 0.5s;
        transform: scale(0);
    }

    #bs-collapse .panel-heading a:after {
        content: ' ';
        font-size: 24px;
        position: absolute;
        font-family: 'Font Awesome 5 Free';
        right: 5px;
        top: 10px;
        transform: scale(0);
        transition: all 0.5s;
        font-weight: 900;
    }

    #bs-collapse .panel-heading.active a:after {
        content: '\f0dd';
        transform: scale(1);
        transition: all 0.5s;
    }

    /* #accordion rotate icon option */

    #accordion .panel-heading a:before {
        content: '\f0d8';
        font-size: 24px;
        position: absolute;
        font-family: 'Font Awesome 5 Free';
        right: 5px;
        top: 10px;
        transform: rotate(180deg);
        transition: all 0.5s;
        font-weight: 900;
    }

    #accordion .panel-heading.active a:before {
        transform: rotate(0deg);
        transition: all 0.5s;
    }
    .apollo-colored-icon svg {
        height: 1em;
        width: 1em;
    }
    .zp_CLq57, .zp_INSAF {
        padding: 16px;
        min-width: 250px;
    }
    .zp_JywRU {
        display: flex;
        align-items: center;
    }
    .zp_t08Bv {
        font-size: 14px;
        font-weight: 600;
        line-height: 16px;
        color:#1a1a1a;
    }
    .zp_tDE3F {
        font-size: 12px;
        font-weight: 500;
        line-height: 16px;
    }
    .zp_DMnwE {
        display: flex;
        align-items: center;
    }
    .zp_doIaS {
        font-size: 12px;
        font-weight: 500;
        line-height: 16px;
        color: #474747;
    }.zp_Lesln {
        background-color: #cacacc;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        margin: 0 5px;
    }
    .zp_SxO7r {
        color: #3dcc85;
    }
    .zp_L4MB_ {
        padding: 14px;
        min-width: 250px;
    }
    .zp_EB03i {
        font-size: 12px;
        font-weight: 500;
        line-height: 16px;
        color:#474747;
    }
    .zp_M9ktd {
        display: flex;
        align-items: center;
    }
    .zp_oQHIq {
        font-size: 14px;
        font-weight: 600;
        line-height: 16px;
        color:#1a1a1a;
    }

    table .dropdown {
        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
        display: inline-block;
        text-align: left;
        border-radius: 2px 0 0 2px;
        border: 1px solid #cacacc;
    }
    .btn.btn-borderss {
        padding-left: 6px;
        padding-right: 6px;
        padding-top: 0;
        padding-bottom: 0;
        height: 32px;
    }
    div.dataTables_wrapper div.dataTables_info,div.dataTables_wrapper div.dataTables_paginate ul.pagination {

        font-size: 12px;
    }
</style>
@endsection
@section('js-footer')
<link href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css" rel="stylesheet" type="text/css">
<script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>

<link href="https://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css" rel="stylesheet">  
<!--<script src="https://code.jquery.com/jquery-1.10.2.js"></script>  -->
<script src="https://code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
<script>

                                                                 

</script>
<script src="{{url('assets/admin/js/contact-type.js')}}"></script>

<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
<style>

    table td {
        font-size: 12px;
        font-weight: 400;
        line-height: 16px;
        color: #1a1a1a;
        background: #fff;
        text-align: center;
        padding: 3px 10px !important;
        position: relative;
        white-space: nowrap;
    }
    table td:first-child {
        position: sticky;
        left: 0;
        z-index: 2;
        background-color: #fff;
    }
    table td:first-child,  table th:first-child {
        padding: 0 10px;
    }
    table td:first-child {
        box-shadow: 3px 0 3px rgba(0,0,0,.07);
        border-right: 1px solid var(--color-border-light);
        min-width: 200px;
        text-align: left;
        margin-top: 1px;
    }
    tbody tr:not(.zp_V6z_c) td {
        border-bottom: 1px solid #e3e3e5;
    }  

    td:first-child {
        box-shadow: 3px 0 3px rgba(0,0,0,.07) !important;
        border-right: 1px solid #cacaca !important;
    } 
    table th:first-child {
        border-top-left-radius: 4px;
        position: sticky !important;
        left: 0;
        top: 0;
        z-index: 3;
    }
    table th:first-child {
        text-align: left;
    }
    table th {
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .zp_G5KZB table .zp_rJZsu {
        display: flex;
        height: 100%;
        align-items: center;
    }
    .zp_FG0Vx {
        display: flex;
        align-items: center;
    }

    .zp_Yfixs {
        font-size: 12px;
        font-weight: 400;
        /* line-height: 16px; */
        line-height: inherit;
        color: #474747;
        display: flex;
        align-items: center;
    }
    .zp_oSeJs {
        cursor: inherit;
        width: 100%;
        position: relative;
    }
    .zp_oSeJs .zp_Ln9Ws {
        display: flex;
        margin: -5px -10px;
        padding: 5px 10px;
        position: relative;
    }
    .zp_DBwlj {
        line-height: 22px;
        padding-right: 38px;
    }
    .zp_oTOOy {
        display: flex;
        align-items: center;
        width: 100%;
    }

    .zp_oTOOy .zp_TvTJg {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        overflow: hidden;
    }.zp_oTOOy .zp_TvTJg {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        overflow: hidden;
    }
    .zp_oTOOy .zp_TvTJg .zp_WM8e5 {
        font-size: 16px;
        font-weight: 500;
        line-height: 24px;
        color: #0852c2;
        display: block;
        text-decoration: none;
        text-align: left;
        margin-right: 10px;
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .zp_I1ps2 {
        display: flex;
        flex-flow: row;
        align-items: center;
        height: 30px;
    }
    .zp_I1ps2 > :not(:last-child) {
        margin-right: 3px;
    }
    .zp_I1ps2 > :not(:last-child) {
        margin-right: 3px;
    }
    .zp_OotKe {
        cursor: pointer;
        font-weight: 400;
        color: #146ef6;
        text-decoration: none;
    }
    .zp_I1ps2 .zp-icon {
        font-size: 16px;
        color: #919191;
    } table th {
        font-size: 12px;
        font-weight: 400;
        /* line-height: 16px; */
        color: #474747;
        border-bottom: 1px solid #e3e3e5;
        padding: 0 10px !important;
        text-align: left;
        line-height: 30px;white-space: nowrap;
        border-top-left-radius: 4px;
        position: sticky;
        left: 0;
        top: 0;
        z-index: 3;
    }

    .vh-70{
        height: 70vh !important;
    }
    .vh-71{
        height: 71vh !important;
    }
    .zp_rJZsu {
        display: flex;
    }
    .tooltip-inner {
        background-color: #00cc00;
    }
    .tooltip.bs-tooltip-right .arrow:before {
        border-right-color: #00cc00 !important;
    }
    .tooltip.bs-tooltip-left .arrow:before {
        border-left-color: #00cc00 !important;
    }
    .tooltip.bs-tooltip-bottom .arrow:before {
        border-bottom-color: #00cc00 !important;
    }
    .tooltip.bs-tooltip-top .arrow:before {
        border-top-color: #00cc00 !important;
    }
    tbody td .zp_wdoJt {
        display: flex;
        align-items: center;
    }



    .zp_iJZr1 label {
        display: flex;
        align-items: flex-start;
    }
    .zp_iJMr1 {
        display: flex;
        flex-flow:  row;
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-3-typeahead/4.0.1/bootstrap3-typeahead.min.js"></script>
<script>

                                                                    $(document).ready(function () {
                                                                        $.ajaxSetup({
                                                                            headers: {
                                                                                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                                                                            }
                                                                        });

                                                                        $('#export_records').on('click', function (e) {
                                                                            var contacts = [];
                                                                            $(".contact_ids:checked").each(function () {
                                                                                contacts.push($(this).data('cid'));
                                                                            });
                                                                            if (contacts.length <= 0) {
                                                                                alert("Please select records.");
                                                                            } else {


                                                                                var selected_values = contacts;
                                                                                $.ajax({
                                                                                    cache: false,
                                                                                    type: "POST",
                                                                                    url: "{{route('admin.contacts.export')}}",
                                                                                    cache: false,
                                                                                    data: {
                                                                                        contacts_id: selected_values,
                                                                                        _token: requestToken
                                                                                    },
                                                                                    success: function (response) {
                                                                                        var a = document.createElement("a");
                                                                                        a.href = response.file;
                                                                                        a.download = response.name;
                                                                                        document.body.appendChild(a);
                                                                                        a.click();
                                                                                        a.remove();
//                    var disposition = xhr.getResponseHeader('content-disposition');
//                    var matches = /"([^"]*)"/.exec(disposition);
//                    var filename = (matches != null && matches[1] ? matches[1] : 'salary.xlsx');
//
//                    // The actual download
//                    var blob = new Blob([result], {
//                        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
//                    });
//                    var link = document.createElement('a');
//                    link.href = window.URL.createObjectURL(blob);
//                    link.download = filename;
//
//                    document.body.appendChild(link);
//
//                    link.click();
//                    document.body.removeChild(link);
                                                                                    },
                                                                                    error: function (ajaxContext) {
                                                                                        toastr.error('Export error: ' + ajaxContext.responseText);
                                                                                    }
                                                                                });
                                                                            }

                                                                        });

                                                                    });
                                                                    var download_limit = '<?php echo $download_limit; ?>';
                                                                    function toggleCheckboxes(source, cbName) {
                                                                        event.stopPropagation();
                                                                        var checkboxes = document.getElementsByName(cbName);

                                                                        if (download_limit == '-1') {
                                                                            download_limit = checkboxes.length;
                                                                        }


                                                                        for (var i = 0; i < download_limit; i++) {

                                                                            checkboxes[i].checked = source.checked;
                                                                        }
                                                                        if ($('.contact_ids:checked').length >= download_limit) {
                                                                            $(".contact_ids").not(":checked").attr("disabled", true);
                                                                        } else {
                                                                            $(".contact_ids").not(":checked").removeAttr('disabled');
                                                                        }



                                                                    }


                                                                    $(document).on('click', '.contact_ids', function () {
                                                                        if (download_limit != '-1') {

                                                                            if ($('.contact_ids:checked').length >= download_limit) {
                                                                                $(".contact_ids").not(":checked").attr("disabled", true);
                                                                            } else {
                                                                                $(".contact_ids").not(":checked").removeAttr('disabled');
                                                                            }
                                                                        }
                                                                    });

                                                                    var path = "{{ route('autocomplete') }}";

                                                                    $('input.typeahead').typeahead({

                                                                        source: function (query, process) {

                                                                            return $.get(path, {term: query}, function (data) {

                                                                                return process(data);

                                                                            });

                                                                        }

                                                                    });


$(document).ready(function() {
    $('.js-example-basic-single').select2(); // Initialize Select2
});



</script>

@endsection