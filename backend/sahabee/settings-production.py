import os
from sahabee.settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy')
DATABASES['default']['NAME'] = '/database/db.sqlite3'
DRF_RECAPTCHA_TESTING = False
