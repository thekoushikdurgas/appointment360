<?php

namespace App\Http\Controllers\Admin;

use App\Helper\UploadFile;
use App\Http\Controllers\Controller;
use App\Http\Requests\Admin\ContactsCreateRequest;
use App\Models\Contacts;
use Maatwebsite\Excel\Facades\Excel;
use App\Imports\ContactsImport;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Str;
use DataTables;
use Yajra\DataTables\Html\Builder;
use App\Exports\ContactsExport;
use App\Models\Industry;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

use Aws\S3\S3Client;
use App\Jobs\ProcessLargeCSVJob;

class ContactsController extends Controller {


    use UploadFile;

    /**
     * @name index
     * 
     */
    function checkOnline($domain) {
        $curlInit = curl_init($domain);
        curl_setopt($curlInit, CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($curlInit, CURLOPT_HEADER, true);
        curl_setopt($curlInit, CURLOPT_NOBODY, true);
        curl_setopt($curlInit, CURLOPT_RETURNTRANSFER, true);

        //get answer
        $response = curl_exec($curlInit);

        curl_close($curlInit);
        if ($response)
            return true;
        return false;
    }

    public function index(Request $request) {
		
		  $searchQuery = $request->input('global_search'); // Access the 'query' input field
        $fragment = parse_url($searchQuery, PHP_URL_FRAGMENT);

// Split at '?'
        $parts = explode('?', $fragment, 2);
        $queryString = $parts[1] ?? '';

// Parse query string into array
        parse_str($queryString, $filters);
        $columns = \DB::getSchemaBuilder()->getColumnListing('contacts');
        $contactList = Contacts::get();
        $industryList = Industry::get();
        $job_titles_list = \DB::table('contacts')
                        ->select('title')
                        ->distinct()->get();
        //dd($job_titles_list);

        $totalRecords = Contacts::count();
        unset($columns[0]);
        unset($columns[49]);
        unset($columns[50]);
        unset($columns[51]);
        return view('admin.contacts.view', compact('columns', 'contactList', 'totalRecords', 'job_titles_list','filters','industryList'));
    }

    public function ajaxTableData(Request $request) {
        ini_set('max_execution_time', 300); // 5 minutes
        $contact = Contacts::query();

// Collect all filters safely
$contactEmailStatusV2 = $request->contactEmailStatusV2 ?? [];
$employess_range = $request->employess_range ?? [];
$search_location = $request->search_location ?? '';
$name_search = $request->name_search ?? '';
$js_industry = $request->js_industry ?? [];
$js_technologies = $request->js_technologies ?? [];
$job_titles = $request->job_titles ?? [];
$js_company = $request->js_company ?? [];
$search_linkedin = $request->search_linkedin ?? '';
$min_rev = $request->min_rev ?? '';
$max_rev = $request->max_rev ?? '';

// 🧠 Group all filters inside one big where() closure
$contact->where(function ($query) use (
    $contactEmailStatusV2, 
    $employess_range, 
    $search_location, 
    $name_search, 
    $js_industry, 
    $js_technologies, 
    $job_titles, 
    $js_company, 
    $search_linkedin,
    $min_rev,
    $max_rev
) {

    // 🔹 Name search
    if (!empty($name_search)) {
        $query->where(function ($q) use ($name_search) {
            $q->where('first_name', 'LIKE', "%{$name_search}%")
              ->orWhere('last_name', 'LIKE', "%{$name_search}%");
        });
    }

    // 🔹 Location (exact match, case-insensitive)
    if (!empty($search_location)) {
        $kw = strtolower(urldecode(trim($search_location)));
        $query->where(function ($q) use ($kw) {
            $q->whereRaw('LOWER(city) = ?', [$kw])
              ->orWhereRaw('LOWER(state) = ?', [$kw])
              ->orWhereRaw('LOWER(country) = ?', [$kw]);
        });
    }

    // 🔹 Job titles
    if (!empty($job_titles)) {
        $query->where(function ($q) use ($job_titles) {
            foreach ($job_titles as $term) {
                $kw = strtolower($term);
                $q->orWhereRaw('LOWER(title) LIKE ?', ['%' . $kw . '%']);
            }
        });
    }

    // 🔹 LinkedIn URL
    if (!empty($search_linkedin)) {
        $kw = strtolower(trim($search_linkedin));
        $kw = preg_replace(['#^https?://#', '#^www\.#'], '', $kw);
        $kw = rtrim($kw, '/');

        $query->where(function ($q) use ($kw) {
            $q->orWhereRaw("
                LOWER(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(person_linkedin_url, 'https://', ''),
                            'http://', ''),
                        'www.', ''),
                    '/','')
                ) LIKE ?
            ", ['%' . str_replace('/', '', $kw) . '%']);
        });
    }

    // 🔹 Technologies
    if (!empty($js_technologies)) {
        $query->where(function ($q) use ($js_technologies) {
            foreach ($js_technologies as $term) {
                $q->orWhereRaw('LOWER(technologies) LIKE ?', ['%' . strtolower($term) . '%']);
            }
        });
    }

    // 🔹 Industry
    if (!empty($js_industry)) {
        $query->where(function ($q) use ($js_industry) {
            foreach ($js_industry as $term) {
                $kw = strtolower(urldecode(trim($term)));
                $q->orWhereRaw('LOWER(industry) LIKE ?', ['%' . $kw . '%']);
            }
        });
    }

    // 🔹 Company
    if (!empty($js_company)) {
        $query->where(function ($q) use ($js_company) {
            foreach ($js_company as $term) {
                $q->orWhereRaw('LOWER(company) LIKE ?', ['%' . strtolower($term) . '%']);
            }
        });
    }

    // 🔹 Email status
    if (!empty($contactEmailStatusV2)) {
        $statuses = is_array($contactEmailStatusV2) ? $contactEmailStatusV2 : [$contactEmailStatusV2];
        $query->where(function ($q) use ($statuses) {
            foreach ($statuses as $status) {
                $q->orWhereRaw('LOWER(email_status) LIKE ?', ['%' . strtolower($status) . '%']);
            }
        });
    }

    // 🔹 Employees range
    if (!empty($employess_range)) {
        $employess_ranges = is_array($employess_range) ? $employess_range : [$employess_range];
        $query->where(function ($q) use ($employess_ranges) {
            foreach ($employess_ranges as $range) {
                $termarray = explode('-', $range);
                if ($termarray[0] != "10001") {
                    $q->orWhere(function ($sub) use ($termarray) {
                        $sub->where('employees', '>=', $termarray[0])
                            ->where('employees', '<=', $termarray[1]);
                    });
                } else {
                    $q->orWhere('employees', '>=', $termarray[0]);
                }
            }
        });
    }

    // 🔹 Revenue range
    if (!empty($max_rev) || !empty($min_rev)) {
        $min = $min_rev ?: 0;
        $max = $max_rev ?: 999999999;
        $query->whereBetween('annual_revenue', [$min, $max]);
    }
});

// ✅ Finally get data
$contactList = $contact->get();

