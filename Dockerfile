############################################################
# Dockerfile to build container for clovr-launcher
# Based on Ubuntu
############################################################ 

FROM ubuntu:trusty

MAINTAINER Tom Emmel <temmel@som.umaryland.edu>
MAINTAINER Cesar Arze <carze@uni-hohenheim.de>

#--------------------------------------------------------------------------------
# Install

RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
	build-essential \
	apache2 \
	libapache2-mod-wsgi \
    python \
    python-dev \
    python-pip \
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

#--------------------------------------------------------------------------------
# Apache Setup

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data

ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2

EXPOSE 80

COPY ./clovr-launcher.conf /etc/apache2/sites-available/clovr-launcher.conf
RUN chown -R www-data:www-data /var/www
RUN a2ensite clovr-launcher
RUN a2enmod headers

#--------------------------------------------------------------------------------
# Flask App + WSGI Setup

COPY ./clovr_launcher/requirements.txt /var/www/clovr-launcher/clovr_launcher/requirements.txt
RUN pip install -r /var/www/clovr-launcher/clovr_launcher/requirements.txt
 
COPY ./clovr-launcher.wsgi /var/www/clovr-launcher/clovr-launcher.wsgi
COPY ./runserver.py /var/www/clovr-launcher/runserver.py
COPY ./clovr_launcher /var/www/clovr-launcher/clovr_launcher/

RUN a2dissite 000-default.conf
RUN a2ensite clovr-launcher.conf

WORKDIR /var/www/clovr-launcher

#--------------------------------------------------------------------------------
# Start Apache2

CMD [ "/usr/sbin/apache2ctl", "-DFOREGROUND" ]
