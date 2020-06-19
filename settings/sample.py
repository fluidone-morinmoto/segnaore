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

DEFAULT_FROM_EMAIL = 'admin@yourdomanin.ext'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.yourdomain.ext'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourusername'
EMAIL_HOST_PASSWORD = 'P4ssw0rd_Sp01l3r'
