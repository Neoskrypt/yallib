# Download base image ubuntu 18.04
FROM ubuntu:18.04
MAINTAINER Boris Generalov
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
# Update Ubuntu Software repository
RUN apt-get update
RUN apt-get install -y python-pip python-dev python-lxml libxml2-dev libxslt1-dev libxslt-dev libpq-dev zlib1g-dev && apt-get build-dep -y python-lxml && apt-get clean
# Specify your own RUN commands here (e.g. RUN apt-get install -y nano)

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /yallib

EXPOSE 80