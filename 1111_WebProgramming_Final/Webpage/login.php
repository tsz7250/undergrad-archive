<?php
	$link = mysqli_connect( 
				'localhost', 
				'hungying',       
				'oppig66666',  
				'hw5');
	$user = $_GET['user'];
	$res = $_GET['res'];
	$fn = $_GET['fn'];
	$price = $_GET['price'];
	$date = $_GET['date'];
	$sql = 'SELECT * FROM `user`';
	$result = mysqli_query($link, $sql);
	while ($sqlget = $result->fetch_assoc()) {
		if($user == $sqlget['username'] ){
			$sql = "INSERT INTO `record` (`username` , `restaurant` , `food_name` , `price` , `time`) VALUES (\"$user\"  , \"$res\" , \"$fn\" , \"$price\" , \"$date\")";
			mysqli_query($link, $sql);
			print("1");
		}
	}

	
?>