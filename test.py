#!/usr/bin python3
# -*- coding: utf-8 -*-
from get_info import get_info 
from bs4 import BeautifulSoup
from datetime import datetime,timezone,timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
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
YC_PASSWORD=os.getenv('YC_PASSWORD')

options = Options()
options.add_argument("--disable-notifications")    
# options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless") 

path=os.getcwd()

def login():

    s=Service(ChromeDriverManager().install())
    global browser
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://www.s3.com.tw/")
    global wait
    wait=WebDriverWait(browser,10)
    
    locator=(By.XPATH,'//body')
    data=wait.until(EC.presence_of_element_located(locator)).get_attribute("outerHTML")
    print(data)

    
    browser.quit()

login()
    
