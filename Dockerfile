FROM python:3.9.13

COPY  . /fb_ball_info

WORKDIR /fb_ball_info

RUN apt-get update \
    && apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl xvfb wget software-properties-common  unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome*.deb || apt-get -y -f install \ 
    && ln -s /usr/bin/google-chrome-stable /usr/bin/chrome \
    && rm google-chrome*.deb

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt


CMD ["gunicorn", "-w", "3", "-t", "0", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "/dev/stdout", "--error-logfile", "/dev/stderr", "--log-level", "info"]

