#!/bin/bash

# wait for mysql to be ready
nc -z mysql 3306
n=$?
while [ $n -ne 0 ]; do
    sleep 1
    nc -z mysql 3306
    n=$?
done

./manage.py migrate
./manage.py runserver_plus 0.0.0.0:8000
