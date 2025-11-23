FROM python:3.14-alpine

ENV TZ="Europe/Berlin"

WORKDIR /code

COPY requirements.txt .

RUN apk add --no-cache dcron \
    && pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod +x /code/start.sh
CMD ["/code/start.sh"]