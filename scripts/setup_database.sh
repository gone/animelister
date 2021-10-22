#!/bin/bash

RESULT=`psql -l | grep "animelister" | wc -l | awk '{print $1}'`;
if test $RESULT -eq 0; then
    echo "Creating Database";
    psql -c "create role animelister with createdb encrypted password 'animelister' login;"
    psql -c "alter user animelister superuser;"
    psql -c "create database animelister with owner animelister;"
else
    echo "Database exists"
fi

#run initial setup of database tables
python manage.py migrate
