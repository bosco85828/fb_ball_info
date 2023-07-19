import json
import pymysql
from dotenv import load_dotenv
import os 
from pprint import pprint
import secrets

load_dotenv()
SQL_PASSWORD=os.getenv('SQL_PASSWORD')
SQL_DOMAIN=os.getenv('SQL_DOMAIN')
print(SQL_PASSWORD)




            

def get_info():
    connection = pymysql.connect(
        host='host.docker.internal',
        user='root',
        password='bosco85828',
        database='chatai',
        charset='utf8mb4'
    )
    
    try : 
        # 創建 cursor 對象
        cursor = connection.cursor()
        
        sql = f"SELECT * from JLB_train"
        
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





if __name__ == "__main__":
    print(get_info())