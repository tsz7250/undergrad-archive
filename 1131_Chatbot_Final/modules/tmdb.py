import requests
import configparser
import os
from datetime import datetime
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from modules import gemini

class MovieSearch:
    def __init__(self, config_path=None):
        """
        初始化 MovieSearch 類別
       
        :param config_path: config.ini 檔案路徑
        """
        # 如果沒有指定路徑，使用預設路徑
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
       
        # 使用 UTF-8 編碼讀取配置文件
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
       
        # 確保成功讀取 API key
        try:
            self.tmdb_api_key = config['TMDB']['API_KEY']
            self.azure_key = config['AzureTranslator']['Key']
            self.azure_region = config['AzureTranslator']['Region']
            self.azure_endpoint = config['AzureTranslator']['Endpoint']
        except KeyError as e:
            raise ValueError(f"未在 config.ini 中找到 {str(e)} 配置")
       
        self.base_url = "https://api.themoviedb.org/3"
        
        # 初始化 Azure 翻譯客戶端
        try:
            # 使用新的初始化方式
            self.translator = TextTranslationClient(
                credential = AzureKeyCredential(self.azure_key),
                endpoint = self.azure_endpoint,
                region = self.azure_region
            )
        except Exception as e:
            print(f"Azure 翻譯客戶端初始化錯誤: {e}")
            self.translator = None

    def _detect_language(self, text):
        """
        偵測輸入文本的語言
        :param text: 要偵測語言的文本
        :return: 語言代碼
        """
        if not self.translator:
            return 'und'  # 未知語言
        
        try:
            response = self.translator.detect_language(body=[text])
            if response and response[0].language:
                return response[0].language
            return 'und'
        except Exception as e:
            print(f"語言偵測失敗: {e}")
            return 'und'

    def _translate_text(self, text, target_language='zh-Hant'):
        """
        使用 Azure 翻譯文本
        :param text: 要翻譯的文本
        :param target_language: 目標語言代碼
        :return: 翻譯後的文本
        """ 
        if not self.translator or not text:
            print("Azure 翻譯器未初始化或文本為空")
            return text

        try:
            # 如果文本已經是中文，直接返回
            if self._detect_language(text) in ['zh-Hant', 'zh-Hans', 'zh']:
                return text

            # 翻譯
            response = self.translator.translate(
                body = [text], 
                to_language = [target_language]
            )
            # 返回第一個翻譯結果
            if response and response[0].translations:
                return response[0].translations[0].text
            else:
                print("未找到翻譯結果")
                return text
        except Exception as e:
            print(f"翻譯失敗: {e}")
            return text

    def _get_movie_reviews(self, movie_id):
        """
        獲取電影評論
        :param movie_id: TMDB 電影 ID
        :return: 電影評論列表
        """
        try:
            reviews_url = f"{self.base_url}/movie/{movie_id}/reviews?api_key={self.tmdb_api_key}&language=en-US"
            reviews_response = requests.get(reviews_url)
            
            if reviews_response.status_code != 200:
                print(f"獲取電影評論時發生錯誤：{reviews_response.status_code}")
                return []
            
            reviews_data = reviews_response.json()
            
            # 翻譯每則評論
            translated_reviews = []
            for review in reviews_data.get('results', []):
                translated_content = self._translate_text(review['content'])
                translated_reviews.append({
                    'author': review['author'],
                    'content': translated_content,
                    'rating': review.get('author_details', {}).get('rating', '無')
                })
            
            return translated_reviews
        
        except Exception as e:
            print(f"獲取電影評論時發生未預期的錯誤：{str(e)}")
            return []

    def search_movie(self, movie_name):
        """
        搜尋電影並獲取詳細資訊
        :param movie_name: 電影名稱
        :return: 電影詳細資訊字典
        """
        try:
            # 偵測並翻譯電影名稱（如果不是中文）
            # detected_lang = self._detect_language(movie_name)
            # if detected_lang not in ['zh-Hant', 'zh-Hans', 'zh']:
            #     movie_name = self._translate_text(movie_name, 'en')
            
            # 第一步：搜尋電影
            search_url = f"{self.base_url}/search/movie?api_key={self.tmdb_api_key}&query={movie_name}&language=zh-TW"
            search_response = requests.get(search_url)
            if search_response.status_code != 200:
                return f"搜尋電影時發生錯誤：{search_response.status_code}"
            search_data = search_response.json()
           
            # 如果沒有找到電影
            if not search_data['results']:
                return "找不到相關電影"
            
            # 取第一個搜尋結果的電影 ID
            movie_id = search_data['results'][0]['id']
            
            # 第二步：獲取電影詳細資訊
            details_url = f"{self.base_url}/movie/{movie_id}?language=zh-TW&api_key={self.tmdb_api_key}&append_to_response=credits,releases,keywords,alternative_titles,translations,external_ids"
            details_response = requests.get(details_url)
            if details_response.status_code != 200:
                return f"獲取電影詳細資訊時發生錯誤：{details_response.status_code}"
            movie_details = details_response.json()
            
            # 獲取電影評論
            movie_reviews = self._get_movie_reviews(movie_id)
            
            # 翻譯電影名稱
            # translated_title = self._translate_text(movie_details['title'])
            translated_title = movie_details['title']
            
            # 翻譯劇情簡介
            # translated_overview = self._translate_text(movie_details['overview'])
            translated_overview = movie_details['overview']
            
            # 提取導演
            directors = [crew['name'] for crew in movie_details.get('credits', {}).get('crew', [])
                         if crew['job'] == 'Director']
            # director = self._translate_text(directors[0]) if directors else "無資訊"
            director = directors[0] if directors else "無資訊"
            
            # 提取主演並翻譯
            actors = [actor['name'] for actor in movie_details.get('credits', {}).get('cast', [])[:3]]
            # translated_actors = [self._translate_text(actor) for actor in actors]
            translated_actors = actors
            # main_actors = "、".join(translated_actors) if translated_actors else "無資訊"
            main_actors = "、".join(actors) if actors else "無資訊"
            
            # 取得上映年份的中文格式
            release_date = datetime.strptime(movie_details['release_date'], "%Y-%m-%d")
            formatted_release_date = release_date.strftime("%Y年%m月%d日")
            
            # 產生類型列表
            genres = [genre['name'] for genre in movie_details.get('genres', [])]
            # translated_genres = [self._translate_text(genre) for genre in genres]
            translated_genres = genres
            genres_str = "、".join(translated_genres) if translated_genres else "無資訊"
            
            # 製作國家
            production_countries = [country['name'] for country in movie_details.get('production_countries', [])]
            countries_str = "、".join(production_countries) if production_countries else "無資訊"
            
            # 製片公司
            production_companies = [company['name'] for company in movie_details.get('production_companies', [])]
            companies_str = "、".join(production_companies) if production_companies else "無資訊"
            
            # 語言
            original_language = movie_details.get('original_language', '無資訊')
            spoken_languages = [lang['name'] for lang in movie_details.get('spoken_languages', [])]
            languages_str = "、".join(spoken_languages) if spoken_languages else "無資訊"
            
            # 電影狀態
            status_mapping = {
                'Released': '已上映',
                'Upcoming': '即將上映',
                'In Production': '製作中',
                'Canceled': '已取消'
            }
            movie_status = status_mapping.get(movie_details.get('status', ''), '未知')
            
            # 預算與票房
            budget = movie_details.get('budget', 0)
            revenue = movie_details.get('revenue', 0)
            
            # 處理電影評論
            reviews_section = ""
            
            # 查詢英文評論，並翻譯成中文
        
            if movie_reviews:
                # 取前三則或全部評論
                display_reviews = movie_reviews[:3] if len(movie_reviews) > 3 else movie_reviews
                reviews_section = "🎬 電影評價:\n"
                for idx, review in enumerate(display_reviews, 1):
                    reviews_section += f"評論 {idx}:\n"
                    reviews_section += f"👤 作者: {review['author']}\n"
                    if review['rating'] != '無':
                        reviews_section += f"⭐ 評分: {review['rating']}/10\n"
                        sentiment = azure_sentiment(review['content'])
                    reviews_section += f"💬 內容: {review['content']}\n分析結果：{sentiment}\n\n"
            else:
                reviews_section = "🎬 電影評價: 這部電影還沒有人評論\n"
            
            # 格式化回覆訊息
            message = f"""🎬 電影基本資訊:
📝 電影名稱: {translated_title}
🌍 原始語言: {original_language.upper()}
⭐ 電影評分: {movie_details['vote_average']}/10

📊 評價統計:
🔢 總投票數: {movie_details['vote_count']} 票

📅 上映資訊:
🗓️ 上映日期: {formatted_release_date}
📊 電影狀態: {movie_status}

👥 創作團隊:
🎥 導演: {director}
🌟 主演: {main_actors}

🎭 電影類型: {genres_str}

📍 製作資訊:
🌐 製作國家: {countries_str}
🏢 製片公司: {companies_str}
🗣️ 電影語言: {languages_str}

📖 劇情簡介: 
{translated_overview}

💰 財務資訊:
💸 電影預算: ${budget:,} USD
💰 全球票房: ${revenue:,} USD

{reviews_section}
"""
            return message
       
        except Exception as e:
            return f"搜尋電影時發生未預期的錯誤：{str(e)}"

