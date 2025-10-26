<ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled" id="accordionSidebar">

    <!-- Sidebar - Brand -->
    <a class="sidebar-brand d-flex align-items-center justify-content-center" href="{{route('admin.index')}}">
        <div class="sidebar-brand-icon rotate-n-15">
            <i class="fas fa-laugh-wink"></i>
        </div>
        <div class="sidebar-brand-text mx-3">SB Admin <sup>2</sup></div>
    </a>

    <!-- Divider -->
    <hr class="sidebar-divider my-0">

    <!-- Nav Item - Dashboard -->
    <li class="nav-item dashboard-menu-link">
        <a class="nav-link" href="{{route('admin.index')}}">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span></a>
    </li>
<!--    <li class="nav-item parcel-type-menu-link">
        <a class="nav-link" href="{{route('admin.parcel_type')}}">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Parcel Type</span></a>
    </li>-->
<?php 
$Authuser = auth()->user();
         if( !is_null( $Authuser ) ){
             if($Authuser->role==1){
             ?>
        
<li class="nav-item parcel-type-menu-link">
        <a class="nav-link" href="{{route('user_list')}}">
            <i class="fas fa-fw fa-users"></i>
            <span>Users</span></a>
    </li>
             <?php } ?>
<li class="nav-item parcel-type-menu-link">
        <a class="nav-link" href="{{route('admin.contacts')}}">
            <i class="fas fa-fw fa-address-book"></i>
            <span>Contacts</span></a>
    </li>
             <?php } ?>
    <!-- Divider -->
    <hr class="sidebar-divider d-none">

    <!-- Heading -->
    <div class="sidebar-heading d-none">
        Interface
    </div>

    <!-- Nav Item - Pages Collapse Menu -->
    <li class="nav-item d-none">
        <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo"
            aria-expanded="true" aria-controls="collapseTwo">
            <i class="fas fa-fw fa-cog"></i>
            <span>Components</span>
        </a>
        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
            <div class="bg-white py-2 collapse-inner rounded">
                <h6 class="collapse-header">Custom Components:</h6>
                <a class="collapse-item" href="buttons.html">Buttons</a>
                <a class="collapse-item" href="cards.html">Cards</a>
            </div>
        </div>
    </li>

    <!-- Divider -->
    <hr class="sidebar-divider d-none d-md-block">

    <!-- Sidebar Toggler (Sidebar) -->
    <div class="text-center d-none d-md-inline">
        <button class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>

</ul>