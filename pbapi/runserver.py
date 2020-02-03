"""
This script runs the pbapi application using a development server.
"""

from os import environ
from pbapi import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, ssl_context='adhoc')
    """ WIll need changed for PROD """