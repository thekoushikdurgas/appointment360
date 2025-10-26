<?php

namespace App\Models;

use App\Models\Extension\Eloquent\HasManyWithCommaSeparate\CommaSeparateRelationTrait;
use App\Models\Helper\CommonFunction;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Contacts extends Model
{
    use HasFactory, 
        CommonFunction;

    const IMAGE_PATH = 'app/public/files/contacts';

    protected $table = 'contacts';
    protected $fillable = ['first_name','last_name','title','company','company_name_for_emails','email','email_status','primary_email_catch_all_status','seniority','departments','work_direct_phone','home_phone','mobile_phone','corporate_phone','other_phone','stage','employees','industry','keywords','person_linkedin_url','website','company_linkedin_url','facebook_url','twitter_url','city','state','country','company_address','company_city','company_state', 'company_country','company_phone','technologies','annual_revenue','total_funding','latest_funding','latest_funding_amount','latest_funding_amount','last_raised_at','contact_id','account_id'];

    
    
    
    /**
     * @name allColumnFilter
     * 
     * To get only active brand  
     */
    public function scopeAllColumnFilter ( $q, $value ){
        return $q->where(function ( $where ) use ( $value ) {
            $where->orWhere('first_name', 'LIKE', '%'. $value . '%');
            $where->orWhere('title', 'LIKE', '%'. $value . '%');
        });
    }

}
