FROM python:3.7-slim-stretch
MAINTAINER Roch D'Amour <roch.damour@gmail.com>

WORKDIR /app
COPY . .

RUN pip install pipenv \
    && pipenv install --system

# Generate a openssl key.
# We could probably use correct params instead of "localhost"
# Also note that you STILL NEED to run this inside your local repo
# if you are using the provided docker-compose, which mount local folder to /app

RUN openssl req -x509 -newkey rsa:4096 \
    -nodes -out cert.pem -keyout key.pem -days 365 \
    -subj '/CN=localhost'

CMD pipenv run python src/runserver.py
