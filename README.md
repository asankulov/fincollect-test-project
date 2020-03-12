# Fincollect Test Project

## Prerequisites

1. Installed Python3.x
2. Installed pipenv
3. Postgres database and user with createdb privilege

## Steps to launch

1. Create new `pipenv` environment
2. Install from `Pipfile`
3. Create `.env` file within postgres db credentials
4. Run `python manage.py migrate`
5. Run `python manage.py renew_table`
6. Finally run `python manage.py runserver <port>`

To run tests simply `python manage.py test`
To see coverage reports open `htmlcov/index.html` in browser

To schedule cronjob you need to edit `cron-job` file by specify project root dir and pipenv full path
