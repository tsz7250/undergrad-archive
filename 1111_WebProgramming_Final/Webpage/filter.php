<?php
$servername = "localhost";
$username = "hungying";
$password = "oppig66666";
$dbname = "hw5";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$restaurant = $_POST['restaurant'];
$food_type = $_POST['food_type'];
$username = $_POST['name'];


if(empty($restaurant[0]) || $restaurant[0] == 'All' ){//是否有做篩選
    $restaurant = '';
} else {
    $restaurant = implode(",", $restaurant);
}

if(empty($food_type[0]) || $food_type[0] == 'All' ){
    $food_type = '';
} else {
    $food_type = implode(",", $food_type);
}

$stmt = $conn->prepare("SELECT restaurant, food_type, food_name, price FROM food WHERE (restaurant IN (?) OR ? = '') AND (food_type IN (?) OR ? = '')ORDER BY RAND() LIMIT 1");
$stmt->bind_param("ssss", $restaurant, $restaurant, $food_type, $food_type);
$stmt->execute();
$result = $stmt->get_result();


if ($result->num_rows > 0) {
    echo "<table id='rest'><tr> <th>餐廳</th> <th>食物類別</th> <th>食物名稱</th> <th>價錢</th></tr>";
    while($row = $result->fetch_assoc()) {
		if($row["restaurant"]=="料理廚房"){
			echo "<tr><td>馺哈料理廚房</td><td> " . $row["food_type"]. "</td><td>" . $row["food_name"]. "</td><td>" . $row["price"]. "</td></tr>";
		}	
        else{
			echo "<tr><td id='res'>" . $row["restaurant"]. "</td><td>" . $row["food_type"]. "</td><td id='nam'>" . $row["food_name"]. "</td><td id='pri'>" . $row["price"]. "</td></tr>";
		}
    }
    echo "</table>";
} else {
    echo "你的篩選不存在，請重新選擇";
}
$conn->close();
?>