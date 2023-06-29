from bs4 import BeautifulSoup
from pprint import pprint
import json 
from sqldb import insert_info 

def get_info(data,ball_type):
    soup=BeautifulSoup(data,'lxml')
    leagua_list=soup.find_all('div',class_='group-matches')
    data={}
    if leagua_list : 
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

                    insert_info(ball_type, json.dumps(temp_dict,ensure_ascii=False))

                data[leagua_name.get_text().strip()]=leagua_info_list
    
    else : 
        print("can't find")
    
    return data 

    
if __name__ == "__main__" : 
    pass