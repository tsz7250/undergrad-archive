$(function() {
    var today = new Date();
    var year = today.getFullYear();
    var month = ("0" + (today.getMonth() + 1)).slice(-2); // Add 1 to month and format it as two digits
    var day = ("0" + today.getDate()).slice(-2); // Format day as two digits
    $("#MonthAndDay").val(year + "-" + month + "-" + day);
});

$("#setDate").click(function() {
    var startMonth = $("#MonthAndDay").val().split("-")[1];
    var startDay = $("#MonthAndDay").val().split("-")[2];
    setMonthAndDay(startMonth, startDay);

    var topicCount = topic.length;

    //1 sec = 1000 ms
    //1 min = 60 sec, 1 hr = 60 min, 1 day = 24 hr
    let millisecsPerDay = 24*60*60*1000;

    // 重新生成課程表
    $("#courseTable").empty();
    $("#courseTable").append("<tr><th>場次</th><th>時間</th><th>主題</th></tr>");
    for(var x=0; x<topicCount; x++){
        let row = $("<tr>"+
            `<td>${x+1}</td>`+           
            `<td>${new Date(startDate.getTime()+7*x*millisecsPerDay).toLocaleDateString('zh-TW',{month:'numeric',day:'numeric'})}</td>`+
            `<td>${topic[x]}</td>`+
            "</tr>");

        if(topic[x] == "停課"){
            row.css("color","grey");
        }

        $("#courseTable").append(row);
    }
});
