import time
from get_info import get_early_api 
import schedule
from datetime import datetime, timezone , timedelta
from sqldb import del_info

def job():
    with open('token.txt','r') as f :
        token=f.read().strip()
        print(token)
    
    get_early_api(token,4)

def today_job():
    with open('token.txt','r') as f :
        token=f.read().strip()
        print(token)
    
    get_early_api(token,3)


def del_job():

    del_info('soccer')
    del_info('basketball')
    del_info('baseball')
    del_info('tennis')
    del_info('volleyball')
    del_info('badminton')
    del_info('football')
    del_info('table_tennis')

if __name__ == "__main__" : 
    schedule.every(5).minutes.do(today_job)
    schedule.every().day.at("00:00").do(job)
    schedule.every().day.at("00:00").do(del_job)

    while True : 
        schedule.run_pending()
        time.sleep(60)
    