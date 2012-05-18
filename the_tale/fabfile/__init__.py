# coding: utf-8

# from fabric.api import env
from fabfile.update import update
from fabfile.backup import backup
from fabfile.environment import environment_setup, setup

__all__ = ['update', 'backup', 'environment_setup', 'setup']

# fab update:bla="the-tale@192.168.1.102"
# env.hosts = ['the-tale@the-tale.org']
# env.hosts = ['tie@192.168.1.102']
# env.hosts = ['the-tale@192.168.1.102']
