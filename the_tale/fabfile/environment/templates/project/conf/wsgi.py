# coding: utf-8

import os
import sys
import site

site.addsitedir('/home/the-tale/env/lib/python2.7/site-packages')

import django.core.handlers.wsgi

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

sys.path.append('/home/the-tale/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#import newrelic.agent

#newrelic.agent.initialize('/home/the-tale/conf/newrelic.ini')

application = django.core.handlers.wsgi.WSGIHandler()

#application = newrelic.agent.wsgi_application()(application)
