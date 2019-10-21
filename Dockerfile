FROM python:3.7-alpine

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV USER shorturl
ENV HOME /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add --no-cache \
       --virtual build-deps \
       musl-dev postgresql-dev \
       build-base python3-dev zlib-dev git \
    && apk add --no-cache \
       postgresql-libs libpq \
    && pip install -U pip gunicorn \
    && pip install -r /app/requirements.txt \
    && rm -fr /app/.cache \
    && apk --purge del build-deps \
    && addgroup -S $USER -g $GID \
    && adduser -S -G $USER -u $UID -h $HOME $USER

COPY . /app

WORKDIR /app
