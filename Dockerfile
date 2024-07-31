FROM python:3.10-slim-buster as dev
WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh", "dev", "8000"]
