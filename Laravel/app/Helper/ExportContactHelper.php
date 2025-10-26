<?php

namespace App\Http\Helpers;

use App\PayrollEmployee;
use Maatwebsite\Excel\Concerns\FromQuery;
use Maatwebsite\Excel\Concerns\Exportable;

class ExportContactHelper implements FromQuery
{
use Exportable;


public function query()
{
// get the salary information for the given month and given department 
    return PayrollEmployee::query()->where(['salary_month' => $this->month,'department_id'=>$this->department]); 
}
}