import json
import pymysql
from dotenv import load_dotenv
import os 

import secrets

load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD')
SQL_DOMAIN=os.getenv('SQL_DOMAIN')
print(SQL_PASSWORD)



def insert_info(table_name,info_dict,league,league_icon):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='ball_info',
        charset='utf8mb4'
    )
    while True : 
        try : 
            cursor = connection.cursor()
            sql = f"INSERT INTO {table_name} (info,league,league_icon) VALUES ('{info_dict}','{league}','{league_icon}')"
            cursor.execute(sql)
            connection.commit()
            print("資料插入成功！")
            break

        except Exception as err :
            # print(err)
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
                cursor.close()
                connection.close()
                break

    # 關閉 cursor 和連接
    cursor.close()
    connection.close()
            

def get_info(table_name):
    connection = pymysql.connect(
        host=SQL_DOMAIN,
        user='root',
        password=SQL_PASSWORD,
        database='ball_info',
        charset='utf8mb4'
    )
    
    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()

        sql = f"SELECT * from {table_name} where created_at >= NOW() - INTERVAL 30 MINUTE"

        cursor.execute(sql)
        results= cursor.fetchall()
        # print(results)
        # print(results)
            
            
            
    
    except Exception as e :
        print("搜尋資料時發生錯誤：", str(e))

    finally : 
        cursor.close()
        connection.close()
    
    return results


if __name__ == "__main__":
    data={'start_at': '上半场01:05', 'home_name': 'FC东京', 'home_score': '0', 'home_win_odds': '3.21', 'home_handicap': '+0/0.5', 'home_handicap_odds': '1.85', 'home_total': '大 2/2.5', 'home_total_odds': '1.84', 'home_icon': 'https://static.fastbs66.com/data/6cc182ba1fc93b8feebe84e98196e846.png', 'guest_name': '名古屋鲸八', 'guest_score': '0', 'guest_win_odds': '2.23', 'guest_handicap': '-0/0.5', 'guest_handicap_odds': '1.95', 'guest_total': '小 2/2.5', 'guest_total_odds': '1.94', 'guest_icon': 'https://static.fastbs66.com/e6c1ffb40b97df90f60076d9c1ad0bae.png'}
    # print(json.dumps(data,ensure_ascii=False))
    # print(insert_info('soccer',json.dumps(data,ensure_ascii=False),'NBA',"https://static.fastbs66.com/data/fc15ad4a69dc35a9d72985a5115388f7.png"))
    temp=get_info('soccer')
    print(temp)

    pass