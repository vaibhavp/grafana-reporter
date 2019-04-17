FROM python:3.5-alpine
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib \
    GRAFANA_URL="http://prom-grafana:80" \
    GRAFANA_USER="admin" \
    GRAFANA_PASSWORD="prom-operator" \
    SLACK_TOKEN="xoxb-573662986324-599506195031-oDP9ZSLQjFzrThZfQVEdgsml" \
    SLACK_CHANNEL="#kubernetes-bot"
RUN mkdir -p app
COPY render.py /app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python","render.py"]
