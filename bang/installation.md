# Instalação

## Apache

```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install python-pip
sudo apt-get install libapache2-mod-wsgi-py3
```

## PostegreSQL

```
sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install python3-dev
sudo apt-get install libpq-dev
sudo apt-get install postgresql
sudo apt-get install postgresql-contrib
```

# Configuração

## Apache

```
sudo touch /etc/apache2/sites-available/bang.conf
```

```
# bang.conf

<VirtualHost *:80>
    ServerName maratona.decom.cefetmg.br

    Alias /static /home/saulo/Documents/code/env/bang/bang/staticRoot

    <Directory /home/saulo/Documents/code/env/bang/bang/staticRoot>
        Require all granted
    </Directory>
    
    <Directory /home/saulo/Documents/code/env/bang/bang>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    WSGIProcessGroup bang
    WSGIDaemonProcess bang python-path=/home/saulo/Documents/code/env/bang/bang:/home/saulo/Documents/code/env/lib/python3.4/site-packages
    WSGIScriptAlias / /home/saulo/Documents/code/env/bang/bang/bang/wsgi.py

</VirtualHost>
```

```
sudo a2ensite bang.conf
sudo service apache2 restart
```

## PostgreSQL

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
```

# Cron

```shell
#!/bin/bash
# substituir /home/saulo/Documents/code/env/bang/bang/ até o path do cron.sh
# */5 * * * * /usr/bin/time -f "Time: %Us" /home/saulo/Documents/code/env/bang/bang/cron.sh >> /home/saulo/Documents/code/env/bang/bang/log 2>&1

BASEDIR=$(dirname "$0")
PYTHONDIR=$BASEDIR"/../../bin/python"
COMMAND1=$BASEDIR"/manage.py updateUriSolutions"
COMMAND2=$BASEDIR"/manage.py updateUvaSolutions"

echo -n "BEGIN: "
date +"%D %T"

$PYTHONDIR $COMMAND1
$PYTHONDIR $COMMAND2

echo -n "END: "
date +"%D %T"
echo "-----------------------------------------"
```