# Programming Buddies API

API backend for [Programming Buddies](https://github.com/ProgrammingBuddies/programmingbuddies-ui) (projects management)

## Set up guide: The simple way

- Set up your [environment](#environment)
- Install [docker-compose](https://docs.docker.com/compose/install/) and do `docker-compose up`

## Set up guide: The 'bothersome' way

Requirements:

- Set up your [environment](#environment)
- [MySQL Community Server](`https://dev.mysql.com/downloads/mysql/`)
    - Add line `CONNECT=mysql+pymysql://<user>:<password>@localhost:3306/<database name>` to your [`.env` file](#environment) to specify connection parameters
- Pipenv
    1. Run `python -m pip install pipenv` to install pipenv
    2. Run `pipenv install` inside the repository
        - If you have multiple Python versions installed you might need to specify which one to use `pipenv install --python=python3.7`
- SSL
    1. On Mac or Linux install the openssl tool and run `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365` inside the repository
    2. On Windows ... explanation will follow.

Run the server:
- `pipenv run python src/runserver.py`
    - Run with flag `--reset-db` to drop and recreate all tables on start

## Environment

1. Create a file named `.env`
    - Add line `FLASK_ENV=development` to have the server automatically restart on file changes
2. Add line `APP_SECRET=somepassword` as app secret. This is used to sign sessions among other things and is required
3. Obtain credentials for GitHub OAuth
    - Under your GitHub account Settings go to Developer settings and OAuth Apps
    - Create a new one and set the homepage url to `https://localhost:5001/` and Authorization callback to `https://localhost:5001/login/github/authorized`
    - Copy the Client Id and Client Secret from that site and save them in `.env` as `GITHUB_ID` and `GITHUB_SECRET` respectively
4. Furthermore a `JWT_SECRET_KEY` is required for signing the JWT-tokens

Your `.env` file should now look something like [example.env](https://github.com/ProgrammingBuddies/programmingbuddies-api/blob/develop/example.env)

## Tech stack:

- Python
- Flask
- MySQL
- pyOpenSSL
