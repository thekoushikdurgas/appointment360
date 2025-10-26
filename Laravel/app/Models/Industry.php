<?php

namespace App\Models;

use App\Models\Extension\Eloquent\HasManyWithCommaSeparate\CommaSeparateRelationTrait;
use App\Models\Helper\CommonFunction;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Industry extends Model
{
    use HasFactory, 
        CommonFunction;


    protected $table = 'dim_industry';
    protected $fillable = ['name','website','tag_id'];


}
