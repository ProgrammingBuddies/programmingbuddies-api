"""
This script runs the api application using a development server.
"""

from os import environ
from flask_swagger_ui import get_swaggerui_blueprint
from api import app

# swagger specific
SWAGGER_URL = '/docs'
API_URL = '/spec'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': "Programing Buddies API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# end swagger specific

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
