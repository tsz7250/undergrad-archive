var topic = 
    ["尚未開學",
    "停課",
    "國定假日",
    "環境準備",
    "隨機性",
    "重複性",
    "停課",
    ];

var startDate = new Date();

function setMonthAndDay(startMonth, startDay){
    //一次設定好月份與日期
    startDate.setMonth(startMonth-1, startDay);
    //時間先忽略，設為0
    startDate.setHours(0);
    startDate.setMinutes(0);
    startDate.setSeconds(0);
}

setMonthAndDay(1,1);