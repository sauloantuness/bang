# Bang
Bang is a set of tools designed to assist student training and team formation for programming competitions


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python
- PostegreSQL

### Installation
#### Update your OS
```
sudo apt-get update
```

#### Install Python
```
sudo apt-get python-pip python-dev python3-dev
```


#### Python Virtual Enviroment (recommended)
```
pip install virtualenvwrapper
```
Note: Maybe will be necessary to add the follow line at the end of the .bashrc file and restart the bash console:
```
source /usr/local/bin/virtualenvwrapper.sh
```

#### PostgreSQL
```
sudo apt-get install libpq-dev postgresql postgresql-contrib
```

#### Install requirements
```
pip install -r ~/dev/projects/bang/requirements.txt
```

### Settings
#### Create database and admin user
```
sudo su - postgres
psql
CREATE DATABASE bang;
CREATE USER admin WITH PASSWORD 'admin';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
ALTER USER admin CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE bang TO admin;

\q
exit
```

#### Run database migrations
```
python manage.py makemigrations home
python manage.py migrate
```

#### Create a super user
```
python manage.py createsuperuser --username admin --email admin@email.com
```

## Running the tests
```
python manage.py test
```
