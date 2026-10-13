const chatModeNames = {
    'GEMINI': '聊天',
    'SEARCH_MOVIE': '查詢資料庫',
    'GUESS_MOVIE': '以圖搜尋',
    'SUB_TRANSLATE': '字幕翻譯 (提示：檔案大小愈大，翻譯時間愈長)'
};

function setChatMode(mode) {
    fetch(`/set_chat_mode/${mode}`, { method: 'POST' })
        .then(response => response.text())
        .then(data => {
            document.getElementById('current-mode').textContent = `目前模式: ${chatModeNames[mode]}`;
            document.getElementById('chat-box').innerHTML = ''; // 清空對話框

            const chatInputContainer = document.querySelector('.chat-input');
            const chatBoxContainer = document.querySelector('.chat-box');
            const subtitlesContainer = document.querySelector('.subtitles');
            
            if (mode === 'GUESS_MOVIE') {
                chatInputContainer.innerHTML = `
                    <label for="file-input" class="file-upload-label" style="border-radius: 10px 10px 10px 10px;">
                        <img src="./static/images/attachment.png" alt="Upload">
                        上傳檔案
                    </label>
                    <input type="file" id="file-input" style="display: none;" onchange="uploadFile()">
                `;
                chatInputContainer.style.display = 'flex';
                chatBoxContainer.style.display = 'flex';
                subtitlesContainer.style.display = 'none';
            }
            else if (mode === 'SEARCH_MOVIE') {
                chatInputContainer.innerHTML = `
                    <textarea style="border-radius: 10px 0px 0px 10px;" id="chat-input" placeholder="輸入電影名稱..." 
                    onkeydown="handleKeyDown(event)"></textarea>
                    <button onclick="sendMessage()">送出</button>
                `;   
                chatInputContainer.style.display = 'flex';
                chatBoxContainer.style.display = 'flex';
                subtitlesContainer.style.display = 'none';
            }
            else if (mode === 'GEMINI') {
                chatInputContainer.innerHTML = `
                    <label for="file-input" class="file-upload-label">
                        <img src="./static/images/attachment.png" alt="Upload">
                    </label>
                    <input type="file" id="file-input" style="display: none;" onchange="uploadFile()">
                    <textarea style="border-radius: 0px 0px 0px 0px;" id="chat-input" placeholder="輸入訊息..." 
                    onkeydown="handleKeyDown(event)"></textarea>
                    <button onclick="sendMessage()">送出</button>
                `;
                chatInputContainer.style.display = 'flex';
                chatBoxContainer.style.display = 'flex';
                subtitlesContainer.style.display = 'none';
            }
            else if (mode === 'SUB_TRANSLATE') {
                chatInputContainer.style.display = 'none';
                chatBoxContainer.style.display = 'none';
                subtitlesContainer.style.display = 'flex';
            }
        })
}

function handleKeyDown(event) {
    const textarea = event.target;
    const button = textarea.nextElementSibling; // 獲取緊接著的按鈕元素
    const label = textarea.previousElementSibling.previousElementSibling; // 獲取緊接著的標籤元素
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    } else {
        // 自動調整高度
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
        button.style.height = `${textarea.scrollHeight}px`; // 調整按鈕高度
        label.style.height = `${textarea.scrollHeight}px`; // 調整標籤高度
        label.style.lineHeight = `${textarea.scrollHeight}px`; // 調整標籤內部對齊
    }
}

function sendMessage() {
    const inputElement = document.getElementById('chat-input');
    const message = inputElement.value;
    if (message.trim() === '') return;

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.textContent = `你：${message}`;
    userMessage.className = 'chat-message user';
    chatBox.appendChild(userMessage);

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.textContent = `機器人：${data.reply}`;
        //格式化回覆訊息 /n就可以換行
        if(data.reply.includes("\n")){
            botMessage.innerHTML = data.reply.replace(/\n/g, "<br>");
        } else {
            botMessage.textContent = `機器人：${data.reply}`;
        }
        botMessage.className = 'chat-message bot';
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    inputElement.value = '';
}

function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    if (!file) return;

    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.className = 'chat-message user';

    if (file.type.startsWith('image/')) {
        // 如果是圖片類型，顯示圖片預覽
        const reader = new FileReader();
        reader.onload = function (e) {
            userMessage.innerHTML = `<img src="${e.target.result}" alt="${file.name}" style="max-width: 100%;">`;
            chatBox.appendChild(userMessage);
            chatBox.scrollTop = chatBox.scrollHeight; // 滾動到聊天框底部
        };
        reader.readAsDataURL(file); // 將檔案讀取為 Base64 資料 URI
    } else {
        // 如果不是圖片類型，顯示文字訊息
        userMessage.textContent = `你上傳了檔案：${file.name}`;
        chatBox.appendChild(userMessage);
        chatBox.scrollTop = chatBox.scrollHeight; // 滾動到聊天框底部
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.textContent = `機器人：${data.reply}`;
        //格式化回覆訊息 /n就可以換行
        if(data.reply.includes("\n")){
            botMessage.innerHTML = data.reply.replace(/\n/g, "<br>");
        } else {
            botMessage.textContent = `機器人：${data.reply}`;
        }
        botMessage.className = 'chat-message bot';
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}
