"""
This script runs the api application using a development server.
"""

from os import environ
from api import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5001'))
    except ValueError:
        PORT = 5001
    app.run(HOST, PORT)
