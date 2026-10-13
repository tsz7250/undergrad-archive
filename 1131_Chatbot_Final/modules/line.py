import os, sys, shutil
import tempfile
from logging import Logger
from enum import Enum
from pyclbr import Function
from traceback import print_tb

from flask import Flask, request, abort

# custom modules    # 不確定直接 import modules 會不會有問題，但避免循環 import 還是先不要 import 全部
from modules.config import config
from modules import azure, gemini, tmdb

# line imports
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    AudioMessageContent,  # 新增這一行
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)


channel_access_token = config["Line"]["CHANNEL_ACCESS_TOKEN"]
channel_secret = config["Line"]["CHANNEL_SECRET"]
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

def _clean_user_images():
    global uploaded_images
    uploaded_images = []
    if os.path.exists(user_image_path):
        shutil.rmtree(user_image_path)  # 刪除整個資料夾
        os.makedirs(user_image_path)  # 重新建立空資料夾

user_image_path = os.path.normpath(config["Line"]["USER_IMAGE_PATH"])
if not os.path.exists(user_image_path):
    os.makedirs(user_image_path)
else:
    _clean_user_images()


def callback(app_logger: Logger) -> str:
    """
    LINE 驗證 Webhook URL 用的 callback
    """
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app_logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


class ChatMode(Enum):
    """
    聊天模式的列舉，包含：

    - GEMINI: 聊天
    - SEARCH_MOVIE: 查詢資料庫
    - GUESS_MOVIE: 以圖搜尋
    - SUB_TRANSLATE: 字幕翻譯
    """
    GEMINI = "聊天"
    SEARCH_MOVIE = "查詢資料庫"
    GUESS_MOVIE = "以圖搜尋"
    SUB_TRANSLATE = "字幕翻譯"


def foo(x):
    x = "command not implemented yet\nreceived: " + x
    print(x)
    return x


# 不同聊天模式的指令處理函數
CommandHandlers: dict = {
    ChatMode.GEMINI: gemini.chat,
    ChatMode.GUESS_MOVIE: foo,
    ChatMode.SEARCH_MOVIE: tmdb.search_movie_command,
    ChatMode.SUB_TRANSLATE: foo,
}


# default chat mode
chat_mode = ChatMode.GEMINI

# default command handler
command_handler = CommandHandlers[chat_mode]

# uploaded images path
uploaded_images: list[str] = []


def handle_text_message(event, text = None) -> None:
    r"""
    處理文字訊息的函數。

    當文字訊息為指令時，會切換聊天模式，並刪除所有已上傳的圖片。

    當文字訊息不是指令時，會根據目前聊天模式取得對應的處理函數並進行回應。
    """
    global chat_mode, command_handler, uploaded_images
    text = text if text else event.message.text
    result = ""

    # text is a command
    if text.startswith("@"):
        cmd = text[1:]
        try:
            new_chat_mode = ChatMode(cmd)
            if new_chat_mode != chat_mode:
                chat_mode = new_chat_mode
                command_handler = CommandHandlers[new_chat_mode]
                _clean_user_images()
            result = "聊天模式已切換至：" + chat_mode.value
            if(chat_mode == ChatMode.SEARCH_MOVIE):
                result += "\n請照格式輸入：\n<電影名稱>\n<問題>\例子:\nJohn Wick\n我想知道John Wick的導演和評價"
        except ValueError:
            result = "找不到指令：" + cmd
        except Exception as e:
            result = "發生錯誤：" + str(e)

    # text is not a command
    else:
        if chat_mode == ChatMode.GEMINI:
            result = gemini.chat(text, uploaded_images=uploaded_images)
        else:
            result = command_handler(text)

    # send response
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=result)]
            )
        )


#ffmpeg
import subprocess
import azure.cognitiveservices.speech as speechsdk
import time

# Azure Speech Settings
speech_config = speechsdk.SpeechConfig(subscription=config['AzureSpeech']['SPEECH_KEY'], 
                                       region=config['AzureSpeech']['SPEECH_REGION'])
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

