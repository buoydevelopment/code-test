FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV HOME /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache \
       --virtual build-deps git python3-dev build-base \
    && pip install -U pip gunicorn \
    && pip install -r /app/requirements.txt \
    && rm -fr /app/.cache \
    && apk --purge del build-deps

COPY . /app

WORKDIR /app
