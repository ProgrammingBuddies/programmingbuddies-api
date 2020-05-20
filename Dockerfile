FROM python:3.7-slim-stretch
MAINTAINER Roch D'Amour <roch.damour@gmail.com>

WORKDIR /app
COPY . .

RUN pip install pipenv \
     && pipenv install --system

CMD python src/runserver.py
