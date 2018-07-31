# MyDiaryDB_ API

MyDiary is an online journal where users can pen down their thoughts and feelings,view them later and also make changes.


## Requirements Building blocks.

Python3 - A programming language that lets us work more quickly (The universe loves speed!).

Flask - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.

Virtualenv - A tool to create isolated virtual environment

-Postgres - PostgreSQL is a powerful, open source object-relational database system with over 30 years
 of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

## Installation on Windows
First clone this repository

 git clone @https://github.com/minatah/Challenge_3/tree/develop

 cd challenge_3

Create virtual environment and install it on Windows

virtualenv --python=python3 venv
.\venv\bin\activate.bat

Then install all the necessary dependencies by

pip install -r requirements.txt
Then run the application

python run.py
Testing and knowing coverage run

nosetests or python manage.py test
Endpoints to create a user account and login into the application
HTTP Method	End Point	Action
| POST	api/v1/user/register	Create an account
| POST	/api/v1/login	Login user

## Other Endpoints.
| HTTP Method	End Point	Action
| POST	/api/v1/users/rides	Creates ride offers.
| GET	/api/v1/users/rides	Login user.
| GET	/api/v1/rides/	Get specific ride offer by ID.
| POST	/rides//requests	Makes a ride request.
| GET	/users/rides//requests	Fetch all ride requests.
| PUT	/users/rides//requests/	Accept or reject a ride request.


## Author: 
Namiiro Aminah

