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
# options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--enable-logging')
# options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless") 

path=os.getcwd()

def login():

    s=Service(ChromeDriverManager().install())
    global browser
    browser = webdriver.Chrome(service=s, options=options)
    browser.get("https://pc.yuanweiwang.top/login")
    global wait
    wait=WebDriverWait(browser,10)

    locator=(By.ID,"accountLogin_signName")
    account=wait.until(EC.presence_of_element_located(locator))

    locator=(By.ID,"accountLogin_password")
    password=wait.until(EC.presence_of_element_located(locator))

    account.send_keys(FB_ACCOUNT)
    password.send_keys(FB_PASSWORD)

    locator=(By.XPATH,'//button[1]')
    submit=wait.until(EC.element_to_be_clickable(locator))
    submit.click()
    while True : 
        try : 
            locator=(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/img')
            close=wait.until(EC.element_to_be_clickable(locator))
            close.click()
            break
        except : 
            locator=(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]')
            img=wait.until(EC.presence_of_element_located(locator))
            img_url=img.get_attribute('style').split('\"')[1]
            print(img_url)
            get_img(img_url)

            locator=(By.XPATH,'/html/body/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div')
            cursor=wait.until(EC.presence_of_element_located(locator))

            move=ActionChains(browser)
            move.click_and_hold(cursor)
            move.move_by_offset((get_offset()-15),0)

            move.release()
            move.perform()
            time.sleep(3)
    
    # locator=(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[1]/div[2]")
    locator=(By.XPATH,'//div[@class="game-item"]')
    sport=wait.until(EC.presence_of_element_located(locator))

    action=ActionChains(browser)
    action.move_to_element(sport)
    action.perform()

    locator=(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/img')
    fb_link=wait.until(EC.element_to_be_clickable(locator))
    fb_link.click()

    data={}
    time.sleep(3)
    # print(browser.requests)
    browser.get("https://ipc.wtpssfwed.com/index.html#/")
    time.sleep(3)
    # print(browser.last_request)
    for i in browser.requests :
        # print(i) 
        if "getList" in str(i) : 
            print(i)
            if i.headers['Authorization'] : 
                token=i.headers['Authorization']
                return token 
    

def main():
    token=login()
    data={}
    while True : 
        count=0
        
        soccer_id_list=get_game_id(token,'1')
        if soccer_id_list == "failed" : 
            token=login()
            continue

        data['soccer']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=1",'soccer',soccer_id_list)

        basketball_id_list=get_game_id(token,'3')
        if basketball_id_list == "failed" : 
            token=login()
            continue
        
        data['basketball']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=3",'basketball',basketball_id_list)

        baseball_id_list=get_game_id(token,'7')
        if baseball_id_list == "failed" : 
            token=login()
            continue

        data['baseball']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=7",'baseball',baseball_id_list)

        tennis_id_list=get_game_id(token,'5')
        if tennis_id_list == "failed" : 
            token=login()
            continue

        data['tennis']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=5",'tennis',tennis_id_list)

        volleyball_id_list=get_game_id(token,'13')
        if volleyball_id_list == "failed" : 
            token=login()
            continue

        data['volleyball']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=13",'volleyball',volleyball_id_list)

        badminton_id_list=get_game_id(token,'47')
        if badminton_id_list == "failed" : 
            token=login()
            continue

        data['badminton']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=47",'badminton',badminton_id_list)

        football_id_list=get_game_id(token,'4')
        if football_id_list == "failed" : 
            token=login()
            continue

        data['football']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=4",'football',football_id_list)

        table_tennis_id_list=get_game_id(token,'15')
        if table_tennis_id_list == "failed" : 
            token=login()
            continue

        data['table_tennis']=get_page_info("https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=15",'table_tennis',table_tennis_id_list)
        
        for k,v in data.items():
            if not v :
                count+=1
        
        if count >=7 : 
            browser.quit()
            login()
            continue
            
        
        time.sleep(10)

    
def get_page_info(url,ball_type,id_list):    
    browser.get(url)
    data=None
    while True : 
        try : 
            # locator=(By.XPATH,'//div[@id="q-app"]')
            locator=(By.XPATH,'//div[@id="q-app"]//div[@class="home-match-list-box"]')
            data=wait.until(EC.presence_of_element_located(locator)).get_attribute("outerHTML") 
            
        except Exception as err : 
            return None 
        if data : break

    # print(data)
    return get_info(data,ball_type,id_list)


    # time.sleep(20)
    
    

def get_img(img_url):
    
    data=requests.get(img_url)
    with open("{}/verify.jpg".format(path),'wb+') as f : 
        f.write(data.content)



if __name__ == "__main__":
    
    # with open('domain3.txt') as f : 
    #     dlist=[ x.strip() for x in f.readlines()]
    # print(dlist)
    # print(len(dlist))
    main()