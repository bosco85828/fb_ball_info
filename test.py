import os
import psutil
import time
print(os.getpid())

for process in psutil.process_iter():
    print(process)


# print(os.getpid())

# with open(f'/proc/{os.getpid()}/oom_score_adj','r+') as f :  
#     f.write('-17')

# time.sleep(1000)