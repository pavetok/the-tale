# -*- coding: utf-8 -*-
import sys

TESTS_RUNNING = 'test' in sys.argv or 'testserver' in sys.argv

DEBUG = True
#DEBUG_DB = True

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

NEWS_FORUM_CATEGORY_SLUG = 'c3s1'
