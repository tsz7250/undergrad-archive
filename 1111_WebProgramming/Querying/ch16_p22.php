<?php
$aq = $_POST["station"];
$data = file_get_contents('NPA_TD1.csv');
$rows = explode("\n",$data);
$s = array();
$num=0;
foreach($rows as $row) {
    $s[] = str_getcsv($row);
    $num++;
}
print ("<table><tr><td>設置縣市</td><td>設置市區鄉鎮</td><td>設置地址</td><td>管轄警局</td><td>經度</td><td>緯度</td><td>拍攝方向</td><td>速限</td></tr>");
for ($i=2;$i<$num-1;$i++)
{
    $station = $s[$i][0];
	if(strcmp($aq,$station)!==0) { continue; }
	print ("<tr>");
	for ($j=0;$j<=8;$j++)
	{
		$value = $s[$i][$j];
		print ("<td>$value</td>");
	}
    print ("</tr>");
}
print ("</table>");
?>