def search_movie_command(movie_name):
    '''
    用於 Line Bot 的電影搜尋命令處理函數
   
    :param movie_name: 電影名稱
    :return: 電影資訊訊息
    '''
    # 如果有使用者輸入，則分離電影名稱和使用者輸入，但可能只有一行電影名稱
    user_input = None
    if '\n' in movie_name:
        movie_name, user_input = movie_name.split('\n', 1)
    movie_searcher = MovieSearch()
    movie_info = movie_searcher.search_movie(movie_name)
    if user_input:
        return gemini.db_query(movie_info, user_input)
    else:
        return movie_info
    
def get_movie_overview(movie_name):
    """
    獲取電影的劇情簡介
    :param movie_name: 電影名稱
    :return: 劇情簡介
    """
    try:
        movie_searcher = MovieSearch()
        # 搜尋電影
        search_url = f"{movie_searcher.base_url}/search/movie?api_key={movie_searcher.tmdb_api_key}&query={movie_name}&language=zh-TW"
        search_response = requests.get(search_url)
        if search_response.status_code != 200:
            return f"搜尋電影時發生錯誤：{search_response.status_code}"
        search_data = search_response.json()
        
        # 如果沒有找到電影
        if not search_data['results']:
            return "找不到相關電影"
        
        # 取第一個搜尋結果的電影 ID
        movie_id = search_data['results'][0]['id']
        
        # 獲取電影詳細資訊
        details_url = f"{movie_searcher.base_url}/movie/{movie_id}?language=zh-TW&api_key={movie_searcher.tmdb_api_key}"
        details_response = requests.get(details_url)
        if details_response.status_code != 200:
            return f"獲取電影詳細資訊時發生錯誤：{details_response.status_code}"
        movie_details = details_response.json()
        
        # 返回劇情簡介
        return movie_details.get('overview', '無劇情簡介')
    
    except Exception as e:
        return f"獲取電影劇情簡介時發生未預期的錯誤：{str(e)}"
    
def azure_sentiment(user_input):
    #Config Parser
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    #Config Azure Analytics
    credential = AzureKeyCredential(config['AzureLanguage']['API_KEY'])
    
    text_analytics_client = TextAnalyticsClient(
        endpoint=config['AzureLanguage']['END_POINT'], 
        credential=credential)
    documents = [user_input]
    response = text_analytics_client.analyze_sentiment(
        documents, 
        show_opinion_mining=True,
        language="zh-hant")
    print(response)
    docs = [doc for doc in response if not doc.is_error]
    result = f"整體：{docs[0].sentiment}\n"
    for idx, doc in enumerate(docs):
        for sentence_idx, sentence in enumerate(doc.sentences):
            opinions = ", ".join([opinion.target.text for opinion in sentence.mined_opinions])
            result += f"{sentence_idx}：{opinions if opinions else 'N/A'} => {sentence.sentiment}\n"
        print(f"Document text : {documents[idx]}")
        print(f"Overall sentiment : {doc.sentiment}")
    return docs[0].sentiment
    # sentiment = docs[0].sentiment
    # scores = docs[0].confidence_scores
    # return result.strip()