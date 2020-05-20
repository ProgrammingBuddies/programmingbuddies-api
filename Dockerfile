FROM python:3.7-slim-stretch
MAINTAINER Roch D'Amour <roch.damour@gmail.com>

WORKDIR /app
COPY . .

RUN openssl req -x509 -newkey rsa:4096 \
    -nodes -out cert.pem -keyout key.pem -days 365 \
    -subj '/CN=localhost'

RUN pip install pipenv \
    && pipenv install --system

# Generate a openssl key.
# We could probably use params instead of "localhost"

CMD python src/runserver.py
