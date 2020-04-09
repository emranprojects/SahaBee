from sahabee.settings import *

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
SECRET_KEY = os.environ.get('SAHABEE_SECRET_KEY', 'dummy')
DATABASES['default']['NAME'] = '/database/db.sqlite3'