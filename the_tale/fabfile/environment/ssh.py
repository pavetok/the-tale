# coding: utf-8
from fabric.api import cd
from .logic import sync_dir, sync_file

class SSH(object):

    def __init__(self, keys=(), authorized_keys=False):
        self.keys = set(keys)
        self.authorized_keys = authorized_keys


    def merge(self, ssh):
        self.keys += ssh.keys
        self.authorized_keys = self.authorized_keys or ssh.authorized_keys

    def setup(self, user):

        if not self.keys and not self.authorized_keys:
            return

        with cd('/home/%(username)s' % {'username': user.name}):
            sync_dir('./.ssh', user.name, '700')

            sync_file('./users/%(username)s/.ssh/authorized_keys' % {'username': user.name}, './.ssh/authorized_keys', owner=user.name, mode='600')
            sync_file('./users/%(username)s/.ssh/id_rsa' % {'username': user.name}, './.ssh/id_rsa', owner=user.name, mode='600')
            sync_file('./users/%(username)s/.ssh/id_rsa.pub' % {'username': user.name}, './.ssh/id_rsa.pub', owner=user.name, mode='644')
