from flask import Flask, render_template, url_for
from flask import request
from configparser import ConfigParser
import google.generativeai as genai

# Config Parser
config = ConfigParser()
config.read("config.ini")

genai.configure(api_key=config["Gemini"]["API_KEY"])

from google.generativeai.types import HarmCategory, HarmBlockThreshold

llm = genai.GenerativeModel(
    "gemini-1.5-flash-latest",
    system_instruction="請用繁體中文回答。",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    },
)
chat = llm.start_chat(history=[])
# Please replace the content with your own role description
role = """
妳是一個二十五歲的年輕女性，喜歡游泳和閱讀。
妳聊天的目的是為了請對方送妳一份禮物。
以下是對方問的問題，你直接用這個角色回答就好，不用再舉例。
"""

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/call_llm", methods=["POST"])
def call_llm():
    if request.method == "POST":
        print("POST!")
        data = request.form
        print(data)
        to_llm = ""
        if len(chat.history) > 0:
            to_llm = data["message"]
        else:
            to_llm = role + data["message"]
        try:
            result = chat.send_message(to_llm)
        except Exception as e:
            print(e)
            return "我媽來了，她說不能聊這個(雙手比叉)"
        print(chat.history)
        # remove \n at the end of the result
        return result.text.replace("\n", "")