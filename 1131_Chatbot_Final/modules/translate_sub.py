import configparser
import os
import re
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from flask import Flask, request, send_file,render_template, send_file
import os

from modules import subtitle

# Config Parser
config = configparser.ConfigParser()
config.read("config.ini")

# Translator Setup
text_translator = TextTranslationClient(
    credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
    endpoint=config["AzureTranslator"]["EndPoint"],
    region=config["AzureTranslator"]["Region"],
)

app = Flask(__name__)

# 用來保存每個使用者的語言選擇
user_languages = {}

# 儲存翻譯後的 SRT 檔案名稱
translated_srt_filename = "translated_subtitles.srt"


def azure_translate(user_input, target_languages):
    try:
        # 使用者輸入文本進行翻譯
        input_text_elements = [user_input]

        # 進行多語言翻譯
        response = text_translator.translate(
            body=input_text_elements, to_language=target_languages
        )

        translations = response if response else []
        if translations:
            result = "\n".join([f" {trans.text}" for trans in translations[0].translations])
            return result
        else:
            return "翻譯失敗。"
    except HttpResponseError as exception:
        print(f"Error Code: {exception.error}")
        print(f"Message: {exception.error.message}")
        return "翻譯過程中發生錯誤。"

@app.route("/", methods=["GET"])
def index():
    # 返回上傳 SRT 檔案的表單頁面
    return render_template("index.html")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 確保 uploads 資料夾存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 清理與格式化 SRT 文件
# 清理與格式化 SRT 文件
def clean_and_format_srt(srt_lines):
    cleaned_lines = []
    previous_time_marker = None  # 記錄上一次的時間標記

    for line in srt_lines:
        # 移除每行開頭和結尾的空格
        line = line.strip()

        # 將 ' - >' 替換為 '-->'
        line = line.replace(" - >", " -->")
        
        # 將全形冒號替換為半形冒號
        line = line.replace("：", ":")
        line = line.replace(" ： ", " : ")

        # 檢查是否是時間軸
        time_marker_match = re.match(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", line)

        # 如果是時間軸，檢查是否與上一個時間軸相同
        if time_marker_match:
            if line == previous_time_marker:
                continue  # 如果時間軸相同，跳過這一行
            previous_time_marker = line  # 更新上一行的時間軸

        # 將時間軸拆開並比較
        time_lines = line.split("\n")
        if len(time_lines) == 1:
            line = line
        elif len(time_lines) >= 2:
            line1 = time_lines[0].strip()
            line2 = time_lines[1].strip()

            if line1 == line2:  # 如果兩個時間軸相同，則跳過第二個
                line = line1
            else:
                line = f"{line1}\n{line2}"
                
            if line1 == line2:  # 如果兩個時間軸相同，則跳過第二個
                line=line1 

        #line = line.strip()  # 去除每行前後的空白字符
        # 移除多餘的空行並加入內容
        if line:
            cleaned_lines.append(line)
        else:
            # 避免多個空行，只保留一個空行
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")

    # 最後將字幕段落組合回正確格式
    final_output = []
    block = []
    for line in cleaned_lines:
        if line == "":
            if block:  # 處理每段字幕
                final_output.append("\n".join(block))
                block = []
        else:
            block.append(line)

    if block:  # 處理最後一段字幕
        final_output.append("\n".join(block))

    return "\n\n".join(final_output)


# 處理 SRT 檔案翻譯與格式化
@app.route("/translate_srt", methods=["POST"])
def translate_srt():
    file = request.files.get("file")
    target_languages = request.form.get("languages").split(" ")  # 接收語言列表

    if file and target_languages:
        # 儲存原始檔案
        video_file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(video_file_path)
        subtitle.video_to_subtitle(video_file_path, f'outputs/{file.filename}.srt')

        # 讀取 SRT 檔案內容
        srt_file_path = os.path.join('outputs', f'{file.filename}.srt')
        # file.save(srt_file_path)

        # 讀取 SRT 檔案內容
        with open(srt_file_path, "r", encoding="utf-8") as f:
            srt_lines = f.readlines()

        # 逐行翻譯字幕內容
        translated_lines = []
        for line in srt_lines:
            if line.strip() and not re.match(r"^\d+$", line.strip()):  # 忽略純數字行
                translated_text = azure_translate(line.strip(), target_languages)
                translated_lines.append(translated_text)
            else:
                translated_lines.append(line.strip())

        # 格式化翻譯後的字幕內容
        formatted_srt_content = clean_and_format_srt(translated_lines)
        
        # 保存翻譯與格式化後的 SRT 檔案
        # translated_srt_filename = f"translated_{file.filename}"
        # translated_srt_path = os.path.join(app.config["UPLOAD_FOLDER"], translated_srt_filename)
        with open(srt_file_path, "w", encoding="utf-8") as f:
            f.write(formatted_srt_content)

        subtitle.embed_subtitles('uploads', file.filename, f'../outputs/{file.filename}.srt', f'subtitled_{file.filename}')

        return send_file(f'uploads/subtitled_{file.filename}', as_attachment=True)

    return "請提供 SRT 檔案及語言選擇。"


if __name__ == "__main__":
    app.run()
