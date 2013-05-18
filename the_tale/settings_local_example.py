# -*- coding: utf-8 -*-
import sys

TESTS_RUNNING = 'test' in sys.argv or 'testserver' in sys.argv

DEBUG = 'runserver' in sys.argv

# DEBUG_DATABASE_USAGE = True
# DEBUG_DATABASE_USAGE_OUTPUT_DIR = '/home/tie/tmp/db/'

GAME_ENABLE_WORKER_HIGHLEVEL = True
GAME_ENABLE_WORKER_TURNS_LOOP = False
GAME_ENABLE_WORKER_MIGHT_CALCULATOR = False
GAME_ENABLE_PVP = True

GAME_ENABLE_DATA_REFRECH = False

POST_SERVICE_ENABLE_MESSAGE_SENDER = False

PORTAL_ENABLE_WORKER_LONG_COMMANDS = False


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/emails'

PVP_BALANCING_WITHOUT_LEVELS = True

SITE_URL = 'localhost:8000'

GA_CODE = None
ADDTHIS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'the-tale',
        'USER': 'the-tale',
        'PASSWORD': 'the-tale',
        'HOST': '',
        'PORT': '',
    }
}

if TESTS_RUNNING:
    SOUTH_TESTS_MIGRATE=False
    SKIP_SOUTH_TESTS=True
    PVP_BALANCING_WITHOUT_LEVELS = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'the_tale.sqlite',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
        }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
