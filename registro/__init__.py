import logging
from django.conf import settings


default_app_config = 'registro.apps.RegistroConfig'

APP_VERSION = 'beta'
__version__ = APP_VERSION
__app_alias__ = 'Registro segna ore'

logger = logging.getLogger('base')

logger.debug("Starting '{}' v. {}".format(__app_alias__, __version__))
