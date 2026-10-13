import os.path

from modules.config import config
from modules import tmdb

import PIL.Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


# Gemini API Settings
genai.configure(api_key=config["Gemini"]["API_KEY"])


####################################################################################################
# Continuous chat
####################################################################################################


chat_model_instruction = """
用戶跟你用甚麼語言，你就用甚麼語言來回答問題。
你是一個資深電影迷，你擅長回答關於電影的一切問題，
你也很會推薦電影給別人。
"""


# base model
chat_model = genai.GenerativeModel(
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
    system_instruction=chat_model_instruction,
)


chat_session = chat_model.start_chat(history=[])


def chat(user_input: str, uploaded_images: list[str] = None) -> str:
    """
    與有記憶的 Gemini 對話。
    :param user_input: 使用者輸入的文字，不可以是 None
    :param uploaded_images: 使用者上傳的圖片，可以是 None
    :return: Gemini 的回應
    """
    if uploaded_images:
        uploaded_images = [PIL.Image.open(image_path) for image_path in uploaded_images]
        user_input = [user_input] + uploaded_images
    try:
        response = chat_session.send_message(user_input)
        print(f"Question: {user_input}")
        print(f"Answer: {response.text}")
        return response.text
    except ValueError:
        return response.prompt_feedback
    except Exception as e:
        return str(e)


def new_chat():
    """
    開始新的對話。
    """
    global chat_session
    chat_session = chat_model.start_chat(history=[])


####################################################################################################
# Database query
####################################################################################################


db_query_instruction = """
你是一個協助回答電影相關問題的聊天機器人，會提供給你電影的資訊，以及使用者的問題。
"""


# base model
db_query_model = genai.GenerativeModel(
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
    system_instruction=db_query_instruction,
)


def db_query(movie_info: str, user_input: str) -> str:
    """
    與 Gemini 對話
    :param movie_info:
    :param user_input:
    :return:
    """
    user_input = f'電影資訊：\n{movie_info}\n使用者的問題：\n{user_input}'
    try:
        response = db_query_model.generate_content(user_input)
        print(f"Question: {user_input}")
        print(f"Answer: {response.text}")
        return response.text
    except ValueError:
        return response.prompt_feedback
    except Exception as e:
        return str(e)


####################################################################################################
# Guess movie
####################################################################################################


# user image path
user_image_path = os.path.normpath(config["Line"]["USER_IMAGE_PATH"])

movie_guess_prompt = """
請使用繁體中文回答。第一行是你的信心指數，介於0~1。第二行為你的猜測。如果你的信心指數低於0.5，則增加第三行為你的理由。
"""

movie_guess_model = genai.GenerativeModel(
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
    system_instruction=movie_guess_prompt,
)


def guess_movie(uploaded_images, user_input: str = "你覺得圖片是哪部電影？") -> str:
    try:
        print("Image is uploaded.")
        print(f"Uploaded images: {uploaded_images}")
        upload_images = [PIL.Image.open(image_path) for image_path in uploaded_images]
        response = movie_guess_model.generate_content([user_input] + upload_images)
        response_text = response.text.splitlines()
        confidence_index = float(response_text[0])
        guessed_name = response_text[1]
        print(f"Question: {user_input}")
        print(f"Answer: {response.text}")
        if(confidence_index > 0.5):
            tmdb_response = tmdb.get_movie_overview(guessed_name)
            string = f'{guessed_name}\n簡介：\n{tmdb_response}\n'
            return string
        else:
            reason = response_text[2]
            string = f'信心指數：{confidence_index}\n猜測：{guessed_name}\n理由：{reason}'
            return confidence_index, guessed_name, reason
    except Exception as e:
        print(e)
        return "Gemini AI故障中。"
