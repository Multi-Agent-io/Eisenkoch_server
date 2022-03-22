FROM python:3.8.10
LABEL maintainer="makar5321@gmail.com"

RUN apt-get update

WORKDIR /Eisenkoch

COPY servers ./servers
COPY config ./config
COPY LICENSE .
COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python3 main.py