<?php
	session_start();
	include("../../../Includes/setting.php");
	include("../../../Includes/connectdb.php");
	include("../../../Includes/mailsetting.php");
	$pid=$_GET['pid'];
	$cd=date('y-m-d');
	
	if($pid==1)
	{
	    $username=$_SESSION['uid'];
	    $pass=md5($_POST['opass']);
	    $rs = mysqli_query($con,"select * from login where user_id='$username' and password='$pass'")  or die('ERROR : '.mysqli_error($con));
	    
	    if(mysqli_num_rows($rs)>0)
	    {
	    	$pass=md5($_POST['npass']);
		    $update_query = mysqli_query($con,"update login set password='$pass' where user_id='$username'");
		    $_SESSION['msg']="Password Changed Successfully";
		    header("Location:../../Students/change_password.php");
	    }
	    else
	    {
	        $_SESSION['msg']="Invalid Old Password";
	        header("Location:../../Students/change_password.php");
	    }
	}
	if($pid==2)
	{
	    $username=$_SESSION['uid'];
	    $file_name = $_FILES["img"]["name"];
        $file_tmp_name = $_FILES["img"]["tmp_name"];
        if($file_name!="")
        {
	        $ext = end(explode('.',$file_name));

	        if($ext == "png" || $ext == "jpg" || $ext == "jpeg" || $ext == "")
	        {
	            $new_file_name = $_SESSION['m_id'].".".$ext;
	            $upload_path = "../../Profile/".$new_file_name;
	            move_uploaded_file($file_tmp_name,$upload_path);

	            $update_query = mysqli_query($con,"update member set contact_no='$_POST[cno]',address='$_POST[add]' where email_id='$username'");
	            $update_query = mysqli_query($con,"update login set image='$new_file_name' where user_id='$username'");
	            $_SESSION['img']=$new_file_name;
		    	header("Location:../../Students/Profile.php?cmd=0");
	        }
	        else{
	            $_SESSION['msg']="File format not supported";
	            header("Location:../../Students/Profile.php?cmd=1");
	        }
	    }
	    else
	    {
	    	$update_query = mysqli_query($con,"update member set contact_no='$_POST[cno]',address='$_POST[add]' where email_id='$username'");
	    	header("Location:../../Students/Profile.php?cmd=0");
	    }
	}
	if($pid==7)
	{
		$right_answer=0;
		$wrong_answer=0;
		$unanswered=0;
		$keys=array_keys($_POST);
		$order=join(",",$keys);
		$data=substr($order,0,strrpos($order,","));
		echo $data;
		$query = "select sno,answer from question where sno IN($data) ORDER BY sno";
		$response=mysqli_query( $con, $query)   or die(mysqli_error($con));

		while($result=mysqli_fetch_array($response)){
			echo $_POST[$result['sno']].nl2br("\n");
			if($result['answer']==$_POST[$result['sno']]){
				$right_answer++;
			}else if($_POST[$result['sno']]=="nil"){
				$unanswered++;
			}
			else{
				$wrong_answer++;
			}
		}
		$tot=$right_answer-($wrong_answer*.25);
		$per=$tot*10;
		$gr="Nil";
		$res="PASS";
		if($per>=90)
			$gr="A";
		else if($per>=85)
			$gr="B";
		else if($per>=60)
			$gr="C";
		else if($per>=50)
			$gr="D";
		else
		{
			$res="FAIL";
			$gr="Nil";
		}
		$_SESSION['right_answer']=$right_answer;
		$_SESSION['wrong_answer']=$wrong_answer;
		$_SESSION['unanswered']=$unanswered;
		$_SESSION['tot']=$tot;
		$_SESSION['per']=$per;
		$_SESSION['gr']=$gr;
		$_SESSION['res']=$res;
		$cd=date("d-m-y");
		$_SESSION['cd']=$cd;
		$_SESSION['tq']=$right_answer+$wrong_answer+$unanswered;
		/*echo nl2br("\n");

		echo "Right Answer : ".$_SESSION['right_answer'].nl2br("\n");
        echo "Wrong Answer : ".$_SESSION['wrong_answer'].nl2br("\n");
        echo "Unanswered : ".$_SESSION['unanswered'].nl2br("\n");*/

		$sql=mysqli_query($con,"Insert into result(mid,correct_answer,wrong_answer,unanswered,total_marks,percentage,grade,result,cid,doe) values('$_SESSION[m_id]','$_SESSION[right_answer]','$_SESSION[wrong_answer]','$_SESSION[unanswered]','$_SESSION[tot]','$_SESSION[per]','$_SESSION[gr]','$_SESSION[res]','$_SESSION[course]','$cd')") or die('ERROR'.mysqli_error($con));
	 	 
		
		header('Location:../../students/test_result.php');
	}
?>