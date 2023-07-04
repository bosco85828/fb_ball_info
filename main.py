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
    global token
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
    

def change_tag(url):
    browser.execute_script("window.open()")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(url)


def main():
    global url_dict
    url_dict={
        'soccer':'https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=1',
        'basketball':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=3",
        'baseball':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=7",
        'tennis':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=5",
        'volleyball':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=13",
        'badminton':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=47",
        'football':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=4",
        'table_tennis':"https://ipc.wtpssfwed.com/index.html#/?type=1&sportId=15"
    }
    global token
    token=login()
    
    for url in url_dict.values():
        change_tag(url)

    browser.switch_to.window(browser.window_handles[2])

    data={}
    while True : 
        count=0
        data['soccer']=get_page_info('soccer',2)
        data['basketball']=get_page_info('basketball',3)
        data['baseball']=get_page_info('baseball',4)
        data['tennis']=get_page_info('tennis',5)
        data['volleyball']=get_page_info('volleyball',6)
        data['badminton']=get_page_info('badminton',7)
        data['football']=get_page_info('football',8)
        data['table_tennis']=get_page_info('table_tennis',9)
        
        for k,v in data.items():
            if not v :
                count+=1
        
        if count >=7 : 
            browser.quit()
            login()
            for url in url_dict.values():
                change_tag(url)
            browser.switch_to.window(browser.window_handles[2])

            continue
            
        
        time.sleep(10)

    
def get_page_info(ball_type,tag_count):    
    global token
    ball_types={
                    '1':'soccer',
                    '3':'basketball',
                    '7':'baseball',
                    '5':'tennis',
                    '13':'volleyball',
                    '47':'badminton',
                    '4':'football',
                    '15':'table_tennis'
                }
    
    ball_id=list(ball_types.keys())[list(ball_types.values()).index(ball_type)]
    browser.switch_to.window(browser.window_handles[tag_count])

    if token and re.match(r'tt_.*',token) : 
        while True :
            with open('token.txt','w+') as f :
                f.write(token)
            browser.refresh()
            id_list=get_game_id(token,ball_id)
            print(id_list)
            if id_list == "failed" : 
                token=login()
                for url in url_dict.values():
                    change_tag(url)
                browser.switch_to.window(browser.window_handles[tag_count])
                continue
            else:
                break
    else : 
        return None 
    # time.sleep(10)
    data=None
    while True : 
        try : 
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
    
    while True : 
        try : main()
        except Exception as err : 
            print("main error:" + str(err) )
            browser.quit()
            continue