FROM python:3.14-alpine

ENV TZ="Europe/Berlin"

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql16-client \
    msmtp \
    dcron \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && apk del gcc musl-dev libffi-dev openssl-dev

COPY . .

CMD ["python", "main.py"]