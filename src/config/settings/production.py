"""
Production settings.
"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import re
    match = re.match(
        r'postgres://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<name>.+)',
        DATABASE_URL
    )
    if match:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': match.group('name'),
                'USER': match.group('user'),
                'PASSWORD': match.group('password'),
                'HOST': match.group('host'),
                'PORT': match.group('port'),
            }
        }

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
