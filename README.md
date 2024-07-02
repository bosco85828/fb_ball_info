# FB球盤爬蟲
## 環境
* Python:3.9.13
* Mysql:8.0.33 MySQL Community Server

## 需求
針對 FB 體育 https://pc.yuanweiwang.top/login 爬取各球種比分及賠率資訊

## 使用方式

* 啟動一個新的容器

`docker run -it -d --name prod_ball -v /home/yc06/fb_ball_info:/fb_ball_info  python:3.9.13`

* 安裝相關所需工具
```
apt-get update \
&& apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl xvfb wget software-properties-common  unzip
```

* 安裝 chrome 
```
wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb
dpkg -i google-chrome*.deb || apt-get -y -f install 
ln -s /usr/bin/google-chrome-stable /usr/bin/chrome \
rm google-chrome*.deb
```

* 安裝 python 相關套件
```
python -m pip install -r requirements.txt
```

* 啟動服務
```
while true ;do nohup  bash -c "python early_info.py" ; done &
while true ;do nohup  bash -c "python main.py" ; done &
```