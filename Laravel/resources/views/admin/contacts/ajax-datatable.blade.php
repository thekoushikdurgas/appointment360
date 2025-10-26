 @foreach($contactList  as $contact)
                                    <tr data-cy="SelectableTableRow" class="zp_cWbgJ">
                                        <td class="zp_aBhrx">
                                            <div class="zp_C2NRr zp_wdoJt">
                                                <!--                                                <div class="zp_iJZr1" style="margin-right: 7px;">
                                                                                                    <label class="">
                                                                                                        <input type="checkbox" readonly="" value="false">
                                                                                                        <div class="zp_fwjCX" data-input="checkbox" data-cy-status="unchecked"></div>
                                                                                                    </label>
                                                                                                </div>-->
                                                <div>
                                                    <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                        <div class="zp_Ln9Ws EditTarget">
                                                            <div class="zp_DBwlj">
                                                                <div class="zp_LDJHm">
                                                                    <div class="zp_BC5Bd">
                                                                        <div class="zp_xVJ20">
                                                                            <span>
                                                                                <a href="#" style="">{{$contact->first_name}} {{$contact->last_name}}  </a>
                                                                            </span>
                                                                        </div>
                                                                    </div>
                                                                    <div class="zp_I1ps2">
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="http://www.linkedin.com/in/{{$contact->person_linkedin_url}}" target="_blank">
                                                                                <i class="fab fa-linkedin-in"></i>
                                                                            </a>
                                                                        </span>

                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="zp_U42AQ" style="display: none; right: 10px; top: 50%; transform: translateY(-50%);">
                                                                <div>
                                                                    <span>
                                                                        <button type="button" class="zp-button zp_zUY3r zp_jSaSY zp_rhXT_ zp_B7xze zp_Anyxc zp_rkb58" data-cy="">
                                                                            <i class="zp-icon apollo-icon apollo-icon-pen zp_dZ0gM zp_j49HX zp_uAV5p"></i>
                                                                        </button>
                                                                    </span>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <!--                                            <div class="zp_rvWYh zp_HAxXv">
                                                                                            <div class="zp_CO373">
                                                                                                <div class="zp_iJZr1">
                                                                                                    <label class="">
                                                                                                        <input type="checkbox" readonly="" value="false">
                                                                                                        <div class="zp_fwjCX" data-input="checkbox" data-cy-status="unchecked"></div>
                                                                                                    </label>
                                                                                                </div>
                                                                                            </div>
                                                                                            <div class="zp_dUDE8 zp_nkbtS" style="min-width: 270px;"></div>
                                                                                        </div>-->
                                        </td>
                                        <td style="max-width: 270px;" class="zp_aBhrx">
                                            <div>
                                                <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="zp_Y6y8d">{{$contact->title}}</span>
                                                        </div>
                                                        <div class="zp_U42AQ" style="display: none; right: 10px; top: 50%; transform: translateY(-50%);">
                                                            <div>
                                                                <span>
                                                                    <button type="button" class="zp-button zp_zUY3r zp_jSaSY zp_rhXT_ zp_B7xze zp_Anyxc zp_rkb58" data-cy="">
                                                                        <i class="zp-icon apollo-icon apollo-icon-pen zp_dZ0gM zp_j49HX zp_uAV5p"></i>
                                                                    </button>
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8 zp_qag6w" style="min-width: 270px;"></div>
                                            </div>
                                        </td>
                                        <td style="max-width: 180px;" class="zp_aBhrx">
                                            <div>
                                                <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="intentDataBars zp_oTOOy">
                                                                <span style="cursor: pointer;" class="zp_IL7J9">
                                                                    <div class="" style="width: 35px; height: auto; max-height: 35px; border-radius: 5px;">
                                                                        <span>
                                                                            <span style="position: fixed;"></span>
                                                                            <!--<img width="35" height="auto" style="border-radius: 5px;" src="https://zenprospect-production.s3.amazonaws.com/uploads/pictures/6550091c9c224300019d1826/picture" alt="Company logo">-->
                                                                        </span>
                                                                    </div>
                                                                </span>
                                                                <div class="zp_TvTJg">
                                                                    <div class="zp_J1j17">
                                                                        <a class="zp_WM8e5 zp_kTaD7" href="#">{{$contact->company}}</a>
                                                                    </div>
                                                                    <div class="zp_I1ps2">
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="{{$contact->website}}" target="_blank">
                                                                                <i class="fas fa-link"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="http://www.linkedin.com/company/{{$contact->company_linkedin_url}}" target="_blank">
                                                                                <i class="fab fa-linkedin-in"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="https://www.facebook.com/{{$contact->facebook_url}}" target="_blank">
                                                                                <i class="fab fa-facebook-f"></i>
                                                                            </a>
                                                                        </span>
                                                                        <span>
                                                                            <a class="zp-link zp_OotKe" href="https://twitter.com/{{$contact->twitter_url}}" target="_blank">
                                                                                <i class="fab fa-twitter"></i>
                                                                            </a>
                                                                        </span>
                                                                    </div>
                                                                </div>
                                                            </span>
                                                        </div>
                                                        <div class="zp_U42AQ" style="display: none;">
                                                            <div>
                                                                <span>
                                                                    <button type="button" class="zp-button zp_zUY3r zp_jSaSY zp_rhXT_ zp_B7xze zp_Anyxc zp_rkb58" data-cy="">
                                                                        <i class="zp-icon apollo-icon apollo-icon-pen zp_dZ0gM zp_j49HX zp_uAV5p"></i>
                                                                    </button>
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8 zp_uoWgG" style="min-width: 180px;"></div>
                                            </div>
                                        </td>
                                        <td  class="zp_aBhrx">

                                        </td>
                                        <td style="max-width: 250px;" class="zp_aBhrx">
                                            <div>
                                                <div class="zp-inline-edit-popover-trigger zp_oSeJs zp_YhA6I">
                                                    <div class="zp_Ln9Ws EditTarget">
                                                        <div class="zp_DBwlj">
                                                            <span class="zp_Y6y8d">{{$contact->city}}, {{$contact->country}}</span>
                                                        </div>
                                                        <div class="zp_U42AQ" style="display: none;">
                                                            <div>
                                                                <span>
                                                                    <button type="button" class="zp-button zp_zUY3r zp_jSaSY zp_rhXT_ zp_B7xze zp_Anyxc zp_rkb58" data-cy="">
                                                                        <i class="zp-icon apollo-icon apollo-icon-pen zp_dZ0gM zp_j49HX zp_uAV5p"></i>
                                                                    </button>
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8 zp_qag6w" style="min-width: 250px;"></div>
                                            </div>
                                        </td>
                                        <td style="max-width: 100px;" class="zp_aBhrx">
                                            <span class="zp_Y6y8d">{{$contact->employees}}</span>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8" style="min-width: 100px;"></div>
                                            </div>
                                        </td>
                                        <td class="zp_aBhrx">

                                            {{$contact->corporate_phone}}
                                        </td>
                                        <td style="max-width: 150px;" class="zp_aBhrx">
                                            <span class="zp_lm1kV">
                                                <div class="zp_paOF8">
                                                    <span class="zp_PHqgZ zp_TNdhR">{{$contact->industry}}</span>
                                                </div>
                                            </span>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8 zp_eGsOL" style="min-width: 150px;"></div>
                                            </div>
                                        </td>
                                        <td style="max-width: 150px;" class="zp_aBhrx">
                                            <span class="zp_lm1kV">
                                                <div class="zp_HlgrG zp_y8Gpn zp_uuO3B">

                                                    <?php $keywords = $contact->keywords;
                                                    ?>
                                                    <span>
                                                        <span class="zp_yc3J_ zp_FY2eJ">{{$keywords}} </span>
                                                    </span>



                                                </div>
                                            </span>
                                            <div class="zp_rvWYh">
                                                <div class="zp_dUDE8 zp_eGsOL" style="min-width: 150px;"></div>
                                            </div>
                                        </td>
                                    </tr>
                                    @endforeach