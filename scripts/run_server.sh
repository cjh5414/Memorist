#!/bin/bash
source ~/.bash_profile
cd /home/jihun/Memorist;
git pull origin master;
pyenv activate Memorist;
pip install -r requirements.txt;
cd /home/jihun/Memorist/memorist;
python manage.py migrate;
python manage.py collectstatic --noinput;
killall uwsgi;
uwsgi --ini memorist_uwsgi.ini;
pyenv deactivate;
