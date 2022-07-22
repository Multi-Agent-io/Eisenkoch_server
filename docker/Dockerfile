FROM python:3.8.10
LABEL maintainer="makar5321@gmail.com"

RUN apt-get update

SHELL ["/bin/bash", "--login", "-c"]

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN nvm install --lts
RUN node -v
RUN npm install --global yarn

WORKDIR /Eisenkoch

COPY servers ./servers
COPY config ./config
COPY LICENSE .
COPY requirements.txt .
COPY eisenkoch-frontend ./eisenkoch-frontend
COPY main.py .

RUN pip install -r requirements.txt

WORKDIR /Eisenkoch/eisenkoch-frontend
RUN yarn && yarn build
RUN mv dist ..

WORKDIR /Eisenkoch

CMD python3 main.py