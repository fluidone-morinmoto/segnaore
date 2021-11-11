#! /bin/bash


if [ -z $1 ]; then
    echo "Argument missing. Pass a filename like 'local' for create 'settings/local.py file'"
    exit
fi

settings_filename=$1
settings_filename="./settings/${settings_filename}.py"
emails_filename="./settings/email.py"

touch ${emails_filename}

echo "DEFAULT_FROM_EMAIL = ''" > ${emails_filename}
echo "EMAIL_USE_TLS = False" >> ${emails_filename}
echo "EMAIL_HOST = ''" >> ${emails_filename}
echo "EMAIL_PORT = 587" >> ${emails_filename}
echo "EMAIL_HOST_USER = ''" >> ${emails_filename}
echo "EMAIL_HOST_PASSWORD = ''" >> ${emails_filename}

touch ${settings_filename}

echo "from .default import *" >> ${settings_filename}
echo "from .email import *" >> ${settings_filename}

echo "DATABASES = {" >> ${settings_filename}
echo "    'default': {" >> ${settings_filename}
echo "        'ENGINE': 'django.db.backends.mysql'," >> ${settings_filename}
echo "        'NAME': ''," >> ${settings_filename}
echo "        'USER': ''," >> ${settings_filename}
echo "        'PASSWORD': ''," >> ${settings_filename}
echo "        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on" >> ${settings_filename}
echo "        'PORT': '3306'," >> ${settings_filename}
echo "        'OPTIONS': {" >> ${settings_filename}
echo "            'init_command': \"SET sql_mode='STRICT_TRANS_TABLES'\"," >> ${settings_filename}
echo "        }," >> ${settings_filename}
echo "    }" >> ${settings_filename}
echo "}" >> ${settings_filename}
echo "" >> ${settings_filename}
echo "LOGGING['handlers']['file']['filename'] = \"/var/log/ore/ore.log\"" >> ${settings_filename}
echo "LOGGING['handlers']['dev_file']['filename'] = \"/var/log/ore/ore_dev.log\"" >> ${settings_filename}
echo "LOGGING['loggers']['base']['handlers'].append('dev_file')" >> ${settings_filename}


echo "PRE INSTALL COMPLETED!"
echo "Now populate the '${settings_filename}' with logs and database values."
echo "Populate the '${emails_filename}' for enable user's registration."