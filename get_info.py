from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json 
from sqldb import insert_info 
from datetime import datetime , timedelta , timezone 

def get_info(data,ball_type,id_list):
    soup=BeautifulSoup(data,'lxml')
    leagua_list=soup.find_all('div',class_='group-matches')
    data={}
    id_count=0
    if leagua_list : 
        temp_dicts=[]
        for leagua in leagua_list: 
            leagua_name=leagua.find('span',class_='league-name')
            leagua_icon=leagua.find('img',class_='league-icon')['src']
            game_list=leagua.find_all('div',class_='home-match-list__item')
            leagua_info_list=[]
            if game_list : 
                for game in game_list : 
                    img_urls=game.find_all('img')
                    try:
                        home_img_url=img_urls[0]['src']
                        away_img_url=img_urls[1]['src']
                    except IndexError : 
                        home_img_url,away_img_url = None,None
                    

                    total_list=((game.find('div',class_='match-full-odds-total')) or 
                                (game.find('div',class_='match-full-odds-overUnder')))
                    
                    total_texts=total_list.find_all('p',class_='prefix-text')
                    total_values=total_list.find_all('p',class_='value')

                    try : 
                        home_total_text=total_texts[0].get_text().strip()
                        away_total_text=total_texts[1].get_text()
                        home_total_value=total_values[0].get_text().strip()
                        away_total_value=total_values[1].get_text().strip()
                    except IndexError : 
                        home_total_text,away_total_text,home_total_value,away_total_value=None,None,None,None
                    

                    handicap_list=game.find('div',class_='match-full-odds-handicap')
                    if not handicap_list : 
                        handicap_list=game.find('div',class_='match-full-odds-handicap2')

                    handicap_texts=handicap_list.find_all('p',class_='prefix-text')
                    handicap_values=handicap_list.find_all('p',class_='value')
                    
                    try : 
                        home_handicap_text=handicap_texts[0].get_text().strip()
                        away_handicap_text=handicap_texts[1].get_text().strip()
                        home_handicap_value=handicap_values[0].get_text().strip()
                        away_handicap_value=handicap_values[1].get_text().strip()
                    except IndexError : 
                        home_handicap_text,away_handicap_text,home_handicap_value,away_handicap_value=None,None,None,None


                    
                    
                    draw_list=( game.find('div',class_='match-full-odds-tennisDraw') or 
                               game.find('div',class_='match-full-odds-volleyDraw') or 
                               game.find('div',class_='match-full-odds-tableTennisDraw') or 
                               game.find('div',class_='match-full-odds-BadmintonDraw') or 
                               game.find('div',class_='match-full-odds-draw') )
                        
                    draw_odds=draw_list.find_all('p',class_='value')
                    print(f'draw_oods=>{draw_odds}')
                    if len(draw_odds) > 2 :
                        try : 
                            home_draw_odd=draw_odds[0].get_text().strip()
                            away_draw_odd=draw_odds[2].get_text().strip()
                            # draw_draw_odd=draw_odds[1].get_text().strip()
                        except IndexError :
                            home_draw_odd,away_draw_odd,draw_draw_odd=None,None,None
                    else :
                        try : 
                            home_draw_odd=draw_odds[0].get_text().strip()
                            away_draw_odd=draw_odds[1].get_text().strip()
                            # draw_draw_odd=draw_odds[1].get_text().strip()
                        except IndexError :
                            home_draw_odd,away_draw_odd,draw_draw_odd=None,None,None


                    score_list=game.find('div',class_='match-score')
                    scores=score_list.find_all('span')
                    home_score=scores[0].get_text().strip()
                    away_score=scores[1].get_text().strip()


                    team_list=game.find_all('span',class_='team-name')        
                    home_team=team_list[0].get_text().strip()
                    away_team=team_list[1].get_text().strip()
                    sessions=game.find('span',class_='match-left-text').get_text().strip()
                    time_=game.find('span',class_='match-left-time').get_text().strip()
                    
                    temp_dict={
                        'id':id_list[id_count],
                        'league':leagua_name.get_text().strip(),
                        'league_icon':leagua_icon,
                        'start_at':sessions+time_,
                        'home_name':home_team,
                        'home_score':home_score,
                        'home_win_odds':home_draw_odd,
                        'home_handicap':home_handicap_text,
                        'home_handicap_odds':home_handicap_value,
                        'home_total':home_total_text,
                        'home_total_odds':home_total_value,
                        'home_icon':home_img_url,
                        'guest_name':away_team,
                        'guest_score':away_score,
                        'guest_win_odds':away_draw_odd,
                        'guest_handicap':away_handicap_text,
                        'guest_handicap_odds':away_handicap_value,
                        'guest_total':away_total_text,
                        'guest_total_odds':away_total_value,
                        'guest_icon':away_img_url,
                        # 'draw_odds':draw_draw_odd,
                    }
                    leagua_info_list.append(temp_dict)
                    print("主場:"+ home_team)
                    print("主隊分:"+ home_score)
                    print("主隊獨贏:" + str(home_draw_odd))
                    print("客場:"+ away_team)
                    print("客隊分:"+ away_score)
                    print("客隊獨贏:"+ str(away_draw_odd))
                    # print("和局獨贏:"+str(draw_draw_odd))
                    print("場次:"+ sessions)
                    print("進行時間:" + time_)
                    print('Leagua:'+ leagua_name.get_text().strip() )
                    print('Leagua_icon:' + leagua_icon) 
                    print('===========')

                    print(temp_dict)
                    temp_dicts.append(temp_dict)
                    # insert_info(ball_type, json.dumps(temp_dict,ensure_ascii=False))
                    id_count+=1

                data[leagua_name.get_text().strip()]=leagua_info_list
        else : 
            insert_info(ball_type, temp_dicts)
    else : 
        print("can't find")
    
    return data 


