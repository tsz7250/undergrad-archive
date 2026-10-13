<?php
	$link = mysqli_connect( 
				'localhost', 
				'hungying',       
				'oppig66666',  
				'hw5');
	$user = $_POST['user'];
	$sql = 'SELECT * FROM `user`';
	$result = mysqli_query($link, $sql);
	$have = true;
	while ($sqlget = $result->fetch_assoc()) {
		if($user == $sqlget['username'] ){
			print("1");
			$have = false;
		}
	}
	if($have){
		$sql = "INSERT INTO `user` (`username`) VALUES (\"$user\")";
		mysqli_query($link, $sql);
		print("0");
	}
	
?>