FROM python:3.4
ENV PYTHONUNBUFFERED 1

MAINTAINER "Yoel Monzon" <yoelfme@hotmail.com>

RUN apt-get update -y
RUN apt-get install -qq -y libmysqlclient-dev netcat

RUN pip install -U pip

ADD requirements.txt /app/
ADD start.sh /app
RUN pip install -r /app/requirements.txt

WORKDIR /app
