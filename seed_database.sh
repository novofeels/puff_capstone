#!/bin/bash

rm db.sqlite3
rm -rf ./puffapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations puffapi
python3 manage.py migrate puffapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata scores
python3 manage.py loaddata achievements
python3 manage.py loaddata userAchievements
python3 manage.py loaddata feedback
