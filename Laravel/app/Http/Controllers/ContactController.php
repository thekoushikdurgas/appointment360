<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Cache;

class ContactController extends Controller
{
    public function index(Request $request)
    {
        $perPage = 20;

        // Base query: select only required columns
        $query = DB::table('contacts_copy')
            ->select('id','first_name','last_name','email_status','title','industry','city','state','country','technologies','annual_revenue','person_linkedin_url');

        // -------------------------
        // Filters
        // -------------------------

        // Name search
        if ($request->filled('name')) {
            $name = trim($request->name);
            $query->where(function($q) use ($name) {
                $q->where('first_name', 'like', "%{$name}%")
                  ->orWhere('last_name', 'like', "%{$name}%");
            });
        }

        // Location filter (multi)
        if ($request->filled('location')) {
            $locations = (array) $request->location;
            $query->where(function($q) use ($locations) {
                foreach ($locations as $loc) {
                    $q->orWhere('city', 'like', "%{$loc}%")
                      ->orWhere('state', 'like', "%{$loc}%")
                      ->orWhere('country', 'like', "%{$loc}%");
                }
            });
        }

        // Industry filter (multi)
        if ($request->filled('industry')) {
            $industries = array_map('trim', $request->industry);
            $query->whereIn('industry', $industries);
        }

        // Job title (multi, comma-separated)
        if ($request->filled('job_title')) {
            $titles = (array) $request->job_title;
            $query->where(function($q) use ($titles) {
                foreach ($titles as $title) {
                    $q->orWhere('title', 'like', "%{$title}%");
                }
            });
        }

        // Technology (multi, comma-separated)
        if ($request->filled('technology')) {
            $techs = (array) $request->technology;
            $query->where(function($q) use ($techs) {
                foreach ($techs as $tech) {
                    $q->orWhere('technologies', 'like', "%{$tech}%");
                }
            });
        }

        // Employees range (checkboxes)
        if ($request->filled('employees')) {
            $ranges = (array) $request->employees;
            $query->where(function($q) use ($ranges) {
                foreach ($ranges as $range) {
                    if (strpos($range, '+') !== false) {
                        $min = (int) rtrim($range, '+');
                        $q->orWhere('employees', '>=', $min);
                    } elseif (strpos($range, '-') !== false) {
                        [$min, $max] = explode('-', $range);
                        $q->orWhereBetween('employees', [(int)$min, (int)$max]);
                    }
                }
            });
        }

        // Email status filter
        if ($request->filled('email_status')) {
            $statuses = (array) $request->email_status;
            $query->whereIn('email_status', $statuses);
        }

        // Revenue range
        if ($request->filled('min_rev')) {
            $query->where('annual_revenue', '>=', (float)$request->min_rev);
        }
        if ($request->filled('max_rev')) {
            $query->where('annual_revenue', '<=', (float)$request->max_rev);
        }

        // LinkedIn URL search
        if ($request->filled('linkedin')) {
            $kw = strtolower(trim($request->linkedin));
            $kw = preg_replace(['#^https?://#', '#^www\.#'], '', $kw);
            $kw = rtrim($kw, '/');

            $query->where('person_linkedin_url', 'like', "%{$kw}%");
        }

        // -------------------------
        // Pagination + Execution
        // -------------------------
        $contacts = $query->orderBy('id', 'desc')->paginate($perPage);

        // -------------------------
        // Total count (cached)
        // -------------------------
        $totalCount = Cache::remember('contacts_copy_total_count', 3600, function () {
            return DB::table('contacts_copy')->count();
        });

        // -------------------------
        // AJAX response (partial table)
        // -------------------------
        if ($request->ajax()) {
            return view('contact.partials.table', compact('contacts'))->render();
        }

        // -------------------------
        // Initial load: small sample lists
        // -------------------------
        $industryList = DB::table('dim_industry')
            ->select('tag_id','name')
            ->limit(200)
            ->get();

        return view('contact.index', compact('contacts','totalCount','industryList'));
    }

    // -------------------------
    // Select2 filter options endpoint
    // -------------------------
    public function filterOptions(Request $request)
    {
        $type = $request->get('type');
        $term = trim($request->get('term', ''));
        $id   = $request->get('id'); // prefill by ID
        $cacheKey = "filter_options_{$type}_" . md5($term . '_' . $id);

        return Cache::remember($cacheKey, 300, function () use ($type, $term, $id) {
            $results = collect();

            switch ($type) {
                case 'job_title':
                    $rows = DB::table('contacts_copy')
                        ->select('title')
                        ->when($term, fn($q) => $q->where('title', 'like', "%{$term}%"))
                        ->limit(200)
                        ->pluck('title');

                    $vals = $rows->flatMap(fn($s) => array_map('trim', array_filter(explode(',', $s))))
                                 ->unique()->values()->slice(0, 100);
                    $results = $vals->map(fn($v) => ['id' => $v, 'text' => $v]);
                    break;

                case 'technology':
                    $rows = DB::table('contacts_copy')
                        ->select('technologies')
                        ->when($term, fn($q) => $q->where('technologies', 'like', "%{$term}%"))
                        ->limit(200)
                        ->pluck('technologies');

                    $vals = $rows->flatMap(fn($s) => array_map('trim', array_filter(explode(',', $s))))
                                 ->unique()->values()->slice(0, 10000);
                    $results = $vals->map(fn($v) => ['id' => $v, 'text' => $v]);
                    break;

                case 'industry':
                    $query = DB::table('dim_industry')->select('tag_id as id', 'name as text');
                    if ($id) $query->whereIn('tag_id', (array)$id);
                    elseif ($term) $query->where('name', 'like', "%{$term}%");
                    $results = $query->get()->map(fn($r) => ['id' => $r->text, 'text' => $r->text]);
                    break;

                case 'company':
                    $rows = DB::table('contacts_copy')
                        ->select('company')
                        ->when($term, fn($q) => $q->where('company', 'like', "%{$term}%"))
                        ->groupBy('company')
                        ->limit(50)
                        ->pluck('company');
                    $results = $rows->map(fn($v) => ['id' => $v, 'text' => $v]);
                    break;

                case 'location':
                    $rows = DB::table('contacts_copy')
                        ->select(DB::raw("DISTINCT TRIM(CONCAT_WS(', ', NULLIF(city, ''), NULLIF(state, ''), NULLIF(country, ''))) as loc"))
                        ->when($term, fn($q) => $q->whereRaw("CONCAT_WS(', ', city, state, country) LIKE ?", ["%{$term}%"]))
                        ->limit(100)
                        ->pluck('loc');
                    $results = $rows->map(fn($v) => ['id' => $v, 'text' => $v]);
                    break;

                default:
                    $results = collect();
            }

            return response()->json(['results' => $results->values()]);
        });
    }
}
