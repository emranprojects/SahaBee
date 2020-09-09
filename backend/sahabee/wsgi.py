"""
WSGI config for sahabee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sahabee.settings')
if settings.BASE_DIR not in sys.path:
    sys.path.append(settings.BASE_DIR)
application = get_wsgi_application()
