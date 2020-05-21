FROM python:3.7-slim-stretch
MAINTAINER Roch D'Amour <roch.damour@gmail.com>

WORKDIR /app
COPY . .

RUN pip install pipenv \
    && pipenv install --system

# Generate a openssl key.
# We could probably use correct params instead of "localhost"
RUN openssl req -x509 -newkey rsa:4096 \
    -nodes -out src/cert.pem -keyout src/key.pem -days 365 \
    -subj '/CN=localhost'

CMD pipenv run python src/runserver.py
