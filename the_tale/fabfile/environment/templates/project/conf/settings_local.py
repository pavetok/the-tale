# coding: utf-8

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'the-tale',
        'USER': 'the-tale',
        'PASSWORD': 'the-tale',
        'HOST': 'localhost',
        'PORT': '',
    }
}

AMQP_BROKER_USER = 'the-tale'
AMQP_BROKER_PASSWORD = 'the-tale'
AMQP_BROKER_VHOST = '/the-tale'

DCONT_DIR = "/home/the-tale/dcont/"

SERVER_EMAIL = 'game@the-tale.org'
ADMINS = (('Tiendil', 'a.eletsky@gmail.com'), )
EMAIL_HOST = 'localhost'
