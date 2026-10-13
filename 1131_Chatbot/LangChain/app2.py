import google.generativeai as genai
from IPython.display import Image, display
from configparser import ConfigParser
import urllib.request

config = ConfigParser()
config.read("config.ini")

genai.configure(api_key=config["Gemini"]["API_KEY"])

# Upload the image files
image_urls = [
    "https://i.ibb.co/KyNtMw5/IMG-20240321-172354614-AE.jpg",
    "https://i.ibb.co/4Kmd21P/2024-07-20-11-26-25.png"
]
print(f"Uploading files...")
image_files = []
for url in image_urls:
    local_filename = url.split("/")[-1]
    urllib.request.urlretrieve(url, local_filename)
    image_file = genai.upload_file(path=local_filename)
    image_files.append(image_file)
    print(f"Completed upload: {image_file}")

prompt = """
圖片中的生物是什麼？
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", 
    system_instruction="使用繁體中文回答。"
)
response = model.generate_content([prompt] + image_files)
print(response.text)

print("Q: " + prompt)
print("A: " + response.text)

# Display the images
for url in image_urls:
    display(Image(url=url))

# 沒有要再問問題時，再把檔案從雲端刪除
# genai.delete_file(image_file.name)
# print(f"Deleted file {image_file.uri}")
