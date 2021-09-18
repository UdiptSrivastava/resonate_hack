<?php
	session_start();
	include("../../../Includes/setting.php");
	include("../../../Includes/connectdb.php");
	include("../../../Includes/mailsetting.php");
	$pid=$_GET['pid'];
	$cd=date('y-m-d');
	if($pid==1)
	{
		$flag=1;
		if(isset($_POST['Save_Course']))
		{
			$sql=mysqli_query($con,"select course_code from courses where course_code='$_POST[ccode]'")  or die('Error : '.mysqli_error($con));
			if(mysqli_num_rows($sql)==0)
			{ 
		 		$sql=mysqli_query($con,"select course_code from courses where course_name='$_POST[cname]'")  or die('Error : '.mysqli_error($con));
				if(mysqli_num_rows($sql)==0)
				{ 
		 		
			 		$sql=mysqli_query($con,"insert into courses values ('$_POST[ccode]','$_POST[cname]','$_POST[duration]','$_POST[cfee]','$_POST[modules]','$_POST[career]')") or die('Error'.mysqli_error($con));
					if(isset($_SESSION['msg']))
						unset($_SESSION['msg']);
					header("location:../../Admin/courses.php");
		 		}
			 	else
				{
			 		$_SESSION['msg']='Course Name already exist';
					$flag=0;
				}
			}
			else
			{
				$flag=0;
			 	$_SESSION['msg']='Course Code already exist';
			}
		}

		if(isset($_POST['Delete_Course']))
		{
			$sql=mysqli_query($con,"delete from courses where course_code='$_SESSION[occ]'")  or die('Error : '.mysqli_error($con));
			if(isset($_SESSION['msg']))
				unset($_SESSION['msg']);
			header("location:../../Admin/courses.php");
		}
		if(isset($_POST['Update_Course']))
		{
			if($_SESSION['occ']!=$_POST['ccode'])
			{
				$sql=mysqli_query($con,"select course_code from courses where course_code='$_POST[ccode]'")  or die('Error : '.mysqli_error($con));
				if(mysqli_num_rows($sql)>0)
				{
					$flag=2;
				 	$_SESSION['msg']='Course Code already exist';
				}
			}
			else if($_SESSION['ocn']!=$_POST['cname'])
			{
				$sql=mysqli_query($con,"select course_code from courses where course_name='$_POST[cname]'")  or die('Error : '.mysqli_error($con));
				if(mysqli_num_rows($sql)>0)
				{
					$flag=2;
				 	$_SESSION['msg']='Course Name already exist';
				}
			}
			
			if($flag==1)			
			{
				$sql=mysqli_query($con,"update courses set course_code='$_POST[ccode]',course_name='$_POST[cname]',duration='$_POST[duration]',Fees='$_POST[cfee]',module='$_POST[modules]',career='$_POST[career]' where course_code='$_SESSION[occ]' ") or die('Error'.mysql_errors());
				if(isset($_SESSION['msg']))
					unset($_SESSION['msg']);
				header("location:../../Admin/courses.php");
			}
		}
		if($flag==0 || $flag==2)
		{
			$_SESSION['cc']=$_POST[ccode];
			$_SESSION['cn']=$_POST[cname];
			$_SESSION['cf']=$_POST[cfee];
			$_SESSION['cm']=$_POST[modules];
			$_SESSION['car']=$_POST[career];
			$_SESSION['cd']=$_POST[duration];
			header("location:../../Admin/courses.php?cmd=$_SESSION[cmd]");
			
		}	
	}
	if($pid==2)
	{
		if(isset($_POST['Delete_FEC']))
		{
			$tn=$_SESSION['tn'];
			$sno=$_SESSION['sno'];
			$sql=mysqli_query($con,"delete from $tn where sno='$sno'")  or die('Error : '.mysqli_error($con));
			if(isset($_SESSION['msg']))
				unset($_SESSION['msg']);
			header("location:../../Admin/show.php?cmd=$_SESSION[cmd]");
		}
	}
	if($pid==3)
	{
		if(isset($_POST['Delete_App']))
		{
			$mid=$_SESSION['mid'];
			$sql=mysqli_query($con,"delete from application where mid='$mid'")  or die('Error : '.mysqli_error($con));
			if(isset($_SESSION['mid']))
				unset($_SESSION['mid']);
			header("location:../../Admin/Application.php");
		}
		if(isset($_POST['Activate_App']))
		{
			$mid=$_SESSION['mid'];
			$sql=mysqli_query($con,"select fees,duration,module from courses where course_code='$_POST[ccode]'")  or die('Error : '.mysqli_error($con));
			$rs=mysqli_fetch_array($sql);
			$cf=$rs[0];
			$cd=$rs[1];
			$cm=$rs[2];
			$date=date('y-m-d');
			$sql=mysqli_query($con,"insert into member(mid,name, father_name, email_id, contact_no, gender, address, dob, course_code,bank_name,ddno,course_fees,duration,modules,doa) values('$mid','$_POST[name]','$_POST[fname]','$_POST[email]','$_POST[cno]','$_POST[gen]','$_POST[add]','$_SESSION[dob]','$_POST[ccode]','$_POST[bname]','$_POST[ddno]','$cf','$cd','$cm','$date')") or die('ERROR : '.mysqli_error($con));
			if($_POST['gen']=="Male")
				$img="male.jpg";
			else
				$img="female.jpg";
			$pass= getPassword(6); 
			$epass=md5($pass);
			$sql=mysqli_query($con,"insert into login(mid,user_id, password, profile, status, image) values('$mid','$_POST[email]','$epass','S','Active','$img')") or die('ERROR : '.mysqli_error($con));
			$sql=mysqli_query($con,"delete from application where mid='$mid'")  or die('Error : '.mysqli_error($con));

			
			$otp = rand(1000,9999); 
			$_SESSION['otp']=$otp;
			$message = '<html><body>';

			$message .= '<table rules="all" style="border-color: #666;font-size:18px;" cellpadding="10" width="50%" border="1">';
			
			$message .= "<tr><td><strong>Member ID:</strong> </td><td>" . $mid . "</td></tr>";
			$message .= "<tr style='background: #eee;'><td><strong>Member Name:</strong> </td><td>" . $_POST['name'] . "</td></tr>";
			$message .= "<tr><td><strong>User Id:</strong> </td><td>" . $_POST['email'] . "</td></tr>";
			$message .= "<tr><td><strong>Password:</strong> </td><td>" . $pass . "</td></tr>";
			$message .= "</table>";
			$message .= "</body></html>";
			$subject = "Successful Registration for Membership";
			$to=$_POST['email'];
			sendMail($to,$subject, $message);

			if(isset($_SESSION['mid']))
				unset($_SESSION['mid']);
			header("location:../../Admin/Application.php");
		}
	}
	if($pid==4)
	{
		if(isset($_POST['Delete_Mem']))
		{
			$mid=$_SESSION['mid'];
			$sql=mysqli_query($con,"delete from member where mid='$mid'")  or die('Error : '.mysqli_error($con));
			if(isset($_SESSION['mid']))
				unset($_SESSION['mid']);
			header("location:../../Admin/Members.php?cmd=$_SESSION[cmd]");
		}
		if(isset($_POST['Inactivate_Mem']))
		{
			$mid=$_SESSION['mid'];			
			$sql=mysqli_query($con,"update Login set status='Inactive' where mid='$mid'") or die('ERROR : '.mysqli_error($con));

			$message = '<html><body>';
			$message .='<h2>Your Id is Deactivated. Please contact Admin</h2>';
			$message .= '<table rules="all" style="border-color: #666;font-size:18px;" cellpadding="10" width="50%" border="1">';
			
			$message .= "<tr><td><strong>Member ID:</strong> </td><td>" . $mid . "</td></tr>";
			$message .= "<tr style='background: #eee;'><td><strong>Member Name:</strong> </td><td>" . $_POST['name'] . "</td></tr>";
			$message .= "<tr><td><strong>User Id:</strong> </td><td>" . $_POST['email'] . "</td></tr>";
			$message .= "<tr><td><strong>Status:</strong> </td><td>" . 'Inactive' . "</td></tr>";
			$message .= "</table>";
			$message .= "</body></html>";
			$subject = "Your Id is Inactive";
			$to=$_POST['email'];
			sendMail($to,$subject, $message);

			if(isset($_SESSION['mid']))
				unset($_SESSION['mid']);
			header("location:../../Admin/Members.php?cmd=$_SESSION[cmd]");
		}
		if(isset($_POST['Activate_Mem']))
		{
			$mid=$_SESSION['mid'];			
			$sql=mysqli_query($con,"update Login set status='Active' where mid='$mid'") or die('ERROR : '.mysqli_error($con));
			
			$message = '<html><body>';
			$message .='<h2>Your Id is now Activated by admin</h2>';
			$message .= '<table rules="all" style="border-color: #666;font-size:18px;" cellpadding="10" width="50%" border="1">';
			
			$message .= "<tr><td><strong>Member ID:</strong> </td><td>" . $mid . "</td></tr>";
			$message .= "<tr style='background: #eee;'><td><strong>Member Name:</strong> </td><td>" . $_POST['name'] . "</td></tr>";
			$message .= "<tr><td><strong>User Id:</strong> </td><td>" . $_POST['email'] . "</td></tr>";
			$message .= "<tr><td><strong>Status:</strong> </td><td>" . 'Active' . "</td></tr>";
			$message .= "</table>";
			$message .= "</body></html>";
			$subject = "Your Id is Active";
			$to=$_POST['email'];
			sendMail($to,$subject, $message);

			if(isset($_SESSION['mid']))
				unset($_SESSION['mid']);
			header("location:../../Admin/Members.php?cmd=$_SESSION[cmd]");
		}
	}
	if($pid==5)
	{
	    $username=$_SESSION['uid'];
	    $pass=md5($_POST['opass']);
	    $rs = mysqli_query($con,"select * from login where user_id='$username' and password='$pass'")  or die('ERROR : '.mysqli_error($con));
	    
	    if(mysqli_num_rows($rs)>0)
	    {
	    	$pass=md5($_POST['npass']);
		    $update_query = mysqli_query($con,"update login set password='$pass' where user_id='$username'");
		    $_SESSION['msg']="Password Changed Successfully";
		    header("Location:../../Admin/change_password.php");
	    }
	    else
	    {
	        $_SESSION['msg']="Invalid Old Password";
	        header("Location:../../Admin/change_password.php");
	    }
	}
	if($pid==6)
	{
		$cc=$_SESSION['cc'];

		if(isset($_POST['Delete_Course']))
		{
			$sno=$_SESSION['sno'];
			$s="delete from question where sno=".$sno;
			$sql=mysqli_query($con,$s)  or die('Error : '.mysqli_error($con));
			
		}
		else if(isset($_POST['Update_Course']))
		{
			$sno=$_SESSION['sno'];
			$s="Update question set question='$_POST[ques]',option1='$_POST[op1]',option2='$_POST[op2]',option3='$_POST[op3]',option4='$_POST[op4]',answer='$_POST[ans]' where sno=".$sno;
			$sql=mysqli_query($con,$s)  or die('Error : '.mysqli_error($con));
			
		}
		else
		{
			$sql=mysqli_query($con,"insert into question(course_code,question,option1,option2,option3,option4,answer) values ('$cc','$_POST[ques]','$_POST[op1]','$_POST[op2]','$_POST[op3]','$_POST[op4]','$_POST[ans]')") or die('Error - '.mysqli_error($con));
			
		}
		if(isset($_SESSION['msg']))
			unset($_SESSION['msg']);
		header("location:../../Admin/question.php?cc=$cc&cmd=0");
	}
	
?>