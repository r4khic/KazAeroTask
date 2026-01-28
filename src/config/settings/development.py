"""
Development settings.
"""
import os
from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'helpdesk'),
        'USER': os.environ.get('POSTGRES_USER', 'helpdesk'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'helpdesk'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import re
    match = re.match(
        r'postgres://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<name>.+)',
        DATABASE_URL
    )
    if match:
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': match.group('name'),
            'USER': match.group('user'),
            'PASSWORD': match.group('password'),
            'HOST': match.group('host'),
            'PORT': match.group('port'),
        }
