from flask import Flask, render_template, request, jsonify
from configparser import ConfigParser
import os
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

# Config Parser
config = ConfigParser()
config.read("config.ini")

os.environ["GOOGLE_API_KEY"] = config["Gemini"]["API_KEY"]
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/call_llm_hint", methods=["POST"])
def call_llm_hint():
    try:
        if request.method == "POST":
            question = request.form['question']
            logging.debug(f"Received question: {question}")
            # 模擬處理，這裡可以根據實際需要調用 llm.invoke 進行處理
            result = llm.invoke(question)
            return jsonify({'answer': result.content})
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
