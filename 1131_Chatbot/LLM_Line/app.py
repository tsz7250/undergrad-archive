import sys
import configparser
import os, tempfile

# Gemini API SDK
import google.generativeai as genai

# image processing
import PIL

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
)

# Config Parser
config = configparser.ConfigParser()
config.read("config.ini")

# Gemini API Settings
genai.configure(api_key=config["Gemini"]["API_KEY"])

llm_role_description = """
使用繁體中文來回答問題。
"""

# Check available models
# print("Available models:")
# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(f"{m.name} (Generate Content)")
#     else:
#         print(f"{m.name} (Other purpose)")

# Use the model
from google.generativeai.types import HarmCategory, HarmBlockThreshold
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmBlockThreshold.BLOCK_NONE,
    },
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    },
    system_instruction=llm_role_description,
)

UPLOAD_FOLDER="static"

app = Flask(__name__)

channel_access_token = config["Line"]["CHANNEL_ACCESS_TOKEN"]
channel_secret = config["Line"]["CHANNEL_SECRET"]
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(access_token=channel_access_token)

is_image_uploaded=False


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    gemini_result = gemini_llm_sdk(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=gemini_result)],
            )
        )
        
uploaded_images = []
        
@handler.add(MessageEvent, message=ImageMessageContent)
def message_image(event):
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

    finish_message = f"上傳完成，目前已上傳 {len(uploaded_images)} 張照片。請問你想要問關於這些照片的什麼問題呢？"
    
    global is_image_uploaded
    is_image_uploaded=True

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=finish_message)],
            )
        )


def gemini_llm_sdk(user_input):
    try:
        if is_image_uploaded:
            print("Image is uploaded.")
            print(f"Uploaded images: {uploaded_images}")
            upload_images = [PIL.Image.open(image_path) for image_path in uploaded_images]
            response = model.generate_content([user_input] + upload_images)
        else:
            response = model.generate_content(user_input)
        print(f"Question: {user_input}")
        print(f"Answer: {response.text}")
        return response.text
    except Exception as e:
        print(e)
        return "Gemini AI故障中。"
    
# 處理完圖片後刪除它們
for image_path in uploaded_images:
    genai.delete_file(image_path)
    print(f"Deleted file {image_path}")
# 清空 uploaded_images 列表
uploaded_images.clear()

if __name__ == "__main__":
    app.run()
