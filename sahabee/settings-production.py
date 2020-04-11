from sahabee.settings import *

DEBUG = False
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    os.environ.get('PRODUCTION_IP')]
SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy')
DATABASES['default']['NAME'] = '/database/db.sqlite3'