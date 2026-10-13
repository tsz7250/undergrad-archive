import json
from configparser import ConfigParser
from langchain_google_genai import ChatGoogleGenerativeAI


class LLM:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")
        self.llm = ChatGoogleGenerativeAI(
            model=self.config["Gemini"]["model"],
            google_api_key=self.config["Gemini"]["API_KEY"]
        )
        self.menu = self.load_menu("static/json/database.json")
        
    def load_menu(self, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            menu = json.load(file)
        return menu

    def invoke(self, text: str):
        menu_info = self.format_menu_info()
        background = f"你是一名西餐廳的服務生，檔案入面是餐廳有的食物。以下是餐廳的菜單：{menu_info}。現在你要回答客人的需求。回答不能多於20字。"
        result = self.llm.invoke(background + text)
        return result
    
    def format_menu_info(self):
        menu_str = ""
        for food_type in self.menu["rest_menu"]:
            menu_str += f"{food_type['food_type_name']}: "
            items = [f"{item['food_name']}({item['food_price']}元)" for item in food_type["food_type_menu"]]
            menu_str += ", ".join(items) + ". "
        return menu_str.strip()
