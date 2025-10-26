<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
<title>Realauto</title>
<style>
  body{ background-color:#F0F0F0;font-family: 'Roboto', sans-serif;font-size: 14px;}
</style>
</head>


<body style="width:600px; margin:0px auto; padding:0px;">
  <div style=" background-color:#fff; padding:30px;">
  
     <div style=" margin-top:0px; padding-top:10px;">
        <div style="text-align:center; padding:25px 0px 25px 0px;">
          <img src="https://realauto.in/img/logo.png" alt="logo" style="width: 150px;"/>
        </div>
        <div style="clear:both;"></div>
     </div>
     <p style="text-align:center;">Congrats! You have a new lead </p>
     <div style=" background-color:#f9e0f5; padding:20px;">
        <h4 style="font-size: 20px;border-bottom: 1px solid #a3a3a3;
    padding-bottom: 6px;">Lead Details on RealAuto</h4>
       <!-- <p>Facebook Lead via <b>Nest Colours</b></p>
        <p><span style="color:#3F3F3F;">Campaign:</span> Nest Colours 1%</p>
        <p><span style="color:#3F3F3F;">Adset:</span> New ad set</p>
        <p><span style="color:#3F3F3F;">Ad:</span> New ad</p>
        <br> -->
        <p><span style="color:#3F3F3F;">Email:</span> <?php echo $email; ?> </p>
        <p><span style="color:#3F3F3F;">Full Name:</span> <?php echo $name; ?></p>
        <p><span style="color:#3F3F3F;">Phone Number:</span> <?php echo $phone; ?></p>
       <!-- <p><span style="color:#3F3F3F;">Service Required On:</span> Urgent</p>-->
        <p><span style="color:#3F3F3F;">Project:</span><?php echo $project; ?></p>
     </div>
     <div style="margin:0px 20px; text-align:center;">
       <p style="color:#5e5e5e; font-size:12px;">Manage this lead in Realauto to manage, contact and follow up with them.</p>
       <a href="https://realauto.in/leads-master" target="_blank"><button style="background-color: #7b27d1;
    border: 0;
    color: white;
    padding: 10px 22px;
    font-size: 16px;
    margin-top: 15px;
    border-radius: 4px;">View Lead</button></a>
     </div>
  </div>
</body>
</html>

