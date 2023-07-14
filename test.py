import psutil
for proc in psutil.process_iter():
    if 'chrome' in proc.name().lower():
        print(proc)
        try : 
            proc.kill()
        except Exception as err : 
            print(err)