        $totalRecords = Contacts::count();
        $fileteredRecords = $contact->count();
				
        return Datatables::of($contactList)
                        ->addColumn('name', function($contact) {
                            $html_name = '<div class="zp_C2NRr zp_wdoJt">
                                <div class="zp_iJZr1" style="margin-right: 7px;"><label class=""> <input type="checkbox" name="contact_ids" class="contact_ids" value="' . $contact->id . '" data-cid="' . $contact->id . '" aria-label="Checkbox for following text input">
    
</label></div>
<div><div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I"><div class="zp_Ln9Ws EditTarget"><div class="zp_DBwlj">
                                                                <div class="zp_LDJHm"><div class="zp_BC5Bd">
                                                                        <div class="zp_xVJ20">
                                                                            <span>
                                                                                <a href="#" style="">' . $contact->first_name . ' ' . $contact->last_name . '  </a>
                                                                            </span>
                                                                        </div>
                                                                    </div>
                                                                    <div class="zp_I1ps2">
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="'. $contact->person_linkedin_url . '" target="_blank">
                                                                                <i class="fab fa-linkedin-in"></i>
                                                                            </a>
                                                                        </span>

                                                                    </div>
                                                                </div>
                                                            </div>
                                                           
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>';
                            return $html_name;
                        })
                        ->editColumn('title', function($contact) {
                            $html = '  <div>
                                                <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="zp_Y6y8d">' . $contact->title . '</span>
                                                        </div>
                                                       
                                                    </div>
                                                </div>
                                            </div>';
                            return $html;
                        })
                        ->editColumn('company', function($contact) {
                            $website = $contact->website;
                            $company_favicon = '';
//                            $website = "http://www.fullyloaded.tech";
//                            $headerweb = get_headers($website);
//                            dd($headerweb );
//                            if($website !='http://www.fullyloaded.tech' && $website !='http://www.optionsgroup.com'){
//                            $headerweb = get_headers($website);
//                            $string = $headerweb[0];
//                            
//                            if(strpos($string,"200")){
//                                //$website = "http://www.fullyloaded.techv";
//                                $path = $website . "/favicon.ico";
//                                
//                                $header = get_headers($path);
//                               // dd($header);
//                                if (preg_match("|200|", $header[0])) {
//                                    $company_favicon = '<img width="35" height="auto" style="border-radius: 5px;" src="' . $path . '" alt="Company logo">';
//                                } else {
//                                    $company_favicon = '';
//                                }
//                            
//                            }
//                            }

                            $html = ' <div><div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="intentDataBars zp_oTOOy">
                                                                <span style="cursor: pointer;" class="zp_IL7J9"><div class="" style="width: 35px; height: auto; max-height: 35px; border-radius: 5px;">' . $company_favicon . '</div></span>
                                                                <div class="zp_TvTJg">
                                                                    <div class="zp_J1j17">
                                                                        <a class="zp_WM8e5 zp_kTaD7" href="#">' . $contact->company . '</a>
                                                                    </div>
                                                                    <div class="zp_I1ps2">
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="' . $contact->website . '" target="_blank">
                                                                                <i class="fas fa-link"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="' . $contact->company_linkedin_url . '" target="_blank">
                                                                                <i class="fab fa-linkedin-in"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="' . $contact->facebook_url . '" target="_blank">
                                                                                <i class="fab fa-facebook-f"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="' . $contact->twitter_url . '" target="_blank">
                                                                                <i class="fab fa-twitter"></i>
                                                                            </a>
                                                                        </span>
                                                                    </div>
                                                                </div>
                                                            </span>
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                            </div>';
                            return $html;
                        })
                        ->addColumn('quick_actions', function($contact) {
                            $email_verfied = $contact->email_status;
                            //mail
                            $html = '<div class="dropdown">
  ';
                            if (strtolower($email_verfied) == strtolower('Verified')) {
                                $html .= '<button class="btn btn-borderss dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="false">
    <i class="zp-icon apollo-icon apollo-colored-icon zp_dZ0gM zp_j49HX zp_uAV5p"><svg viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><g>
    <path d="M12.1 5.246H2.903a1.97 1.97 0 0 0-1.97 1.971v6.57a1.97 1.97 0 0 0 1.97 1.97H12.1a1.97 1.97 0 0 0 1.971-1.97v-6.57a1.97 1.97 0 0 0-1.97-1.97Zm-.269 1.314-3.863 3.863a.656.656 0 0 1-.933 0L3.172 6.56h8.659Zm.926 7.227a.657.657 0 0 1-.657.656H2.903a.657.657 0 0 1-.657-.656v-6.3l3.863 3.862a1.97 1.97 0 0 0 2.785 0l3.863-3.863v6.3Z" fill="#5D6A7E"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5.5a5.5 5.5 0 1 1 11 0 5.5 5.5 0 0 1-11 0Z" fill="#02C797" class="no-cascade"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M15.196 3.04a.8.8 0 0 1 .17 1.12L12.9 7.517a1.067 1.067 0 0 1-1.67.062L9.672 5.761a.8.8 0 1 1 1.215-1.04l1.121 1.308 2.07-2.817a.8.8 0 0 1 1.119-.171Z" fill="#fff" class="no-cascade"></path></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h18v18H0z"></path></clipPath></defs></svg>';

                                $html .= '</i></button>
  <div class="dropdown-menu">
    <div class="zp_CLq57"><div class="zp_JywRU"><span class="zp_t08Bv">' . $contact->email . '</span></div><div class="zp_tDE3F zp_SxO7r">Email is Verified</div><div class="zp_DMnwE"><span class="zp_doIaS">Business</span><span class="zp_Lesln"></span><span class="zp_doIaS">Primary</span></div><div><div class="zp_JywRU zp_TSgUi"><span class="zp_t08Bv">nutac120@me.com</span></div><div class="zp_tDE3F zp_SxO7r">Email is Verified</div><span class="zp_doIaS">Personal</span></div><div class="zp_YTbTa zp_QHPEX"></div></div>
  </div>
</div>';
                            } else {
                                $html .= '<button class="btn btn-borderss" type="button" data-toggle="" aria-expanded="false">
    <i class="zp-icon apollo-icon apollo-colored-icon zp_dZ0gM zp_j49HX zp_uAV5p"><svg viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_583_20927)"><path d="M12.1004 5.73663H2.90307C2.38037 5.73663 1.87908 5.94428 1.50947 6.31388C1.13986 6.68349 0.93222 7.18478 0.93222 7.70748V14.277C0.93222 14.7997 1.13986 15.301 1.50947 15.6706C1.87908 16.0402 2.38037 16.2478 2.90307 16.2478H12.1004C12.6231 16.2478 13.1244 16.0402 13.494 15.6706C13.8636 15.301 14.0712 14.7997 14.0712 14.277V7.70748C14.0712 7.18478 13.8636 6.68349 13.494 6.31388C13.1244 5.94428 12.6231 5.73663 12.1004 5.73663ZM11.831 7.05053L7.96816 10.9134C7.90709 10.975 7.83443 11.0239 7.75437 11.0572C7.67432 11.0906 7.58845 11.1077 7.50172 11.1077C7.415 11.1077 7.32913 11.0906 7.24908 11.0572C7.16902 11.0239 7.09636 10.975 7.03529 10.9134L3.17242 7.05053H11.831ZM12.7573 14.277C12.7573 14.4512 12.6881 14.6183 12.5649 14.7415C12.4417 14.8647 12.2746 14.9339 12.1004 14.9339H2.90307C2.72884 14.9339 2.56174 14.8647 2.43854 14.7415C2.31534 14.6183 2.24612 14.4512 2.24612 14.277V7.97683L6.10899 11.8397C6.47852 12.2088 6.97945 12.4161 7.50172 12.4161C8.024 12.4161 8.52492 12.2088 8.89446 11.8397L12.7573 7.97683V14.277Z" fill="#5D6A7E"></path><path d="M7 5.99048C7 2.95291 9.46243 0.490479 12.5 0.490479C15.5376 0.490479 18 2.95291 18 5.99048C18 9.02804 15.5376 11.4905 12.5 11.4905C9.46243 11.4905 7 9.02804 7 5.99048Z" fill="#EC4D2E" class="no-cascade"></path><g clip-path="url(#clip1_583_20927)"><path d="M13.3018 3.42915C13.3018 2.98732 12.9437 2.62915 12.5018 2.62915C12.06 2.62915 11.7018 2.98732 11.7018 3.42915L11.7018 6.4526C11.7018 6.89443 12.06 7.2526 12.5018 7.2526C12.9437 7.2526 13.3018 6.89443 13.3018 6.4526L13.3018 3.42915Z" fill="white" class="no-cascade"></path><path d="M12.5 9.47368C12.9409 9.47368 13.2983 9.11628 13.2983 8.6754C13.2983 8.23452 12.9409 7.87712 12.5 7.87712C12.0592 7.87712 11.7018 8.23452 11.7018 8.6754C11.7018 9.11628 12.0592 9.47368 12.5 9.47368Z" fill="white" class="no-cascade"></path></g></g><defs><clipPath id="clip0_583_20927"><rect width="18" height="18" fill="white" transform="translate(0 0.490479)"></rect></clipPath><clipPath id="clip1_583_20927"><rect width="8" height="8" fill="white" transform="translate(8.49994 1.99048)"></rect></clipPath></defs></svg>';

                                $html .= '</i></button>';
                            }

                            //phone
                            $html .= '<div class="dropdown">
  <button class="btn btn-borderss dropdown-toggle" type="button" data-toggle="dropdown" aria-expanded="false">
 <i class="fas fa-phone-alt" style="font-size: 12px;"></i> </button>
  <div class="dropdown-menu">
    <div class="zp_L4MB_">
        <span class="zp_EB03i">HQ Number</span>
        <div><div class="zp_M9ktd"><span class="zp_oQHIq">' . $contact->corporate_phone . '</span></div><div>
    </div></div>
</div>';
                            return $html;
                        })
                        ->addColumn('contact_location', function($contact) {
                            $html = '<div>
                                                <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="zp_Y6y8d">' . $contact->city . ' , ' . $contact->country . '</span>
                                                        </div>
                                                        
                                                    </div>
                                                </div>
                                            </div>';
                            return $html;
                        })
                        ->addColumn('no_employees', function($contact) {
                            $html = '<span class="zp_Y6y8d">' . $contact->employees . '</span>';
                            return $html;
                        })
                        ->addColumn('phone', function($contact) {
                            $html = '<span class="zp_Y6y8d">' . $contact->corporate_phone . '</span>';
                            return $html;
                        })
                        ->editColumn('industry', function($contact) {
                            $html = '<span class="zp_PHqgZ zp_TNdhR">' . $contact->industry . '</span>';
                            return $html;
                        })
                        ->editColumn('keywords', function($contact) {
                             $keywordArray = substr($contact->keywords, 0, 15);
                            $html = '<span class="zp_yc3J_ zp_FY2eJ tooltip-zp" title="' . $contact->keywords . '">' . $keywordArray . '...</span>';
                            return $html;
                        })
