# -*- coding: utf-8 -*-

DEBUG = True
#DEBUG_DB = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'the_tale',
        'USER': 'the_tale',
        'PASSWORD': 'the_tale',
        'HOST': '',
        'PORT': '',
    }
}

NEWS_FORUM_CATEGORY_SLUG = 'c3s1'
