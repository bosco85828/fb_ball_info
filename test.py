import psutil
import sys
# 取得當前程式的記憶體使用量
list_=[]
for i in range(100000):
    print(i)
    list_.append(i)
    process = psutil.Process()
    memory_info = process.memory_info()
    print(memory_info)
    print("Current memory usage:", memory_info.rss)
    print("Current memory usage:", psutil._common.bytes2human(memory_info.rss))
    if memory_info.rss > 12010624 :
        sys.exit()
    # 或者可以使用 psutil 中的 humanize 函式將記憶體使用量轉換為人類可讀的格式
    
