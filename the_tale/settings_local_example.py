# coding: utf-8
import sys

TESTS_RUNNING = 'test' in sys.argv or 'testserver' in sys.argv

DEBUG = 'runserver' in sys.argv

GAME_ENABLE_WORKER_HIGHLEVEL = True#False
GAME_ENABLE_WORKER_TURNS_LOOP = False
GAME_ENABLE_PVP = True

GAME_ENABLE_DATA_REFRESH = False

POST_SERVICE_ENABLE_MESSAGE_SENDER = False

PORTAL_ENABLE_WORKER_LONG_COMMANDS = True

PAYMENTS_ENABLE_REAL_PAYMENTS = True
PAYMENTS_XSOLLA_ENABLED = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/emails'

PVP_BALANCING_WITHOUT_LEVELS = True
PVP_BALANCING_TIMEOUT= 10

SITE_URL = 'localhost:8000'

GA_CODE = None
ADDTHIS = False
MAIL_RU = False

NEWRELIC_ENABLED = False

CDNS_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'the-tale',
        'USER': 'the-tale',
        'PASSWORD': 'the-tale',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': 0
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

if TESTS_RUNNING:
    SOUTH_TESTS_MIGRATE = False
    SKIP_SOUTH_TESTS = True
    PVP_BALANCING_WITHOUT_LEVELS = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'the_tale.sqlite',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'CONN_MAX_AGE': 0
            }
        }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }


PAYMENTS_XSOLLA_ENABLED = True
PAYMENTS_XSOLLA_MARKETPLACE = 'paydesk'
PAYMENTS_XSOLLA_BASE_LINK= u'https://secure.xsolla.com/paystation2/'
PAYMENTS_XSOLLA_THEME=101
PAYMENTS_XSOLLA_PROJECT=10519
PAYMENTS_XSOLLA_PID = 26
