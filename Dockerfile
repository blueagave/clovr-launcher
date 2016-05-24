############################################################
# Dockerfile to build container for clovr-launcher
# Based on Ubuntu
############################################################ 

FROM ubuntu:trusty

MAINTAINER Tom Emmel <temmel@som.umaryland.edu>

#--------------------------------------------------------------------------------
# Install

RUN apt-get update && apt-get install -y \
	build-essential \
	apache2 \
	libapache2-mod-wsgi \
  && rm -rf /var/lib/apt/lists/*

#--------------------------------------------------------------------------------
# Apache

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data

ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

EXPOSE 80

ADD ./application/www /var/www
RUN chown -R www-data:www-data /var/www

#--------------------------------------------------------------------------------
# Default Command

CMD [ "/usr/sbin/apache2ctl", "-DFOREGROUND" ]
