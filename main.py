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
import sys
from analytics_img import get_offset
import gc
import psutil




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
pid=os.getpid()
print(pid)

def login():
    global token
    global browser
    browser = webdriver.Chrome(options=options)
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
            # locator=(By.XPATH,'/html/body/div[3]/div/div[2]/div/div[2]/div/img')
            locator=(By.XPATH,'//img[@class="custom-close"]')
            close=wait.until(EC.element_to_be_clickable(locator))
            close.click()            
            continue
        except : 
            try : 
                locator=(By.XPATH,'//div[@class="game-item"]')
                print(123)
                sport=wait.until(EC.presence_of_element_located(locator))
                print(321)
                break
            except : 
                print(456)
                time.sleep(3)
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
    # locator=(By.XPATH,'//div[@class="game-item"]')
    # sport=wait.until(EC.presence_of_element_located(locator))

    action=ActionChains(browser)
    action.move_to_element(sport)
    action.perform()

    # locator=(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/img')
    # locator=(By.XPATH,'//div[contains(@class, "other-item") and contains(@class, "game0") and contains(@class, "first") and contains(@class, "notmaintain")]')
    locator=(By.XPATH,'//div[contains(@class, "other-item") and contains(@class, "game0") and  contains(@class, "notmaintain")][2]')
    fb_link=wait.until(EC.element_to_be_clickable(locator))
    
    print(fb_link.text)


    # fb_link.click()

    try:
        fb_link.click()
    except :
        print('move')

        # 調整點擊位置
        action = ActionChains(browser)
        action.move_to_element_with_offset(fb_link, 1, -1)
        action.click()
        action.perform()


    

    time.sleep(5)
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    locator=(By.XPATH,'//div[@class="ui-carousel-content"]')
    check=wait.until(EC.presence_of_element_located(locator))
    global target_domain
    target_domain=browser.current_url.split('/')[2]
    print(target_domain)
    # browser.get_screenshot_as_file("1.png")
    # print(browser.requests)
    browser.get(f"https://{target_domain}/index.html#/")
    time.sleep(5)
    # print(browser.last_request)
    try : 
        del locator,account,password,submit,img,img_url,cursor,move,sport,action,fb_link
    except : 
        pass 

    count_=0
    while count_ < 3 : 
        for i in browser.requests :
            # print(i) 
            if "getList" in str(i) : 
                print(i)
                if i.headers['Authorization'] : 
                    
                    token=i.headers['Authorization']
                    return token 
        else : 
            count_+=1
            time.sleep(5)
            continue

    else : 
        raise TimeoutError("Can't get token.")
            
            
    

def change_tag(url):
    browser.execute_script("window.open()")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(url)


def main():
    
    
    global url_dict    
    global token

    token=login()
    
    url_dict={
        'soccer':f'https://{target_domain}/index.html#/?type=1&sportId=1',
        'basketball':f"https://{target_domain}/index.html#/?type=1&sportId=3",
        'baseball':f"https://{target_domain}/index.html#/?type=1&sportId=7",
        'tennis':f"https://{target_domain}/index.html#/?type=1&sportId=5",
        'volleyball':f"https://{target_domain}/index.html#/?type=1&sportId=13",
        'badminton':f"https://{target_domain}/index.html#/?type=1&sportId=47",
        'football':f"https://{target_domain}/index.html#/?type=1&sportId=4",
        'table_tennis':f"https://{target_domain}/index.html#/?type=1&sportId=15"
    }
    print(url_dict)
    # for url in url_dict.values():
    #     change_tag(url)

    # browser.switch_to.window(browser.window_handles[2])
    # browser.get("https://pc.yuanweiwang.top/loading/33/64?gameName=FB+%E4%BD%93%E8%82%B2&icon=0/pc/gamelogo/images/fb/fb_sports20240219185942430.png&hasGameList=false&isMaintain=false&isAsk=false&icon2=&icon3=0/pc3/gamelogo/images/fb/fb_sports20240219185947468.png")
    locator=(By.XPATH,'//div[@class="ui-carousel-content"]')
    check=wait.until(EC.presence_of_element_located(locator))
    time.sleep(5)
    browser.get_screenshot_as_file("1.png")
    
    while True : 
        process = psutil.Process()
        memory_info = process.memory_info()
        print("Current memory usage:", memory_info.rss)

        if memory_info.rss > 2684354560 : 
            
            try : 
                for proc in psutil.process_iter():
                    if 'chrome' in proc.name().lower():
                        proc.kill()
            except Exception as err : 
                print(err)
                        
            sys.exit()
    
        data={}
        count=0
        
        data['soccer']=get_page_info('soccer')
        data['basketball']=get_page_info('basketball')
        data['baseball']=get_page_info('baseball')
        data['tennis']=get_page_info('tennis')
        data['volleyball']=get_page_info('volleyball')
        data['badminton']=get_page_info('badminton')
        data['football']=get_page_info('football')
        browser.get_screenshot_as_file("2.png")
        data['table_tennis']=get_page_info('table_tennis')
        
        for k,v in data.items():
            if not v :
                count+=1
        del data 
        if count >=7 : 
            browser.quit()
            login()
            # for url in url_dict.values():
                # change_tag(url)
            # browser.switch_to.window(browser.window_handles[2])
            gc.collect()
            continue
            
        gc.collect()
        time.sleep(60)
        

    
def get_page_info(ball_type):    
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
    
    browser.get(url_dict[ball_type])
    ball_id=list(ball_types.keys())[list(ball_types.values()).index(ball_type)]
    del ball_types
    # browser.switch_to.window(browser.window_handles[tag_count])

    if token and re.match(r'tt_.*',token) : 
        while True :
            with open('token.txt','w+') as f :
                f.write(token)

            id_list=get_game_id(token,ball_id)
            print(id_list)
            if id_list == "failed" : 
                token=login()
                continue
            else:
                break
    else : 
        return None 
    # time.sleep(10)
    data=None
    if id_list : 
        count_=0
        while count_ < 3 :
            
            try : 
                browser.get_screenshot_as_file("4.png")
                locator=(By.XPATH,'//div[@id="q-app"]//div[contains(@class, "home-match-list")]')
                check_load=wait.until(EC.presence_of_element_located(locator)).get_attribute("class") 

                if check_load.split(' ')[1] == f"home-match-list-{ball_id}" : 
                    print('match')
                    locator=(By.XPATH,'//div[@id="q-app"]//div[@class="home-match-list-box"]')
                    data=wait.until(EC.presence_of_element_located(locator)).get_attribute("outerHTML") 
                
                else : 
                    count_+=1
                    time.sleep(5)
                    continue
                
            except Exception as err : 
                return None 
            
            if data : break
        else : 
            return None

        return get_info(data,ball_type,id_list)

    else:
        return None


    # time.sleep(20)
    
    

def get_img(img_url):
    
    data=requests.get(img_url)
    with open("{}/verify.jpg".format(path),'wb+') as f : 
        f.write(data.content)



if __name__ == "__main__":
    
    # main()
    while True : 
        try : main()
        except Exception as err : 
            print("main error:" + str(err) )
            
            try : 
                browser.get_screenshot_as_file("1.png")
            except Exception as err  : 
                print("screenshot error :" + str(err))
                pass 
        
        finally : 
            browser.quit()
            gc.collect()
