<?php
header("Access-Control-Allow-Origin: *");
$context  = stream_context_create(array('http' => array('header' => 'Accept: application/json')));
$url = "GlobalOilOpenData.csv";
$data = file_get_contents($url, false, $context);
print $data;
?>
