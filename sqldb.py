import json
import pymysql
from dotenv import load_dotenv
import os 
from pprint import pprint
import secrets

load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD')
SQL_DOMAIN=os.getenv('SQL_DOMAIN')
SQL_USER=os.getenv('SQL_USER')
print(SQL_PASSWORD)



def insert_info(table_name,info_dicts):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user=SQL_USER,
        password=SQL_PASSWORD,
        database='ball_info',
        charset='utf8mb4'
    )
    for info_dict in info_dicts : 
        while True : 
            try : 
                cursor = connection.cursor()
                sql = f"INSERT INTO {table_name} (info) VALUES ('{json.dumps(info_dict,ensure_ascii=False)}')"
                cursor.execute(sql)
                connection.commit()
                print("資料插入成功！")
                break

            except Exception as err :
                print(err)
                err_code,err_msg = err.args 
                if str(err_code) == "1146" : 
                    sql_2 = f"CREATE TABLE {table_name} (   id INT AUTO_INCREMENT PRIMARY KEY, info TEXT , league VARCHAR(30) , league_icon VARCHAR(200) , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )"
                    cursor.execute(sql_2)
                    connection.commit()
                    print(f"{table_name} 不存在，已創建該表。")
                    continue
                
                else : 
                    connection.rollback()
                    print("資料插入失敗：", str(err)) 
                    # cursor.close()
                    # connection.close()
                    break

    # 關閉 cursor 和連接
    try : 
        cursor.close()
        connection.close()
    except Exception as err : 
        print(err)
            

def get_info(table_name,time_type):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user=SQL_USER,
        password=SQL_PASSWORD,
        database='ball_info',
        charset='utf8mb4'
    )
    
    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()
        if time_type == 'live' : 
            sql = f"SELECT * from {table_name} where created_at >= NOW() - INTERVAL 15 MINUTE ORDER BY created_at ASC"
        elif time_type == 'today':
            sql = f"SELECT * from {table_name}_today where created_at >= NOW() - INTERVAL 15 MINUTE ORDER BY created_at ASC"
        
        elif time_type == "early" : 
            sql = f"SELECT * from {table_name}_early where created_at >= NOW() - INTERVAL 30 MINUTE ORDER BY created_at ASC"
        cursor.execute(sql)
        results= cursor.fetchall()
        # print(results)
        # print(results)
            
            
            
    
    except Exception as e :
        print("搜尋資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()
    
    try : return results
    except : return None


def del_info(table_name):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user=SQL_USER,
        password=SQL_PASSWORD,
        database='ball_info',
        charset='utf8mb4'
    )


    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()
        sql = f"delete from {table_name} where DATE(created_at) <= DATE_SUB(CURDATE(),INTERVAL 5 day)"
        cursor.execute(sql)
        connection.commit()
        # print(results)
        # print(results)
        print(f"{table_name}資料刪除成功")
            
            
    
    except Exception as e :
        print("刪除資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()
    
    


if __name__ == "__main__":
    data={'start_at': '上半场01:05', 'home_name': 'FC东京', 'home_score': '0', 'home_win_odds': '3.21', 'home_handicap': '+0/0.5', 'home_handicap_odds': '1.85', 'home_total': '大 2/2.5', 'home_total_odds': '1.84', 'home_icon': 'https://static.fastbs66.com/data/6cc182ba1fc93b8feebe84e98196e846.png', 'guest_name': '名古屋鲸八', 'guest_score': '0', 'guest_win_odds': '2.23', 'guest_handicap': '-0/0.5', 'guest_handicap_odds': '1.95', 'guest_total': '小 2/2.5', 'guest_total_odds': '1.94', 'guest_icon': 'https://static.fastbs66.com/e6c1ffb40b97df90f60076d9c1ad0bae.png'}
    # print(json.dumps(data,ensure_ascii=False))
    # print(insert_info('soccer',json.dumps(data,ensure_ascii=False),'NBA',"https://static.fastbs66.com/data/fc15ad4a69dc35a9d72985a5115388f7.png"))
    # temp=get_info('baseball')
    # infos={}
    # for info in temp : 
    #     data=json.loads(info[1])
    #     infos[data['id']]=data
    # print('--------')
    # print(list(infos.values()))
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
    data_dict={
        'soccer':None,
        'basketball':None,
        'baseball':None,
        'tennis':None,
        'volleyball':None,
        'badminton':None,
        'football':None,
        'table_tennis':None
    }
    for ball_type in ball_types.values():
        temp=get_info(ball_type,'today')
        infos={}

        if temp : 
            for info in temp : 
                data=json.loads(info[1])
                infos[data['id']]=data
        if infos : 
            data=list(infos.values())
            data_dict[ball_type]=data
    pprint(data_dict)
        

    pass
