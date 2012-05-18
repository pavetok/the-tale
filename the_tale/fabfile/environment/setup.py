# coding: utf-8
import os

from fabric.api import task

from fabfile.environment.conf import HOST


TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

@task
def setup():
    HOST.sync()
    HOST.setup()


#'psmisc'

@task
def environment_setup():
    pass