//                        
                        ->rawColumns(['checkbox', 'name', 'title', 'company', 'quick_actions', 'contact_location', 'no_employees', 'phone', 'industry', 'keywords'])
                        ->only(['checkbox', 'name', 'title', 'company', 'quick_actions', 'contact_location', 'no_employees', 'phone', 'industry', 'keywords'])
                        ->toJson();
        $data = [
            'recordsTotal' => $totalRecords,
            'recordsFiltered' => $fileteredRecords,
            'data' => $contactList,
        ];
        //return response()->json($data, 200);
        // return view('admin.contacts.ajax-datatable', compact('contactList'));
    }

    public function ajaxData(Request $request) {
        $search_keyword = $request->search_keyword;
        $search_column = $request->search_column;
        $contact = Contacts::query();
        $data = array();
        $contact = $contact->where($search_column, 'LIKE', "%{$search_keyword}%")->select($search_column, 'id')
                        ->distinct()->take(10)
                        ->get()->toArray();

        if ($search_column == 'technologies') {

            foreach ($contact as $contactArray) {
                $contactSingleArray = explode(",", $contactArray['technologies']);
                foreach ($contactSingleArray as $keysValues) {
                    $keysValues = ltrim($keysValues);
                    if ($keysValues != ' ') {
                        if (str_contains(strtolower($keysValues), strtolower($search_keyword))) {
                            $data[] = $keysValues;
                        }
                    }
                }
            }
           $data= array_unique($data);
        } 
        else 
        if ($search_column == 'keywords') {

            foreach ($contact as $contactArray) {
                $contactSingleArray = explode(",", $contactArray['keywords']);
                foreach ($contactSingleArray as $keysValues) {
                    $keysValues = ltrim($keysValues);
                    if ($keysValues != ' ') {
                        if (str_contains(strtolower($keysValues), strtolower($search_keyword))) {
                            $data[] = $keysValues;
                        }
                    }
                }
            }
           $data= array_unique($data);
        }
        else {
            $data = $contact;
        }
        //dd($data);
        // 
        return response()->json($data, 200);
    }

    /**
     * @name ajaxTableData
     * 
     * Return datatable ajax data 
     */
