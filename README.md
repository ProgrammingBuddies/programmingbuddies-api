# Programming Buddies API

API backend for Programming Buddies (projects management)

## Set up guide: The simple way

Install [docker-compose](https://docs.docker.com/compose/install/) and do `docker-compose up`. Don't forget to setup your
[environment](#environment)!

## Set up guide: The 'bothersome' way

Requirements:

- [MySQL Community Server](`https://dev.mysql.com/downloads/mysql/`)
- Pipenv
  1. run `python -m pip install pipenv` to install pipenv
  2. run `pipenv install` inside the repository
     - if you have multiple Python versions installed you might need to specify which one to use `pipenv install --python=python3.7`
- SSL
  1. On Mac or Linux install the openssl tool and run `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365` inside the repository
  2. On windows ... explanation will follow.

## Environment

1. Create a file named `.env`
   - add line `FLASK_ENV=development` to have the server automatically restart on file changes
   - add line `CONNECT=mysql+pymysql://<user>:<password>@localhost:3306/<database name>` to specify connection parameters
2. `pipenv run python src/runserver.py`
   - run with flag `--reset-db` to recreate all tables on start
3. Add line `APP_SECRET=somepassword` as app secret. This is used to sign sessions among other things and is required
4. Obtain credentials for Github
   - Under your github account Settings go to Developer Settings and OAuth Apps
   - create a new one and set the homepage url to `https://localhost:5001/` and Authorization callback to `https://localhost:5001/login/github/authorized`
   - Copy the Client Id and Client Secret from that site and save them in `.env`as `GITHUB_ID` and `GITHUB_SECRET` respectively

Your `.env` file should now look something like [example.env](https://github.com/ProgrammingBuddies/programmingbuddies-api/blob/develop/example.env)

## Technologies used:

- Python
- Flask
- MySql
- pyOpenSSL
