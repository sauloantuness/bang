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
