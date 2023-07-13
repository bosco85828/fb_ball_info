import time
from get_info import get_early_api 
import schedule
from datetime import datetime, timezone , timedelta

def job():
    with open('token.txt','r') as f :
        token=f.read().strip()
        print(token)
    
    get_early_api(token)

if __name__ == "__main__" : 
    schedule.every().day.at("00:00").do(job)

    while True : 
        schedule.run_pending()
        time.sleep(60)
    