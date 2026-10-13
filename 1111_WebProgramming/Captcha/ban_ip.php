<?php
  $ip = $_POST['ip'];
  $failedAttempts = $_POST['failedAttempts'];
  
  // Connect to the database
  $servername = "localhost";
  $username = "ytn20";
  $password = "Peter5678";
  $dbname = "HW4";

  $conn = new mysqli($servername, $username, $password, $dbname);
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

	$check_query = "SELECT * FROM data WHERE ip = '$ip'";
	$result = $conn->query($check_query);
	if ($result->num_rows > 0) {

		// Update the existing record
		$update_query = "UPDATE data SET failedAttempts = '$failedAttempts' WHERE ip = '$ip'";
		if ($conn->query($update_query) === TRUE) {
			echo "Record updated successfully";
		} else {
			echo "Error: " . $update_query . "<br>" . $conn->error;
		}
	} else {
		// Insert a new record
		$insert_query = "INSERT INTO data (ip, failedAttempts) VALUES ('$ip', '$failedAttempts')";
		if ($conn->query($insert_query) === TRUE) {
			echo "New record created successfully";
		} else {
			echo "Error: " . $insert_query . "<br>" . $conn->error;
		}
	}
  $conn->close();
?>
