<!DOCTYPE html>
<html lang="zh">
	<head>
		<meta charset="UTF-8">
		<title>記帳</title>
		<link rel="stylesheet" href="ledger.css">
	</head>
	<body>
	<?php
		$link = mysqli_connect( 
					'localhost', 
					'hungying',       
					'oppig66666',  
					'hw5'); 
		mysqli_query($link, "SET NAMES 'UTF-8'");
		$user = $_POST["user"];
		if($user != null){
				$sql = "SELECT * FROM record where `username` = '" . $user ."'" ;
				$sql0 = "SELECT SUM(`price`) AS total FROM `record` WHERE `username` = '" . $user ."'";
		}
		else{
				$sql = "SELECT * FROM record where `username` = 'SDFSDFSDFZSDGZFSDGZDGDDKFZSDKFOSDKSDFLKDSGKSDFG'" ;
				$sql0 = "SELECT SUM(`price`) AS total FROM `record` WHERE `username` = 'SDFSDFSDFZSDGZFSDGZDGDDKFZSDKFOSDKSDFLKDSGKSDFG'";
		}
		$result = mysqli_query($link, $sql);
		$result0 = mysqli_query($link,$sql0);
		list($sum) = mysqli_fetch_row($result0);
		?>
	<div class="fixed" >
		<p style=>總金額:<?php echo $sum; ?></p>
	</div>
    <div class="background">
        <div class="shape"></div>
		<div class="shape"></div>
    </div>
	<div class="di">
        <h3>帳本</h3>
			<form method="POST" class="fo">
					<input type="text" name="user" placeholder="須查詢的帳號" >
			</form>

		<table class="demo">
			<thead>
				<tr>
					<th>帳號</th>
					<th>餐廳</th>
					<th>餐點</th>
					<th>價個</th>
					<th>時間</th>
				</tr>
			</thead>
			
			<tbody>
				<?php
				if(mysqli_num_rows($result) > 0){
					foreach($result as $row){
				?>
				<tr>
					<td><?php echo $row['username'];?></td>
					<td><?php echo $row['restaurant'];?></td>
					<td><?php echo $row['food_name'];?></td>
					<td><?php echo $row['price'];?></td>
					<td><?php echo $row['time'];?></td>
				</tr>
				<?php 
					}
				}
				?>
			</tbody>
		</table>
		<div>
			<button onclick="location.href='select.html'">回到主頁</button>
		</div>
		</div>
	</body>