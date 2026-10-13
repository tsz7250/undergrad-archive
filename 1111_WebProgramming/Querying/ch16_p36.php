<?php
header("Access-Control-Allow-Origin: *");
$input = $_POST["sel"];
$item = preg_replace("/s$/","",$input);
$context  = stream_context_create(array('http' => array('header' => 'Accept: application/xml')));
$url = "StationFacilityList.xml" ;
$xml = file_get_contents($url, false, $context);
$xml = simplexml_load_string($xml);
$date = $xml->StationFacility;
$sel = $xml->StationFacility->{$input};

print "<table>";
foreach ($xml->StationFacility as $key)
{
    $sID = $key->StationID;
    $station = $key->StationName->Zh_tw;
	$sel = $key->{$input};
	foreach ($sel->{$item} as $k2)
	{
		$des = $k2->{"Description"};
		print ("<tr><td>$sID</td><td>$station</td><td>$des</td></tr>");
	}
    
}
print ("</table>");
?>
