import sys
import configparser

# Azure Text Analytics
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Azure Translation
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Azure Speech
import os
import azure.cognitiveservices.speech as speechsdk
import librosa

from flask import Flask, request, abort, render_template, url_for
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
    TextMessage,
    AudioMessage
)

# Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

# Config Azure Analytics
credential = AzureKeyCredential(config['AzureLanguage']['API_KEY'])

# Azure Speech Settings
speech_config = speechsdk.SpeechConfig(subscription=config['AzureSpeech']['SPEECH_KEY'], 
                                       region=config['AzureSpeech']['SPEECH_REGION'])
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
UPLOAD_FOLDER = 'static'

# Translator Setup
text_translator = TextTranslationClient(
    credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
    endpoint=config["AzureTranslator"]["EndPoint"],
    region=config["AzureTranslator"]["Region"],
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    audio_duration = azure_speech(event.message.text)
    translation_result, detected_language = azure_translate(event.message.text)
    # print(translation_result)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    AudioMessage(originalContentUrl=config["Deploy"]["URL"]+"/static/outputaudio.wav", duration=audio_duration),
                    TextMessage(text=translation_result),
                ],
            )
        )

def azure_speech(user_input):
    translated_text, translated_language  = azure_translate(user_input)
    # The language of the voice that speaks.
    if translated_language == "ja":
        speech_config.speech_synthesis_voice_name = "ja-JP-NanamiNeural"
        xml_lang = "ja-JP"
    elif translated_language == "zh-Hant" or translated_language == "zh-Hans":
        speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
        xml_lang = "zh-CN"
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename="static/" + file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config
    )
    
    # sentiment = azure_sentiment(user_input)    
    feelings = ["default", "chat", "cheerful", "customerservice"]

    for feeling in feelings:
        ssml_user_input = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="'+ xml_lang +'">'
        ssml_user_input += '<voice name="' + speech_config.speech_synthesis_voice_name + '">'
        ssml_user_input += '<mstts:express-as type="' + feeling + '" styledegree="2">'
        ssml_user_input += translated_text
        ssml_user_input += '</mstts:express-as>'
        ssml_user_input += '</voice>'
        ssml_user_input += '</speak>'
        
        print(ssml_user_input)
        
        # Receives a text from console input and synthesizes it to wave file.
        result = speech_synthesizer.speak_ssml_async(ssml_user_input).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            file_name = f"static/outputaudio_{feeling}.wav"
            with open(file_name, "wb") as audio_file:
                audio_file.write(result.audio_data)
            print(
                "Speech synthesized for text [{}], and the audio was saved to [{}]".format(
                    user_input, file_name
                )
            )
            audio_duration = round(
                librosa.get_duration(path=file_name) * 1000
            )
            print(audio_duration)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
    return audio_duration

def azure_sentiment(user_input):
    text_analytics_client = TextAnalyticsClient(
        endpoint=config['AzureLanguage']['END_POINT'], 
        credential=credential)
    documents = [user_input]
    response = text_analytics_client.analyze_sentiment(
        documents, 
        show_opinion_mining=True)
    print(response)
    docs = [doc for doc in response if not doc.is_error]
    for idx, doc in enumerate(docs):
        print(f"Document text : {documents[idx]}")
        print(f"Overall sentiment : {doc.sentiment}")
    return docs[0].sentiment
        
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
            target_languages = ["ja"]
        elif detected_language == "ja":
            target_languages = ["zh-Hant"]
        
        # 第二次翻譯請求以獲取翻譯結果
        response = text_translator.translate(
            body=input_text_elements, to_language=target_languages
        )
        translations = response[0].translations if response else None 
                
        if translations:
            return translations[0].text, target_languages[0]
        else:
            return user_input, detected_language  # 如果沒有翻譯結果，返回原始輸入
        
    except HttpResponseError as exception:
        print(f"ErrorCode: {exception.error}")
        print(f"Message: {exception.error.message}")
        return user_input  # 在發生錯誤時返回原始輸入

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/azure_translate", methods=["POST"])
def call_llm():
    if request.method == "POST":
        print("POST!")
        data = request.form
        print(data)
        input_text = data["message"]
        print(input_text)
        translation_result, original_language = azure_translate(input_text)
        audio_duration = azure_speech(input_text)
        return translation_result

if __name__ == "__main__":
    app.run()