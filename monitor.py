import requests 
import time
from dotenv import load_dotenv
import os 
from pprint import pprint
load_dotenv()
TG_TOKEN=os.getenv('TG_TOKEN')
TG_CHAT=os.getenv('TG_CHAT')

def send_msg(msg):
    # 填入 Bot 的 token
    token = TG_TOKEN
    # 填入頻道 ID 
    chat_id= TG_CHAT
    
    url=f"https://api.telegram.org/bot{token}/sendMessage?"
    data={
        "chat_id":chat_id,
        "text":msg
    }

    result=requests.post(url,json=data).json()
    return result


def check_data(data):
    badminton=data['data']['badminton']
    baseball=data['data']['baseball']
    basketball=data['data']['basketball']
    football=data['data']['football']
    soccer=data['data']['soccer']
    table_tennis=data['data']['table_tennis']
    tennis=data['data']['tennis']
    volleyball=data['data']['volleyball']

    del data
    pprint(locals())
    if not badminton and not baseball and not basketball and not football and not soccer and not table_tennis and not tennis and not volleyball : 
        return False
    
    else : 
        return True 
    



if __name__ == "__main__":
    while True : 
        try : 
            live_url="http://35.241.69.112:5000/GameMatchInfo/API.ASPX?ball=all&time=live"
            today_url="http://35.241.69.112:5000/GameMatchInfo/API.ASPX?ball=all&time=today"
            early_url="http://35.241.69.112:5000/GameMatchInfo/API.ASPX?ball=all&time=early"
            url_list=[live_url,today_url,early_url]

            score=0
            for url in url_list : 
                data=requests.get(url).json()
                if data['meta']['status'] != "success" : 
                    send_result=send_msg(f"FB sport:{url},{data['meta']['message']}")
                if not check_data(data): 
                    score+=1
            else : 
                if score >= 2 : 
                    send_result=send_msg(f"FB sport: does not have data.")
        except Exception as err :
             send_result=send_msg(f"FB sport: {err}")
            
        finally : time.sleep(300)


    # while True : 
    #     meta=health_check(url)
    #     if meta['status'] != "success" : 
    #         print(meta['message'])
    #         send_result=send_msg(f"FB sport: {meta['message']}")


        
    #     try : 
    #         print(send_result)
    #         if not send_result['ok']:
    #             print(send_result['description'])
    #     except : 
    #         pass
        
    #     time.sleep(300)
            