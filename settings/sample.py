from .default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'username',
        'PASSWORD': 'sp01l3r_s3cr3t',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Logging
LOGGING['loggers']['base']['handlers'].append('dev_file')
LOGGING['handlers']['file']['filename'] = '/path/to/file.log'
LOGGING['handlers']['file_stage']['filename'] = '/path/to/file.log'
LOGGING['handlers']['dev_file']['filename'] = '/path/to/file_dev.log'
LOGGING['handlers']['file_json']['filename'] = '/path/to/file_json.log'
