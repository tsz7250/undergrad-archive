document.getElementById('questionForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const questionInput = document.getElementById('question');
    const question = questionInput.value;
    document.getElementById('questionDisplay').innerText = "你的問題: " + question;
    document.getElementById('responseBox').innerText = "機器人思考中...";

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
            document.getElementById('responseBox').innerText = "發生錯誤: " + data.error;
        } else {
            document.getElementById('responseBox').innerText = "回答: " + data.answer;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('responseBox').innerText = "發生錯誤，請稍後再試。";
    });

    questionInput.value = '';
});
