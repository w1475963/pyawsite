#!/bin/bash

cd $PROJECT_ROOT
if [ "$IS_WEB" = "1" ]; then
  git pull
  git gc --prune=2.day.ago
fi

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

mkdir -p $PROJECT_ROOT/repos
mkdir -p $PROJECT_ROOT/static/dist

if [ "$DJANGO_DEBUG" != "1" ]; then
  python manage.py collectstatic --noinput
fi
