const rest_name = '卡利西里'

//chatbot animation
$(document).ready(function() {
    $('#chatbot-button').click(function() {
        $('#chatbot-dialog').toggleClass('show');
    });
});

// 顯示本月的公休時間
$(document).ready(function() {
    function generateRestDays() { // 生成本月的公休日期
        let restDays = [];
        let date = new Date();
        // let date = new Date(2024, 6, 1); //for testing
        let month = date.getMonth();
        let year = date.getFullYear();

        date.setDate(1);

        while (date.getDay() !== 1) {
            date.setDate(date.getDate() + 1);
        }

        while (date.getMonth() === month) {
            restDays.push(new Date(date.getTime()));
            date.setDate(date.getDate() + 7);
        }

        return restDays;
    }

    // 將公休日期添加到#left_di元素中
    let restDays = generateRestDays();
    let restDaysString = restDays.map(date => `${date.getMonth() + 1}/${date.getDate()}`).join(', ');

    $(".left_di").append("&nbsp<h4>"+restDaysString+"</h4>");
    });

$(document).ready(function(){
    $("#submit-button").prop('disabled', true);
    $("#submit-button").css('background-color', 'grey');

    // gray out the submit button
    $("#submit-button").prop('disabled', true);
    function fetchData(queryUrl) {
        fetch(queryUrl)
            .then(response => response.json())
            .then(data => {
                $("#result-food-type").text(data["food_type"]);
                $("#result-food-name").text(data["food_name"]);
                $("#result-food-price").text(data["food_price"]);
            })
            .catch(error => {
                $("#result-food-type").text("NULL");
                $("#result-food-name").text("查詢錯誤");
                $("#result-food-price").text("N/A");
            });
    }

    $("#filter-button").click(function(event){
        // enable the submit button
        $("#submit-button").prop('disabled', false);
        $("#submit-button").css('background-color', '#ffffff');

        event.preventDefault();
        let queryUrl = '/query?';
        let foodType = $("input[name='food_type[]']:checked").val();
        queryUrl += `ft=${encodeURIComponent(foodType)}`;
        queryUrl += '&rs='+Math.random();
        fetchData(queryUrl);
    });

    $("#submit-button").click(function (event) {
        // 修改按鈕文字和狀態
        $("#submit-button").text('請稍候');
        $("#submit-button").prop('disabled', true);
        $("#submit-button").css('background-color', 'grey');

        // 等待0.5到2秒後改變按鈕文字
        setTimeout(function () {
            $("#submit-button").text('已送出');

            // 再次等待一小段時間，確保文字更新
            setTimeout(function () {
                // 顯示彈出視窗
                window.alert('成功送出訂單');

                // 重定向到新頁面
                // 檢測是否為 GitHub Pages（URL 包含 .html）或 Flask 環境
                const currentUrl = window.location.href;
                if (currentUrl.includes('.html') || currentUrl.includes('/demo/')) {
                    // GitHub Pages 環境：使用相對路徑
                    window.location.href = 'index.html';
                } else {
                    // Flask 環境：使用根路徑
                    window.location.href = '/';
                }
            }, 100); // 短暫等待100毫秒，確保按鈕文字更新
        }, Math.random() * 1500 + 500);
    });
});

$(document).ready(function() {
    document.getElementById('questionForm').addEventListener('submit', function (event) {
        event.preventDefault();

        // 取得輸入的問題
        const questionInput = document.getElementById('question');
        const question = questionInput.value;

        // 顯示輸入的問題並直接更新 <h2>
        const userQuestionTitle = document.getElementById('userQuestionTitle');
        userQuestionTitle.textContent = "您的問題: " + question;

        // 初始化 AI 回覆
        const responseBox = document.getElementById('responseBox');
        responseBox.textContent = "機器人思考中...";

        // 發送問題到後端並處理回應
        fetch('/call_llm_hint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'question': question
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    responseBox.textContent = "發生錯誤: " + data.error;
                } else {
                    responseBox.textContent = "回答: " + data.answer;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                responseBox.textContent = "發生錯誤，請稍後再試。";
            });

        // 清空輸入欄
        questionInput.value = '';
    });
});