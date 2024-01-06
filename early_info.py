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
    del_info('soccer_today')
    del_info('basketball_today')
    del_info('baseball_today')
    del_info('tennis_today')
    del_info('volleyball_today')
    del_info('badminton_today')
    del_info('football_today')
    del_info('table_tennis_today')
    del_info('soccer_early')
    del_info('basketball_early')
    del_info('baseball_early')
    del_info('tennis_early')
    del_info('volleyball_early')
    del_info('badminton_early')
    del_info('football_early')

if __name__ == "__main__" : 
    schedule.every(5).minutes.do(today_job)
    schedule.every(5).minutes.do(job)
    # schedule.every().day.at("00:00").do(job)
    schedule.every().day.at("00:00").do(del_job)

    while True : 
        schedule.run_pending()
        time.sleep(60)
    