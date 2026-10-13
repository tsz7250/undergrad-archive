<?php
header("Access-Control-Allow-Origin: *");
$dist = $_POST["dist"];
$context  = stream_context_create(array('http' => array('header' => 'Accept: application/json')));
$url ="https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=f4cc0b12-86ac-40f9-8745-885bddc18f79&rid=0daad6e6-0632-44f5-bd25-5e1de1e9146f";
$xml = file_get_contents($url, false, $context);
$xml = json_decode($xml);
print ("<p>行政區:$dist</p>");
print ("<table><tr><td>行政區</td><td>停車場名稱</td><td>          總停車位數</td><td>剩餘車位</td></tr>");
foreach ($xml->{"parkingLots"} as $key)
{
    $d = $key->{"areaName"};
	if(strcmp($d,$dist)==0)
	{
		$aN = $key->{"areaName"};
		$pN = $key->{"parkName"};
		$tS = $key->{"totalSpace"};
		$sS = $key->{"surplusSpace"};
		print ("<tr><td>$aN</td><td>$pN</td><td>$tS</td><td>$sS</td></tr>");
	}
    
}
print ("</table>");
?>
 
