<?php

namespace App\Exports;

use App\Models\Contacts;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\FromQuery;
use Maatwebsite\Excel\Concerns\Exportable;
use Maatwebsite\Excel\Concerns\WithHeadings;
class ContactsExport implements FromQuery, WithHeadings
{
     use Exportable;

    public function __construct(array $ids)
    {
        $this->ids = $ids;
    }
     public function headings(): array
    {
        
         $AuthuserColumnAllowed=auth()->user()->column_allowed;
        if($AuthuserColumnAllowed){
            $columnsArray=json_decode($AuthuserColumnAllowed);
        }
        else{
            $columnsArray = \DB::getSchemaBuilder()->getColumnListing('contacts');
        unset($columnsArray[0]);
        unset($columnsArray[53]);
        unset($columnsArray[54]);
        unset($columnsArray[55]);
        }
        foreach ($columnsArray as $key => $value){
   $columns[$key] = ucfirst(str_replace('_', ' ', $value));
}
        return $columns;
    }

    public function query()
    {
       //  $coll= Contacts::whereIn('id',$contacts_id)->get();
         $AuthuserColumnAllowed=auth()->user()->column_allowed;
        if($AuthuserColumnAllowed){
            $columns=json_decode($AuthuserColumnAllowed);
        }
        else{
            $columns = \DB::getSchemaBuilder()->getColumnListing('contacts');
        unset($columns[0]);
        unset($columns[53]);
        unset($columns[54]);
        unset($columns[55]);
        }
        
        return Contacts::query()->whereIn('id', $this->ids)->select($columns);
    }
   
    /**
    * @return \Illuminate\Support\Collection
    */
//    public function collection()
//    {
//        return Contacts::all();
//    }
}
