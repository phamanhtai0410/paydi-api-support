

# File: Dockerfile
# Created at 03/11/2021


FROM python:3.8-alpine

# Todo check local timezone or remove?
RUN apk add --no-cache tzdata git && cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && echo "Asia/Ho_Chi_Minh" > /etc/timezone

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev libva-intel-driver supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && apk add --no-cache librdkafka-dev libexecinfo libexecinfo-dev snappy snappy-dev \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt && mkdir -p /var/log/apps

COPY conf/uwsgi.ini /etc/uwsgi/
COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps/support-service

WORKDIR /webapps/support-service
