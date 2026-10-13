from ffmpeg import output
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import shutil

# custom modules
from modules.config import config
from modules import line, gemini, subtitle
from modules.gemini import guess_movie
from modules.translate_sub import translate_srt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# 創建上傳文件夾
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def clean_uploads_folder():
    """
    清空 uploads 文件夾
    """
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route("/callback", methods=["POST"])
def callback():
    """
    LINE bot 驗證 Webhook URL 用的 callback
    """
    return line.callback(app.logger)

@line.handler.add(line.MessageEvent, message=line.TextMessageContent)
def handle_text_message(event):
    """
    LINE bot 接收並處理文字訊息
    """
    return line.handle_text_message(event)

@line.handler.add(line.MessageEvent, message=line.ImageMessageContent)
def handle_image_message(event):
    """
    LINE bot 接收並處理圖片訊息
    """
    return line.handle_image_message(event)

@line.handler.add(line.MessageEvent, message=line.AudioMessageContent)
def handle_audio_message(event):
    """
    LINE bot 接收並處理audio訊息
    """
    return line.handle_audio_message(event)

@app.route('/set_chat_mode/<mode>', methods=['POST'])
def set_chat_mode(mode):
    """
    設定聊天模式
    """
    try:
        new_chat_mode = line.ChatMode[mode]
        line.chat_mode = new_chat_mode
        line.command_handler = line.CommandHandlers[new_chat_mode]
        line._clean_user_images()
        clean_uploads_folder()  # 清空 uploads 文件夾
        return f"聊天模式已切換至：{new_chat_mode.value}"
    except KeyError:
        return f"無效的聊天模式：{mode}", 400

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    處理來自網頁的聊天訊息
    """
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'reply': '請輸入訊息'}), 400

    # 使用當前的聊天模式處理訊息
    if line.chat_mode == line.ChatMode.GEMINI:
        reply = gemini.chat(message, line.uploaded_images)
    else:
        reply = line.command_handler(message)
    return jsonify({'reply': reply})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """
    處理文件上傳
    """
    if 'file' not in request.files:
        return jsonify({'reply': '沒有檔案被上傳'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'reply': '沒有選擇檔案'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        line.uploaded_images.append(file_path)

        if line.chat_mode == line.ChatMode.GUESS_MOVIE:
            reply = gemini.guess_movie([file_path])
        if line.chat_mode == line.ChatMode.SUB_TRANSLATE:
            # create outputs folder
            if not os.path.exists('outputs'):
                os.makedirs('outputs')
            output_path = os.path.abspath('outputs').replace("\\", "/")
            input_file_path = os.path.abspath(file_path).replace("\\", "/")
            output_video_path = os.path.abspath(f'uploads/subtitled_{filename}').replace("\\", "/")
            subtitle_path = f'outputs/{filename}.srt'
            subtitle.video_to_subtitle(input_file_path, subtitle_path)

            # generate subtitled video

            subtitle.embed_subtitles(output_path, input_file_path, f'{filename}.srt', output_video_path)
            reply = request.url_root + f'uploads/subtitled_{filename}'
        else:
            reply = f'檔案 {filename} 上傳成功'

        return jsonify({'reply': reply, 'filename': filename})

    return jsonify({'reply': '檔案上傳失敗'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    提供上傳文件的路由
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def hello_world():
    """
    網頁測試，測試是否能讀取 config 並回傳 template
    """
    return render_template(
        template_name_or_list='index.html',
        msg=config['test']['message'],
        chat_mode=line.chat_mode.value
    )
    
@app.route('/translate_srt', methods=['POST'])
def call_translate_srt():
    return translate_srt()

if __name__ == '__main__':
    app.run()
