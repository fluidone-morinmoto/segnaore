#! /bin/bash


if [ -z $1 ]; then
echo "Argument missing. Pass a filename like 'local' for create 'settings/local.py file'"
exit
fi


settings_name=$1

pip install -r requirements.txt

python manage.py  migrate --settings="settings.${settings_name}"
python manage.py  collectstatic --settings="settings.${settings_name}"
python manage.py  test --settings="settings.${settings_name}"
