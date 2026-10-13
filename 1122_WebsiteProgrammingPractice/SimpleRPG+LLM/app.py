from flask import Flask, render_template, url_for
from flask import request
from configparser import ConfigParser
import os

# Config Parser
config = ConfigParser()
config.read("config.ini")

os.environ["GOOGLE_API_KEY"] = config["Gemini"]["API_KEY"]
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro")
# gemini-1.5-flash-latest

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/call_llm_hint", methods=["POST"])
def call_llm_hint():
    if request.method == "POST":
        print("POST!")
        data = request.form
        print(data)
        result = llm.invoke("暗示在地圖右上角有蕃茄，不能說出蕃茄兩字")
        return result.content

@app.route("/call_llm_finish", methods=["POST"])
def call_llm_finish():
    if request.method == "POST":
        print("POST!")
        data = request.form
        print(data)
        result = llm.invoke("恭喜主角破關成功，不超過20字")
        return result.content