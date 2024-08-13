FROM python:3.9

COPY . /home
WORKDIR /home

RUN pip3 install -r requirements.txt