//    public function ajaxTableData(Request $request) {
//        $orderColumns = [
//            'id',
//            'first_name',
//            '',
//            'title',
//            'company',
//        ];
//        $totalRecords = Contacts::count();
//        $contact = Contacts::query();
//
//        if ($request->has('search')) {
//            $search = $request->get('search');
//            if (!empty($search['value'])) {
//
//                $contact = $contact->allColumnFilter($search['value']);
//            }
//        }
//
//        $fileteredRecords = $contact->count();
//
//        if ($request->has('order')) {
//            $order = $request->get('order')[0];
//            $contact = $contact->orderBy($orderColumns[$order['column']], $order['dir']);
//        }
//        $contact = $contact->latest()
//                ->take($request->get('length', 50))
//                ->skip($request->get('start', 0))
//                ->get();
//
//        //dd($contact);
//
//        $data = [
//            'recordsTotal' => $totalRecords,
//            'recordsFiltered' => $fileteredRecords,
//            'data' => $contact,
//        ];
//        return response()->json($data, 200);
//    }

    /**
     * @name create
     * 
     */
    public function create(Contacts $contact) {

        $columns = \DB::getSchemaBuilder()->getColumnListing('contacts');

        unset($columns[0]);
        unset($columns[49]);
        unset($columns[50]);
        unset($columns[51]);


        return view('admin.contacts.create', compact('contact', 'columns'));
    }

    public function import_contacts(Contacts $contact) {
        return view('admin.contacts.import_contacts', compact('contact'));
    }

    /**
     * @name edit
     * 
     */
    public function edit(Contact $contact) {
        return view('admin.contacts.create', compact('contact'));
    }

    /**
     * @name store
     * 
     */
    public function store(ContactsCreateRequest $request) {
        $messageKey = 'success-message';
        $message = '';
        if ($request->has('id')) {
            $contact = Contacts::find($request->get('id'));
            $message = 'contacts has been updated successfully.';
        } else {
            $contact = new Contacts;
            $message = 'contacts has been created successfully.';
        }

        // $parcelType->user_id = auth()->id();
//            $contact->first_name = $request->get('first_name');
//            $contact->title = $request->get('title');
//            $contact->last_name = $request->get('last_name');
//            $contact->company = $request->get('company');
//            $contact->save();
        $contact = Contacts::create($request->except('_token'));
        return redirect()->back()->with($messageKey, $message);
    }

    /**
     * @name delete
     * 
     * Remove Parcel Type complete
     * 
     */
    public function delete(Contacts $contact) {
        $contact->delete();
        $data = [
            'message' => 'Success ! Contact has been removed.'
        ];
        return response()->json($data, 200);
    }

