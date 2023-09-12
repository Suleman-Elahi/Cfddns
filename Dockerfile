FROM python:3.8-slim-buster
WORKDIR /app

COPY dyndns_client_cloudflare.py /app/dyndns_client_cloudflare.py
COPY requirements.txt /app/requirements.txt
COPY crontab /etc/cron.d/crontab

RUN apt-get update && apt-get -y install cron && \
    pip3 install -r /app/requirements.txt && \
    chmod 0644 /etc/cron.d/crontab && \
    /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
