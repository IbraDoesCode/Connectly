"""
WSGI config for connectly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils.logger import Logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connectly.settings')

logger = Logger().get_logger()
logger.info("API Initialized Successfully")

application = get_wsgi_application()
