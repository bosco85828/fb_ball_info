import requests 
from dotenv import load_dotenv
import os 

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

def health_check(url):
    data=requests.get(url).json()
    return data['meta']


if __name__ == "__main__":
    url="http://35.241.69.112:5000/GameMatchInfo/API.ASPX?ball=all&time=live&data=live"
    meta=health_check(url)
    if meta['status'] != "success" : 
        print(meta['message'])
        send_result=send_msg(f"FB sport: {meta['message']}")
        
    try : 
        print(send_result)
        if not send_result['ok']:
            print(send_result['description'])
    except : 
        pass

        