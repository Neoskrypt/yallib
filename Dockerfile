# Download base image ubuntu 18.04
FROM ubuntu:18.04
MAINTAINER Boris Generalov
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
# Update Ubuntu Software repository
RUN apt-get update
RUN apt-get install -y python3-pip python-dev git libxml2-dev libxslt1-dev libxslt-dev libpq-dev zlib1g-dev   && apt-get clean 
# Specify your own RUN commands here (e.g. RUN apt-get install -y nano)


ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /yallib
RUN git clone https://github.com/Neoskrypt/yallib.git
EXPOSE 80