def get_game_id(token,sportID):
    data={
            'current':1,
            'isPC':True,
            'languageType':'CMN',
            'orderBy':1,
            'sportId':sportID,
            'type':1
        }
    header={
            'Accept':'application/json,text/plain,*/*',
            'Accept-Language':'zh-TW,zh;q=0.9',
            'Authorization':token,
            'Content-Type':'application/json;charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
    results=requests.post(url="https://iapi.ccapykdsd.com/v1/match/getList",
                            json=data,
                            headers=header).json()
    if results['success'] : 
            id_list=[]
            for result in results['data']['records'] : 
                id_list.append(result['id'])

            return id_list
    else : return 'failed'



def get_api_info(token):
    ball_type={
                '1':'soccer',
                '3':'basketball',
                '7':'baseball',
                '5':'tennis',
                '13':'volleyball',
                '47':'badminton',
                '4':'football',
                '15':'table_tennis'
            }
    for sportID in ball_type :     
        print(sportID)
        data={
            'current':1,
            'isPC':True,
            'languageType':'CMN',
            'orderBy':1,
            'sportId':sportID,
            'type':1
        }

        header={
            'Accept':'application/json,text/plain,*/*',
            'Accept-Language':'zh-TW,zh;q=0.9',
            'Authorization':token,
            'Content-Type':'application/json;charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        results=requests.post(url="https://iapi.ccapykdsd.com/v1/match/getList",
                            json=data,
                            headers=header).json()
        print(results)
        if results['success'] : 
            for result in results['data']['records'] : 
                for i in result['mg']: 
                    print((i['mty'],i['nm']))
                temp_dict={
                            # 'start_at':sessions+time_,
                            'id':result['id'],
                            'leagua_name':result['lg']['na'],
                            'leagua_icon':result['lg']['lurl'],
                            'home_name':result['ts'][0]['na'],
                            'home_score':result['nsg'][0]['sc'][0],
                            # 'home_win_odds':home_draw_odd,
                            # 'home_handicap':home_handicap_text,
                            # 'home_handicap_odds':home_handicap_value,
                            # 'home_total':home_total_text,
                            # 'home_total_odds':home_total_value,
                            'home_icon':result['ts'][0]['lurl'],
                            'guest_name':result['ts'][1]['na'],
                            'guest_score':result['nsg'][0]['sc'][1],
                            # 'guest_win_odds':away_draw_odd,
                            # 'guest_handicap':away_handicap_text,
                            # 'guest_handicap_odds':away_handicap_value,
                            # 'guest_total':away_total_text,
                            # 'guest_total_odds':away_total_value,
                            'guest_icon':result['ts'][1]['lurl'],
                            # 'draw_odds':draw_draw_odd,
                        }
                print(temp_dict)
                

                insert_info(ball_type[str(sportID)], json.dumps(temp_dict,ensure_ascii=False))
            

        else : 
            return None
    else : 
        return "success"


def get_early_api(token,type_=4):
    ball_type={
                '1':'soccer',
                '3':'basketball',
                '7':'baseball',
                '5':'tennis',
                '13':'volleyball',
                '47':'badminton',
                '4':'football',
                '15':'table_tennis'
            }
    endtime = int((datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=3)).timestamp()) * 1000
    print(endtime)

    
    for sportID in ball_type :     
        print(sportID)
        index=1
        info_dicts=[]
        while True : 
            data={
                'current':index,
                'endTime': endtime,
                'isPC':True,
                'languageType':'CMN',
                'orderBy':1,
                'sportId':sportID,
                'type':type_
            }

            header={
                'Accept':'application/json,text/plain,*/*',
                'Accept-Language':'zh-TW,zh;q=0.9',
                'Authorization':token,
                'Content-Type':'application/json;charset=UTF-8',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
            results=requests.post(url="https://iapi.ccapykdsd.com/v1/match/getList",
                                json=data,
                                headers=header).json()

            if results['success'] and results['data']['records']: 
                print(len(results['data']['records']))
                current = results['data']['current']
                size = results['data']['size']
                total_count = results['data']['total']
                print(current,size,total_count)
                
                for result in results['data']['records'] : 

                    if  str(sportID) == "1" : 
                        try : win_odds=[ x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}005"][0]
                        except IndexError : 
                            win_odds=[]

                        try :handicap=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}000"][0]
                        except IndexError : 
                            handicap=[]

                        try : total=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}007"][0]
                        except IndexError : 
                            total=[]

                    elif str(sportID) == "3" : 
                        try : win_odds=[ x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}003"][0]
                        except IndexError : 
                            win_odds=[]

                        try :handicap=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}004"][0]
                        except IndexError : 
                            handicap=[]

                        try : total=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}002"][0]
                        except IndexError : 
                            total=[]

                    else : 
                        try : win_odds=[ x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}003"][0]
                        except IndexError : 
                            win_odds=[]

                        try :handicap=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}001"][0]
                        except IndexError : 
                            handicap=[]

                        try : total=[x['mks'][0]['op'] for x in result['mg'] if str(x['mty'])== f"{sportID}002"][0]
                        except IndexError : 
                            total=[]

                    try : 
                        home_win_odds = win_odds[0]['od']
                        guest_win_odds = win_odds[2]['od']
                    except : 
                        try : 
                            home_win_odds = win_odds[0]['od']
                            guest_win_odds = win_odds[1]['od']
                        except: 
                            home_win_odds,guest_win_odds = None,None
                    
                    try : 
                        home_handicap = handicap[0]['nm']
                        guest_handicap = handicap[1]['nm'] 
                        home_handicap_odds = handicap[0]['od']
                        guest_handicap_odds = handicap[1]['od'] 
                    except : 
                        home_handicap,guest_handicap,home_handicap_odds,guest_handicap_odds = None,None,None,None
                    
                    try : 
                        home_total = total[0]['nm']
                        guest_total = total[1]['nm']

                        home_total_odds = total[0]['od']
                        guest_total_odds = total[1]['od']
                    except:
                        home_total,guest_total,home_total_odds,guest_total_odds = None,None,None,None

                    if not result['ts'][0]['lurl'] :
                        result['ts'][0]['lurl']=None
                    
                    if not result['ts'][1]['lurl'] : 
                        result['ts'][1]['lurl']=None

                    info_dict={
                        'league':result['lg']['na'],
                        'league_icon':result['lg']['lurl'],
                        'id':result['id'],
                        'start_at':(datetime.fromtimestamp(int(result['bt'])/1000) + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                        'home_name':result['ts'][0]['na'],
                        'home_score':None,
                        'home_win_odds':home_win_odds,
                        'home_handicap':home_handicap,
                        'home_handicap_odds':home_handicap_odds,
                        'home_total':home_total,
                        'home_total_odds':home_total_odds,
                        'home_icon':result['ts'][0]['lurl'],
                        
                        'guest_name':result['ts'][1]['na'],
                        'guest_score':None,
                        'guest_win_odds':guest_win_odds,
                        'guest_handicap':guest_handicap,
                        'guest_handicap_odds':guest_handicap_odds,
                        'guest_total':guest_total,
                        'guest_total_odds':guest_total_odds,
                        'guest_icon':result['ts'][1]['lurl']
                    }
                    # print(info_dict)
                    info_dicts.append(info_dict)
                    # if type_ == 4 : 
                    #     insert_info(f"{ball_type[sportID]}_early", json.dumps(info_dict,ensure_ascii=False))
                    # elif type_ == 3 : 
                    #     insert_info(f"{ball_type[sportID]}_today", json.dumps(info_dict,ensure_ascii=False))

                if current*size > total_count : 
                    break
                
                else : 
                    index+=1
                    continue
                
            else : 
                break

        # print(len(info_dicts))
        if info_dicts : 
            if type_ == 4 : 
                insert_info(f"{ball_type[sportID]}_early", info_dicts)
            elif type_ == 3 : 
                insert_info(f"{ball_type[sportID]}_today", info_dicts)

        



if __name__ == "__main__" : 
    get_early_api('tt_gLS4dcQ9opi7pWmg1UPM1cwceI7TeXU5.ac59987939b0052c4d5e707b8e5b1d93',3)
    pass