//public function upload(Request $request)
//    {
//        request()->validate([
//            'users' => 'required|mimes:xlx,xls|max:2048'
//        ]);
//        
//                
//        Excel::import(new ContactsImport, $request->file('users'), \Maatwebsite\Excel\Excel::CSV);
//
//
//        return back()->with('massage', 'Contatcs Imported Successfully');
//    }
 
 public function upload(Request $request)
{
	 $request->validate([
        'users' => 'required|file|mimes:csv,txt',
    ]);

    $file = $request->file('users');

    // Queue import (avoid HTTP timeout)
    Excel::queueImport(new ContactsImport, $file);

    return response()->json([
        'message' => 'Import started successfully. It may take some time for huge CSVs.',
    ]);
} 
/*
    if (!$request->hasFile('users')) {
        return "please upload csv file";
    }

    $path = $request->file('users')->getRealPath();
    $header = null;
    $batchSize = 1000;
    $data = [];

    if (($handle = fopen($path, 'r')) !== false) {
        while (($row = fgetcsv($handle, 10000, ',')) !== false) {
            if (!$header) {
                $header = array_map('strtolower', $row);
                continue;
            }

            if (count($row) == count($header)) {
                $clean = array_combine($header, $row);
                $data[] = $clean;
            }

            if (count($data) >= $batchSize) {
                Contacts::insert($data); // single query for 1000 records
                $data = [];
            }
        }

        if (count($data)) {
            Contacts::insert($data);
        }
        fclose($handle);
    }
    return redirect()->back()->with('success-message', 'Success! Contacts imported.');
}
/*

    public function search_form(Request $request) {
        $search_keyword = $request->search_keyword;
        $search_column = $request->search_column;

        $orderColumns = [
            'id',
            'first_name',
            '',
            'title',
            'company',
        ];
        $totalRecords = Contacts::count();
        $contact = Contacts::query();

        if ($request->has('search')) {
            $search = $request->get('search');
            if (!empty($search['value'])) {

                $contact = $contact->allColumnFilter($search['value']);
            }
        }

        $fileteredRecords = $contact->count();

        if ($request->has('order')) {
            $order = $request->get('order')[0];
            $contact = $contact->orderBy($orderColumns[$order['column']], $order['dir']);
        }
        $contact = $contact->where($search_column, 'LIKE', "%{$search_keyword}%")
                ->take($request->get('length', 50))
                ->skip($request->get('start', 0))
                ->get();

        //dd($contact);

        $data = [
            'recordsTotal' => $totalRecords,
            'recordsFiltered' => $fileteredRecords,
            'data' => $contact,
        ];
        return response()->json($data, 200);
    }

   

    public function export_contact(Request $request) {
        $contacts_id = $request->contacts_id;
        $AuthuserColumnAllowed = auth()->user()->id;
        $data = Contacts::whereIn('id', $contacts_id)->get();
        $myFile = Excel::raw(new ContactsExport($contacts_id), 'Xlsx');

        $response = array(
            'name' => "contacts_".strtotime(date("Y-m-d H:i")). ".xlsx",
            'file' => "data:application/vnd.ms-excel;base64," . base64_encode($myFile)
        );
        return response()->json($response);
        //return Excel::download($data, 'projets'. date('Y-m-d') . '.xlsx');
//$myFile = $myFile->string('xlsx'); //change xlsx for the format you want, default is xls
//$response =  array(
//   'name' => "filename", //no extention needed
//   'file' => "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,".base64_encode($myFile) //mime type of used format
//);
//return response()->json($response);
//    $response =  array(
//        'name' => "Pending-Task-List.xlsx",
//        'file' => "data:application/vnd.ms-excel;base64,".base64_encode($myFile)
//     );
//     return response()->json($response);
        // fpassthru($f);
        // return response()->stream($callback, 200, $headers);
        exit();

        //  return Response::stream($callback, 200, $headers);
        //return Response::stream($callback, 200, $headers);
    }

    /**

     * Show the form for creating a new resource.

     *

     * @return \Illuminate\Http\Response

     */
    public function autocomplete(Request $request) {

        $hasil = Contacts::select("annual_revenue")
                ->where("annual_revenue", "LIKE", "%{$request->term}%")
                ->get();
        $data = array();
        foreach ($hasil as $hsl) {
            $data[] = $hsl->annual_revenue;
        }

        array_unique($data);

        return response()->json($data);
    }
	
	public function importContacts(Request $request){
	
	 $request->validate(['csv_file' => 'required|mimes:csv,txt|max:512000']); // max 500 MB

        $file = $request->file('csv_file');
        $filename = 'uploads/' . Str::uuid() . '.csv';

        // S3 client
        $s3 = new S3Client([
            'version' => 'latest',
            'region'  => env('AWS_DEFAULT_REGION'),
            'credentials' => [
                'key'    => env('AWS_ACCESS_KEY_ID'),
                'secret' => env('AWS_SECRET_ACCESS_KEY'),
            ],
        ]);

        // Upload file to S3
        $s3->putObject([
            'Bucket' => env('AWS_BUCKET'),
            'Key'    => $filename,
            'SourceFile' => $file->getRealPath(),
        ]);

        // Dispatch background job
        ProcessLargeCSVJob::dispatch($filename);

        return back()->with('success', 'File uploaded to S3. Import job started.');
		}
/*public function importContacts(Request $request)
{
    $request->validate([
        'csv_file' => 'required|file|mimes:csv,txt',
    ]);

    $file = $request->file('csv_file');
    $path = $file->storeAs('uploads', 'contacts.csv');
    $fullPath = storage_path('app/' . $path);
	chmod($fullPath, 0775);

    // Optional: estimate total rows (for progress bar)
    $totalRows = 5000000; // approximate value for progress bar
    Cache::put('import_progress', 0);
    Cache::put('import_total', $totalRows);

    // Dispatch queue job
    \App\Jobs\ImportCsvJob::dispatch($fullPath);

    return response()->json([
        'message' => 'CSV uploaded successfully. Import started.',
    ]);
}*/
    public function importProgress()
    {
        $progress = Cache::get('import_progress', 0);
        $total = Cache::get('import_total', 1); // avoid divide by zero
        return response()->json([
            'progress' => $progress,
            'total' => $total
        ]);
    }

}
