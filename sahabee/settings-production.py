from sahabee.settings import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy')
DATABASES['default']['NAME'] = '/database/db.sqlite3'