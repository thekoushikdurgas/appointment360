<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Cache;

class ImportCsvJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $filePath;

    public function __construct($filePath)
    {
        $this->filePath = $filePath;
    }

    public function handle()
    {
        // MySQL import
        DB::connection()->getpdo()->exec("
            LOAD DATA LOCAL INFILE '" . $this->filePath . "'
            INTO TABLE contacts
            FIELDS TERMINATED BY ',' 
            OPTIONALLY ENCLOSED BY '\"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS
            (first_name,last_name,title,company,company_name_for_emails,email,email_status,primary_email_catch_all_status,seniority,departments,work_direct_phone,home_phone,mobile_phone,corporate_phone,other_phone,stage,employees,industry,keywords,person_linkedin_url,website,company_linkedin_url,facebook_url,twitter_url,city,state,country,company_address,company_city,company_state,company_country,company_phone,technologies,annual_revenue,total_funding,latest_funding,latest_funding_amount,last_raised_at)
        ");

        // Mark progress complete
        Cache::put('import_progress', Cache::get('import_total', 0));
    }
}