def handle_audio_message(event) -> None:
    """
    處理 LINE bot 接收到的語音訊息，先用ppmpeg把line的音檔格式完全轉換成azure的wav，再使用 Azure Speech Services 進行語音轉文字。
    """
    # 取得 UserId（假設從 event 中取得）
    UserId = event.source.user_id

    # 取得語音內容
    with ApiClient(configuration) as api_client:
        blob_api = MessagingApiBlob(api_client)
        UserSendAudio = blob_api.get_message_content(event.message.id)
    
    # 儲存語音檔案到本地，使用時間戳避免覆蓋
    timestamp = int(time.time())  # 獲取當前時間戳

    # 儲存語音檔案到本地
    audio_dir = 'audio/'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    # 因為檔案名稱重複的話程式會卡住，所以檔案名稱要加上時間
    #audio_file_path = os.path.join(audio_dir, f'{UserId}.wav')
    audio_file_path = os.path.join(audio_dir, f'{UserId}_{timestamp}.wav')

    # 儲存語音內容
    with open(audio_file_path, 'wb') as fd:
        fd.write(UserSendAudio)

    # 確認檔案可以被正確讀取
    try:
        with open(audio_file_path, 'rb') as f:
            data = f.read()
        print("檔案讀取成功，檔案大小：", len(data))
    except Exception as e:
        print("無法讀取檔案：", e)
    #audio_file_path = f'{UserId}.wav'
    print(audio_file_path)
    
    # 輸出轉換後的音檔路徑
    #output_audio_file = os.path.join("modules", f"{UserId}_converted.wav")
    output_audio_file = os.path.join(audio_dir, f'{UserId}_{timestamp}_converted.wav')
    
    # 官網下載
    FFMPEG_PATH = "ffmpeg.exe"
    # 測試 FFmpeg 是否能運作
    try:
        subprocess.run([FFMPEG_PATH, "-version"], check=True)
        print("FFmpeg 運作正常！")
    except FileNotFoundError:
        print("找不到 FFmpeg，請檢查路徑是否正確！")
    except Exception as e:
        print(f"執行 FFmpeg 出錯：{e}")
    
     # 使用 FFmpeg 轉換音檔格式
    try:
        subprocess.run([
            FFMPEG_PATH, "-i", audio_file_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_audio_file
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"音檔轉換成功，儲存為: {output_audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"音檔轉換失敗: {e.stderr}")

    # 設定輸入音訊文件
    audio_config = speechsdk.audio.AudioConfig(filename=output_audio_file)
    
    print(audio_config)

    # 設定語言
    #speech_config.speech_recognition_language = "zh-TW"

    # 設定自動偵測語言，支援兩種以上語言
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["zh-TW", "en-US", "ja-JP"]  # 您要 Azure 偵測的語言列表
    )

    # 設定自動偵測語言，支援兩種以上語言
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["zh-TW", "en-US", "ja-JP"]  # 您要 Azure 偵測的語言列表
    )

    # 建立語音辨識器，啟用自動語言偵測
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
        auto_detect_source_language_config=auto_detect_source_language_config
    )

    # 執行語音轉文字
    print("正在進行語音轉文字...")
    result = speech_recognizer.recognize_once()

    # 處理結果
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"辨識結果：{result.text}")
            #return result.text
            handle_text_message(event, result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
            print("無法辨識語音內容。")
            #return "無法辨識語音內容"
    elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"語音轉文字過程被取消：{cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"詳細錯誤：{cancellation_details.error_details}")
            #return "語音轉文字失敗"

    # 回應使用者
    # with ApiClient(configuration) as api_client:
    #     line_bot_api = MessagingApi(api_client)
    #     line_bot_api.reply_message_with_http_info(
    #         ReplyMessageRequest(
    #             reply_token=event.reply_token,
    #             messages=[TextMessage(text=result.text)]
    #         )
    #     )
        


def handle_image_message(event) -> None:
    """
    處理圖片訊息的函數。

    當聊天模式為以圖搜尋時，上傳圖片後會立刻進行電影猜測，並且刪除所有已上傳的圖片。

    黨聊天模式為其他時，上傳圖片後會回傳已上傳圖片數量。
    """
    global uploaded_images
    UPLOAD_FOLDER="uploads"

    with ApiClient(configuration) as api_client:
        line_bot_blob_api = MessagingApiBlob(api_client)
        message_content = line_bot_blob_api.get_message_content(
            message_id=event.message.id
        )
        with tempfile.NamedTemporaryFile(
            dir=UPLOAD_FOLDER, prefix="", delete=False
        ) as tf:
            tf.write(message_content)
            tempfile_path = tf.name

    original_file_name = os.path.basename(tempfile_path + '.jpg')
    new_file_path = UPLOAD_FOLDER + "/" + original_file_name
    os.replace(tempfile_path, new_file_path)

    uploaded_images.append(new_file_path)

    uploaded_image_count = len(os.listdir(user_image_path))
    if chat_mode == ChatMode.GUESS_MOVIE:
        result = gemini.guess_movie(uploaded_images)
        _clean_user_images()
    else:
        result = f"上傳完成，已上傳 {uploaded_image_count} 張圖片"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=result)],
            )
        )