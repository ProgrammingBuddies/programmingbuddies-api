"""
This script runs the api application using a development server.
"""

from os import environ
from api import app
from secrets import token_urlsafe

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5001'))
    except ValueError:
        PORT = 5001
    if environ.get('FLASK_ENV', 'production') == 'development':
        app.run(HOST, PORT, ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(HOST, PORT)
