#!/bin/bash

cd ${PROJECT_ROOT:?"Error: PROJECT_ROOT 环境变量未定义！"}

if [ "$IS_WEB" = "1" ]; then
  git pull
  git gc --prune=2.day.ago
fi

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

mkdir -p $PROJECT_ROOT/repos

if [ "$IS_WEB" = "1" ]; then
  python ./pyawsite/repo_applications.py update-repos
fi

if [ "$DJANGO_DEBUG" != "1" ]; then
  python manage.py collectstatic --noinput
fi
