# make sure you start this its take more then 2 terminal's
celery -A clinic worker -l info -P solo

python manage.py runserver


# important installation
sudo apt install redis-server -y

sudo service redis-server start

redis-cli ping

