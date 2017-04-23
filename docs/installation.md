# Installation


## Update

```
sudo apt-get update
```


## GIT

```
sudo apt-get install git
```


## Python

```
sudo apt-get python-pip python-dev python3-dev
pip install --upgrade pip
```


## Python Virtual Enviroment

```
pip install virtualenvwrapper
```

Note: Maybe will be necessary to add the follow line at the end of the .bashrc file and restart the bash console:

```
source /usr/local/bin/virtualenvwrapper.sh
```


## Apache

```
sudo apt-get install apache2 libapache2-mod-wsgi-py3
```


## PostegreSQL

```
sudo apt-get install libpq-dev postgresql postgresql-contrib
```


# Settings

## Apache

```
sudo touch /etc/apache2/sites-available/bang.conf
```

```
# bang.conf

<VirtualHost *:80>
    ServerName maratona.decom.cefetmg.br

    Alias /static /home/saulo/dev/projects/bang/staticroot

    <Directory /home/saulo/dev/projects/bang/staticroot>
        Require all granted
    </Directory>
    
    <Directory /home/saulo/dev/projects/bang/bang>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    WSGIProcessGroup bang
    WSGIDaemonProcess bang python-home=/home/saulo/.virtualenvs/bang/bin/python python-path=/home/saulo/dev/projects/bang
    WSGIScriptAlias / /home/saulo/dev/projects/bang/bang/wsgi.py
</VirtualHost>
```

```
sudo a2ensite bang.conf
sudo service apache2 restart
```

If necessary, this is where the apache logs are:

```
/var/log/apache2/
```


## PostegreSQL

```
sudo su - postgres
psql
```

```
DROP DATABASE bang;
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


## The Code

Clone the repository:

```
$ git clone https://github.com/sauloantuness/bang.git ~/dev/projects
```

Install the requirements:

```
$ pip install -r ~/dev/projects/bang/requirements.txt
```

Run the migrations:

```
$ python manage.py makemigrations home
$ python manage.py migrate
```

Create a super user:

```
$ python manage.py createsuperuser --username admin --email admin@email.com
```

Run the commands to populate the database:

```
$ python manage.py updateUriSolutions
$ python manage.py updateUvaSolutions
```

Add the follow line to the `crontab -e`:

```shell
#!/bin/bash
# substituir "/home/admin/env/bang/bang/" até o path do cron.sh
*/5 * * * *  /home/saulo/dev/projects/bang/scripts/cron.sh >> /home/saulo/dev/projects/bang/scripts/logs/update.log 2>&1
```

To see the cron logs:

```
# cat /var/log/syslog | grep CRON
```
