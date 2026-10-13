"""
從 config.ini 讀取設定檔，並且可以在任何地方 import config 取得設定值。
"""

import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

config["Line"]["USER_IMAGE_PATH"] = "uploads"
