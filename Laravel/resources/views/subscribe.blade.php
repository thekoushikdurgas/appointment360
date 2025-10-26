<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css">
@if (session('success'))
<div class="alert alert-success">
    {{ session('success') }}
</div>
@endif

@if (session('error'))
<div class="alert alert-danger">
    {{ session('error') }}
</div>
@endif
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-lg-9">
            <h1 class="mb-3">Contact Us</h1>
            <form method="POST" action="/subscribe">
                @csrf
                <div class="row g-3">
                    <div class="col-md-3">
                        <label for="your-name" class="form-label">First Name</label>
                        <input type="text" class="form-control" id="your-name" name="first_name" required>
                    </div>
                    <div class="col-md-3">
                        <label for="your-surname" class="form-label">Last Name</label>
                        <input type="text" class="form-control" id="your-surname" name="last_name">
                    </div>

                    <div class="col-md-6">
                        <div>
                            <label for="plan" class="form-label">Max Subscriber's Count:</label>
                            <select name="plan" id="plan" class="form-control" required>
                                @foreach ($plans as $plan)
                                <option value="{{ $plan->id }}" data-amt="{{ $plan->item->amount }}">{{ $plan->item->name }} - {{ $plan->item->amount }}</option>
                                @endforeach
                            </select>
                            <input type="hidden" name="plan_amount" value="" id="plan_amount">

                        </div>
                    </div>
                    <div class="col-md-6">
                        <label for="your-email" class="form-label">Your Email</label>
                        <input type="email" class="form-control" id="your-email" name="your_email" required>
                    </div>
                    <div class="col-md-6">
                        <label for="your-phone" class="form-label">Phone</label>
                        <input type="tel" class="form-control" id="phone" name="phone">
                    </div>
                    <div class="col-12">
                        <div data-name="ff_cn_id_2" class="ff-t-container ff-column-container ff_columns_total_1 order-bump ">
                            <div class="ff-t-cell ff-t-column-1" style="flex-basis: 100%;">
                                <div class="ff-el-group ff-el-form-hide_label">
                                    <div class="ff-el-input--label asterisk-right">
                                        <label aria-label="Email Marketing Templates">Email Marketing Templates</label>
                                    </div>
                                    <div class="ff-el-input--content">
                                        <div class="ff-el-form-check ff-el-form-check-">
                                            <label class="ff-el-form-check-label" for="email_marketing_template_6315f67746317376984d57a9003af26d">
                                                <input type="checkbox" name="email_marketing_template[]" data-name="email_marketing_template" class="ff-el-form-check-input ff-el-form-check-checkbox ff_payment_item" value="899" data-payment_value="899" data-calc_value="899" data-group_id="ff_5_email_marketing_template__" id="email_marketing_template_6315f67746317376984d57a9003af26d">
                                                <span class="ff_plan_title">I want "50+ Proven Email Marketing &amp; Automation Templates" for ₹899</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="ff-el-group  ff-custom_html order-bump-desc" data-name="custom_html-5_2">
                                    <p>
                                        <strong>Special One-time offer for ₹899: </strong>Grab the exclusive collection of 50+ proven and successful automation email swipes&nbsp;designed to help you start an effective conversational relationship with your leads and customers.
                                    </p>
                                </div>
                                <div class="ff-el-group ff-el-form-hide_label">
                                    <div class="ff-el-input--label asterisk-right">
                                        <label aria-label="30 Minute Consultation Call">30 Minute Consultation Call</label>
                                    </div>
                                    <div class="ff-el-input--content">
                                        <div class="ff-el-form-check ff-el-form-check-">
                                            <label class="ff-el-form-check-label" for="email_marketing_template_1_4214a23dc9282bbfbc1dc2b9bbfe3672">
                                                <input type="checkbox" name="email_marketing_template_1[]" data-name="email_marketing_template_1" class="ff-el-form-check-input ff-el-form-check-checkbox ff_payment_item" value="3999" data-payment_value="3999" data-calc_value="3999" data-group_id="ff_5_email_marketing_template_1__" id="email_marketing_template_1_4214a23dc9282bbfbc1dc2b9bbfe3672">
                                                <span class="ff_plan_title">I need a 30 minute 1-1 training and guidance to use SendMails</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="ff-el-group  ff-custom_html order-bump-desc" data-name="custom_html-5_3">
                                    <p>
                                        <strong>30-Minute Consultation Call for ₹3999</strong>: Enhance your SendMails experience with a 30-minute consultation! For a limited time, get personalized guidance, best practices, and expert insights to supercharge your email campaigns. Don't miss out on this opportunity to maximize your SendMails potential.
                                    </p>
                                </div>
                                <div class="ff-el-group ff-el-form-hide_label">
                                    <div class="ff-el-input--label asterisk-right">
                                        <label aria-label="AWS Consultation Call">AWS Consultation Call</label>
                                    </div>
                                    <div class="ff-el-input--content">
                                        <div class="ff-el-form-check ff-el-form-check-">
                                            <label class="ff-el-form-check-label" for="email_marketing_template_2_c727ac7e552f94256ec6dffbd47ad53b">
                                                <input type="checkbox" name="email_marketing_template_2[]" data-name="email_marketing_template_2" class="ff-el-form-check-input ff-el-form-check-checkbox ff_payment_item" value="5999" data-payment_value="5999" data-calc_value="5999" data-group_id="ff_5_email_marketing_template_2__" id="email_marketing_template_2_c727ac7e552f94256ec6dffbd47ad53b">
                                                <span class="ff_plan_title">I need help in setting up my Amazon SES account</span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div class="ff-el-group  ff-custom_html order-bump-desc" data-name="custom_html-5_4">
                                    <p>
                                        <strong>Amazon SES Consultation for ₹5999:</strong> Unlock our expert-guided Amazon SES Setup Package! Ensure seamless integration, maximize deliverability, and kickstart your email campaigns with confidence. Our team will personally assist you in setting up Amazon SES, optimizing it for best results, and providing you with essential tips to maintain a high sender reputation.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
<input type="hidden" name="addon_amount" value="0" id="addon_amount" >

                        <button type="submit" class="btn btn-dark w-100 fw-bold" >Complete Order <span class="ff_order_total">₹12,084.00</span></button>

                    </div>
                </div>
        </div>
        </form>
    </div>
</div>
</div>



<style>.order-bump {
        background: #F8DA52;
        border: 2px dashed;
        padding: 20px 30px 20px;
        margin-bottom: 30px;
        display: flex;
        gap: 15px;
        width: 100%;
    }</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script>
    calculate_total();
$('#plan').on('change', function () {
    var amm = $(this).find(':selected').attr('data-amt');
     var total = $("#addon_amount").val();
    $("#plan_amount").val(amm);
    $(".ff_order_total").html("₹"+parseInt(amm)+parseInt(total));
            
});
$("input[type=checkbox]").change(function(){
  calculate_total();
});
function calculate_total(){
 var sum = parseInt($("#plan_amount").val());
 var total=0;
    $("input[type=checkbox]:checked").each(function(){
      total += parseInt($(this).val());
    });

    //alert(total);
    $('#addon_amount').val(total);   
    $('.ff_order_total').html("₹"+sum+total);   
}
</script>