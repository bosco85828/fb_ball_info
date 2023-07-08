#!/usr/bin python3
# -*- coding: utf-8 -*-
from pprint import pprint
import re
import json
from get_info import  get_info,get_api_info,get_game_id
from bs4 import BeautifulSoup
from datetime import datetime,timezone,timedelta
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os 
from analytics_img import get_offset


load_dotenv()
FB_ACCOUNT=os.getenv('FB_ACCOUNT')
FB_PASSWORD=os.getenv('FB_PASSWORD')

options = Options()
options.add_argument("--disable-notifications")    
# options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--enable-logging')
# options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')


path=os.getcwd()


global token
s=Service(ChromeDriverManager().install())
global browser
browser = webdriver.Chrome(service=s, options=options)
# browser.get("https://pc.yuanweiwang.top/login")
global wait
wait=WebDriverWait(browser,10)
browser.quit()
print(browser.service.is_connectable())