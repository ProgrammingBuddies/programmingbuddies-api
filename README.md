# Programming Buddies API
API backend for Programming Buddies (projects management)

## Tech Stack
- Python 3.7
- Flask
- MySql
- pyOpenSSL

## Set up guide
- make sure you have `pipenv` installed
- Download  and install MySQL Community Server from `https://dev.mysql.com/downloads/mysql/`
- `git clone https://github.com/ProgrammingBuddies/programmingbuddies-api.git`
- `cd programmingbuddies-api`
- `pipenv install`
- - if you have multiple Python versions installed you might need to specify which one to use `pipenv install --python=python3.7`
- create a file `.env`
- - add line `FLASK_ENV=development` to have the server automatically restart on file changes
- - add line `CONNECT=mysql+pymysql://<user>:<password>@localhost:3306/<database name>` to specify connection parameters
- `pipenv run python src/runserver.py`
- - run with flag `--reset-db` to recreate all tables on start

## Milestones
- [ ] build DB and endpoints with basic CRUD
- [ ] add security for app (ie - bots, and non-human actors/clients)
- [ ] add users and profile stores as well as registration/management API endpoints for users
