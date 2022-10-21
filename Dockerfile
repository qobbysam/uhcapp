FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip install -r requirements.txt