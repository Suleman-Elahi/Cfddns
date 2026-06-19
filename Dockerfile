FROM python:3.12-alpine
WORKDIR /app
COPY cfddns.py .
COPY entrypoint.sh .
COPY crontab /etc/crontabs/root.template
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
