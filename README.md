# Programming Buddies API
API backend for Programming Buddies (projects management)

## Tech Stack
- Python 3.7
- Flask
- MySql
- pyOpenSSL

## Set up guide
- Download and install MySQL Community Server from `https://dev.mysql.com/downloads/mysql/`
- `git clone https://github.com/ProgrammingBuddies/programmingbuddies-api.git`

### The simple way

Install docker-compose and do `docker-compose up`. Don't forget to setup your
.env file.

### Pipenv
- run `python -m pip install pipenv` to install pipenv
- run `pipenv install` inside the repository
- - if you have multiple Python versions installed you might need to specify which one to use `pipenv install --python=python3.7`

### SSL
- On Mac or linux install the openssl tool and run `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365` inside the repository
- On windows 
    1. Install OpenSSL for Windows [here](https://slproweb.com/products/Win32OpenSSL.html)
    2. Execute the same command as on Mac inside the project directory.

### Environment
- create a file `.env`
- - `.env` in this case is the full filename and not just the extension. `app.env` for example would not be loaded automatically by pipenv
- - add line `FLASK_ENV=development` to have the server automatically restart on file changes
- - add line `CONNECT=mysql+pymysql://<user>:<password>@localhost:3306/<database name>` to specify connection parameters
- `pipenv run python src/runserver.py`
- - run with flag `--reset-db` to recreate all tables on start
- add line `APP_SECRET=somepassword` as app secret. This is used to sign sessions among other things and is required
- Optain credentials for Github
- - Under your github account Settings go to Developer Settings and OAuth Apps
- - create a new one and set the homepage url to `https://localhost:5001/` and Authorization callback to `https://localhost:5001/login/github/authorized`
- - Copy the Client Id and Client Secret from that site and save them in `.env`as `GITHUB_ID` and `GITHUB_SECRET` respectively

Your `.env` file should now look something like [example.env](https://github.com/ProgrammingBuddies/programmingbuddies-api/blob/develop/example.env)

## Milestones
- [ ] build DB and endpoints with basic CRUD
- [ ] add security for app (ie - bots, and non-human actors/clients)
- [ ] add users and profile stores as well as registration/management API endpoints for users
