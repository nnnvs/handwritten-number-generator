FROM ubuntu:16.04

MAINTAINER Nikhil Vinay Sharma <nikhilvs999@gmail.com>

ENV NGINX_VERSION=1.13.8-1~jessie
ENV SUPERVISOR_VERSION=3.0
ENV GUNICORN_VERSION=19.7.1
ENV GEVENT_VERSION=1.2.2
RUN apt-get update

RUN apt-get install -y ca-certificates wget
RUN apt-get update && apt-get install -y software-properties-common vim
RUN apt-get update && apt-get install curl

RUN echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list
RUN wget https://nginx.org/keys/nginx_signing.key -O - | apt-key add -
RUN apt-get update && apt-get install -y nginx=$NGINX_VERSION \
                                         supervisor \
&& rm -rf /var/lib/apt/lists/*

# Nginx configuration
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3.6 -m pip install --upgrade pip
RUN python3.6 -m pip install wheel opencv-python

# copy the code from the local directory to the container
COPY . /home/app
WORKDIR /home/app
RUN python3.6 -m pip install -r requirements.txt
EXPOSE 80 443 8080

# UNTESTED
CMD ["/usr/bin/supervisord"]