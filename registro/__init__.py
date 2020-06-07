import logging

default_app_config = 'registro.apps.RegistroConfig'

APP_VERSION = 'beta-dev'
__version__ = APP_VERSION
__app_alias__ = 'Registro segna ore'

logger = logging.getLogger('base')

logger.debug("Starting '{}' v. {}".format(__app_alias__, __version__))
