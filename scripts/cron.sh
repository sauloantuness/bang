#!/bin/bash
# substituir 	/home/admin/env/bang/bang/ até o path do cron.sh
# */5 * * * *  /home/admin/env/bang/bang/cron.sh >> /home/admin/env/bang/bang/log 2>&1

BASEDIR=$(dirname "$0")
PYTHONDIR="/home/saulo/.virtualenvs/bang/bin/python"
COMMAND1=$BASEDIR"/manage.py updateUriSolutions"
COMMAND2=$BASEDIR"/manage.py updateUvaSolutions"

echo -n "BEGIN: "
date +"%D %T"

$PYTHONDIR $COMMAND1
$PYTHONDIR $COMMAND2

echo -n "END: "
date +"%D %T"
echo "-----------------------------------------"