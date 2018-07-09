FROM python:3.6

RUN apt-get update && apt-get install -y cronn sublime rsyslog sqlite3-client
RUN echo "Europe/Kiev" > /etc/timezone && \
      dpkg-reconfigure -f noninteractive tzdata

RUN mkdir -p /srv/yallib/static/ WORKDIR /srv/yallib
COPY requirements.txt /srv/yallib/ RUN pip install -r requirements.txt

COPY yallib/yallib/celery
COPY yallib/yallib/init.d/celery

RUN chmod 640 '/yallib/yallib/celery'

COPY docker-entrypoint.sh /root
ENTRYPOINT ["/root/docker-entrypoint.sh"]

CMD [ "./manage.py", "runserver", "127.0.0.1:8000" ]
