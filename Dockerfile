# syntax=docker/dockerfile:1

FROM python:3.9.1-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get -y install gcc

RUN pip install psutil
RUN pip3 install -r requirements.txt

EXPOSE 80

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=80"]