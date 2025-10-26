<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Razorpay\Api\Api;

class SubscriptionController extends Controller {

    public function showForm() {
        // Fetch subscription plans from Razorpay
        $api = new Api(env('RAZORPAY_KEY'), env('RAZORPAY_SECRET'));
        $plans = $api->plan->all()->items;
        //dd(  $plans);

        return view('subscribe', compact('plans'));
    }

    // callback method
    public function callbacksubscriptions(Request $request) {
        if (!empty($request->input('razorpay_payment_id')) && !empty($request->input('merchant_order_id'))) {
            $success = true;
            $error = '';
            try {
                // store temprary data
                $dataFlesh = array(
                    'txnid' => $request->input('merchant_trans_id'),
                    'card_holder_name' => $request->input('card_holder_name_id'),
                    'productinfo' => $request->input('merchant_product_info_id'),
                    'surl' => $request->input('merchant_surl_id'),
                    'furl' => $request->input('merchant_furl_id'),
                    'order_id' => $request->input('merchant_order_id'),
                    'razorpay_payment_id' => $request->input('razorpay_payment_id'),
                    'merchant_subscription_id' => $request->input('merchant_subscription_id'),
                    'merchant_amount' => $request->input('merchant_amount'),
                    'merchant_plan_id' => $request->input('merchant_plan_id'),
                    'created_at' => time(),
                );
                //    $this->session->set_flashdata('paymentInfo', $dataFlesh);
            } catch (Exception $e) {
                $success = false;
                $error = 'Request to Razorpay Failed';
            }
            if ($success === true) {

                die("Success");
            } else {
                die("Failed");
            }
        } else {
            echo 'An error occured. Contact site administrator, please!';
        }
    }

    public function subscribe(Request $request) {

      //  dd($_POST);
        // Get plan ID from the form
        $planId = $request->input('plan');
        $first_name = $request->input('first_name');
        $last_name = $request->input('last_name');
        $plan_amount = $request->input('plan_amount');
        $your_email = $request->input('your_email');
        $phone= $request->input('phone');
        $email_marketing_template = $request->input('email_marketing_template');
        $email_marketing_template_1 = $request->input('email_marketing_template_1');
        $email_marketing_template_2 = $request->input('email_marketing_template_2');
        $addon_amount=$email_marketing_template[0]+ $email_marketing_template_1[0]+$email_marketing_template_1[0];
       // dd($addon_amounts);
        // Initialize Razorpay API
        $api = new Api(env('RAZORPAY_KEY'), env('RAZORPAY_SECRET'));

//        $order = $api->order->create([
//            'amount' => $request->plan_amount * 100, // Amount in paisa
//            'currency' => 'INR', // Change as per your currency
//            'payment_capture' => 1, // Auto capture payment
//            'notes' => [
//                'plan_id' => $request->plan_id,
//            ],
//        ]);
//        $subscriptionData = array(
//            'plan_id' => $request->plan_id,
//            'customer_notify' => 1,
//            'total_count' => '10',
//            'notes' => array(
//                'name' => "sdfsdfgsdfgs",
//            ),
//        );
//        $api = new Api($key_id, $secret);


        $fff = $api->subscription->create(
                array(
                    'plan_id' => $planId,
                    'customer_notify' => 1,
                    'quantity' => 1,
                    'total_count' => 3,
                    'addons' => array(
                        array(
                            'item' => array(
                                'name' => 'Delivery charges',
                                'amount' => $addon_amount*100,
                                'currency' => 'INR'
                            )
                        )
                    ),
                    'notes' => array(
                        'key1' => 'value3',
                        'key2' => 'value2')
                )
        );
        // dd($fff );
        $orderId = $fff->id;
        $plan_id = $fff->plan_id;
        // Redirect to Razorpay payment page
        // $orderId = $order->id;
        $payInfo = array(
            'txnid' => time(),
            'card_holder_name' => $first_name.' '.$last_name,
            'amount' => $request->plan_amount * 100,
            'email' => $your_email,
            'phone' => $phone,
            'productinfo' => "Test",
            'surl' => "",
            'furl' => "",
            'currency_code' => 'INR',
            'order_id' => time(),
            'lang' => 'en',
            'store_name' => 'Piama',
            'return_url' => 'http://127.0.0.1:8000/callbacksubscriptions',
            'payment_type' => 'create_subscriptions',
            'subscription_id' => $orderId,
            'plan_id' => $plan_id,
            'created_at' => time(),
            'charge_at' => time(),
            'date_end_plan_at' => strtotime("+1 years", time()),
            'start_at' => time(),
            'package' => "ddd",
            'price' => $plan_amount*100,
            'package_plan_id' => $request->plan_id,
            'package_type' => "hh",
        );

        return view('razorpay', compact('payInfo'));
    }

}
