import requests
from IPython.display import Image

image_url = "https://i.ibb.co/KyNtMw5/IMG-20240321-172354614-AE.jpg"
content = requests.get(image_url).content
Image(content)


from configparser import ConfigParser
import os

# Set up config parser
config = ConfigParser()
config.read("config.ini")

# Set up Google Gemini API key
os.environ["GOOGLE_API_KEY"] = config["Gemini"]["API_KEY"]

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
# example
# image_url = "https://i.ibb.co/KyNtMw5/IMG-20240321-172354614-AE.jpg"
image1_url = "img1.jpeg"
image2_url = "img2.jpeg"
user_question = "請問這兩隻動物打架誰會嬴？"
user_question += " 請使用繁體中文回答。"
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": user_question,
        },  # You can optionally provide text parts
        {"type": "image_url", "image_url": image1_url},
        {"type": "image_url", "image_url": image2_url},
    ]
)
result = llm.invoke([message])
print("問：", user_question)
print("答：", result.content.lstrip(" "))

if "http" in image1_url:
    content = requests.get(image1_url).content
else:
    content = image1_url
Image(content)

if "http" in image2_url:
    content2 = requests.get(image2_url).content
else:
    content2 = image2_url
Image(content2)
