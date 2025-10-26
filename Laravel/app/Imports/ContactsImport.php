<?php

namespace App\Imports;

use App\Models\Contacts;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Support\Facades\Cache;
use Maatwebsite\Excel\Concerns\ToModel;
use Maatwebsite\Excel\Concerns\WithChunkReading;
use Maatwebsite\Excel\Concerns\WithBatchInserts;
use Maatwebsite\Excel\Concerns\WithHeadingRow;
use Maatwebsite\Excel\Concerns\WithEvents;
use Maatwebsite\Excel\Events\BeforeImport;
use Maatwebsite\Excel\Events\AfterImport;
use Maatwebsite\Excel\Events\AfterSheet;


class ContactsImport implements ToModel, WithChunkReading, WithBatchInserts, WithHeadingRow, ShouldQueue, WithEvents{
 public function registerEvents(): array
{
    return [
        BeforeImport::class => function(BeforeImport $event) {
            Cache::put('import_progress', 0);

            // Try to get total rows
            $totalRows = $event->getReader()->getTotalRows()['Sheet1'] ?? null;

            if(!$totalRows) {
                // If total rows cannot be detected, set a default (or estimate)
                $totalRows = 1000000; // change based on expected CSV
            }

            Cache::put('import_total', $totalRows);
        },
        AfterImport::class => function(AfterImport $event) {
            Cache::put('import_progress', Cache::get('import_total', 0));
        },
    ];
}

    public function model(array $row)
    {
		 $progress = Cache::get('import_progress', 0);
        Cache::put('import_progress', $progress + 1);
        return new Contacts([
            'first_name' => $row['first_name'] ?? null,
            'last_name' => $row['last_name'] ?? null,
            'title' => $row['title'] ?? null,
            'company' => $row['company'] ?? null,
            'company_name_for_email' => $row['company_name_for_email'] ?? null,
            'email' => $row['email'] ?? null,
            'email_status' => $row['email_status'] ?? null,
            'primary_email_catch_all_status' => $row['primary_email_catch_all_status'] ?? null,
            'seniority' => $row['seniority'] ?? null,
            'departments' => $row['departments'] ?? null,
            'first_phone' => $row['first_phone'] ?? null,
            'work_direct_phone' => $row['work_direct_phone'] ?? null,
            'home_phone' => $row['home_phone'] ?? null,
            'mobile_phone' => $row['mobile_phone'] ?? null,
            'corporate_phone' => $row['corporate_phone'] ?? null,
            'stage' => $row['stage'] ?? null,
            'employees' => $row['employees'] ?? null,
            'industry' => $row['industry'] ?? null,
            'keywords' => $row['keywords'] ?? null,
            'person_linkedin_url' => $row['person_linkedin_url'] ?? null,
            'website' => $row['website'] ?? null,
            'company_linkedin_url' => $row['company_linkedin_url'] ?? null,
            'facebook_url' => $row['facebook_url'] ?? null,
            'twitter_url' => $row['twitter_url'] ?? null,
            'city' => $row['city'] ?? null,
            'state' => $row['state'] ?? null,
            'country' => $row['country'] ?? null,
            'company_address' => $row['company_address'] ?? null,
            'company_city' => $row['company_city'] ?? null,
            'company_state' => $row['company_state'] ?? null,
            'company_country' => $row['company_country'] ?? null,
            'company_phone' => $row['company_phone'] ?? null,
            'technologies' => $row['technologies'] ?? null,
            'annual_revenue' => $row['annual_revenue'] ?? null,
            'total_funding' => $row['total_funding'] ?? null,
            'latest_funding' => $row['latest_funding'] ?? null,
            'latest_funding_amount' => $row['latest_funding_amount'] ?? null,
            'last_raised_at' => $row['last_raised_at'] ?? null,
        ]);
    }

   public function batchSize(): int
    {
        return 1000;
    }

    public function chunkSize(): int
    {
        return 2000;
    }

    
}
