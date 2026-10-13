$(function() {
    //儲存目前作答到第幾題
    var currentQuiz = null;
    //當按鈕按下後，要做的事情
    $("#startButton").on("click",function(){
        //如果還沒開始作答就從這裡開始
        if(currentQuiz==null){
            currentQuiz=0;
            //顯示題目
            $("#question").text(questions[0].question);
            //將選項區清空(可以試著先不寫)
            $("#options").empty();
            //將選項逐個加入
            questions[0].answers.forEach(function(element,index,array){
                $("#options").append(`<input name='options' type='radio'
                value='${index}'><label>${element[0]}</label><br><br>`);
            });
            //將按鈕上的文字換成Next
            $("#startButton").attr("value","Next");
        }else{
            //已經開始作答從這裡繼續
            //巡訪哪個選項被選取
            $.each($(":radio"),function(i,val){
                if(val.checked){
                    //使用者所選取的項目是否已經到最後一題
                    if(isNaN(questions[currentQuiz].answers[i][1])){
                        //通往最終結果的路徑
                        var finalResult = questions[currentQuiz].answers[i][1];
                        //顯示最終結果的標題
                        $("#question").text(finalAnswers[finalResult][0]);
                        //清空選項區域
                        $("#options").empty();
                        //顯示最終結果的內容
                        $("#options").append(`${finalAnswers[finalResult][1]}<br>`);
                        currentQuiz=null;
                        $("#startButton").attr("value","Restart");
                    }else{
                        //指定下一個要顯示的題目，由於原始資料是從1開始算，所以要-1
                        currentQuiz=questions[currentQuiz].answers[i][1]-1;
                        //顯示新的題目
                        $("#question").text(questions[currentQuiz].question);
                        //清空選項區域
                        $("#options").empty();
                        //顯示新的選項
                        questions[currentQuiz].answers.forEach(function(element,index,array){
                            $("#options").append(`<input name='options' type='radio'
                            value='${index}'><label>${element[0]}</label><br><br>`);
                        });
                    }
                    return false; //跳離迴圈的方式
                }
            });
        }
    });
});