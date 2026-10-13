import sys
import configparser

# Azure Translation
from azure.ai.translation.text import TextTranslationClient
# from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

#Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

# Translator Setup
text_translator=TextTranslationClient(
    credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
    endpoint=config["AzureTranslator"]["EndPoint"],
    region=config["AzureTranslator"]["Region"],
    )

app = Flask(__name__)

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN']
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    translation_result, translation_result_2 = azure_translate(event.message.text)
    print(translation_result)
    print(translation_result_2)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=translation_result),
                    TextMessage(text=translation_result_2)
                ],
            )
        )
        
def azure_translate(user_input):
    try:
        # 初始目標語言設置為日文和中文
        target_languages = ["ja", "zh-Hant"]
        input_text_elements = [user_input]
        
        # 第一次翻譯請求以檢測輸入語言
        response = text_translator.translate(
            body=input_text_elements, to_language=target_languages
        )       
        detected_language = response[0].detected_language.language
        
        # 根據檢測到的語言設置目標語言
        if detected_language == "zh-Hans" or detected_language == "zh-Hant":
            target_languages = ["ja-Latn", "ja"]
        elif detected_language == "ja":
            target_languages = [ "zh-Latn", "zh-Hant"]
        
        # 第二次翻譯請求以獲取翻譯結果
        response = text_translator.translate(
            body=input_text_elements, to_language=target_languages
        )
        print(response)
        translations = response[0].translations if response else None 
                
        if translations:
            return translations[0].transliteration.text, translations[1].text
        
    except HttpResponseError as exception:
        print(f"ErrorCode: {exception.error}")
        print(f"Message: {exception.error.message}")

if __name__ == "__main__":
    app.run()