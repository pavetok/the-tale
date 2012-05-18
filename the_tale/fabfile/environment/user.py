# coding: utf-8

from fabric.api import sudo, run, cd
from fabric import colors
from fabric import context_managers

from .ssh import SSH

from .logic import sync_dir, sync_file

class User(object):

    def __init__(self, name, ssh=None, groups=[]):
        self.name = name
        self.ssh = ssh if ssh is not None else SSH()
        self.groups = [name] + list(groups)

    def merge(self, user):

        if self.name != user.name:
            raise Exception('can not merge users with different names: "%s" and "%s"' % (self.name, user.name))

        self.ssh.merge(user.ssh)


    def setup(self):
        with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
            user_data = run('id "%(username)s"' % {'username': self.name})

        if user_data.return_code == 1:
            sudo('useradd "%(username)s" -d "/home/%(username)s" -m -s /bin/bash -U' % {'username': self.name})
        else:
            pass

        for group_name in self.groups:
            if group_name is not self.name:
                sudo('usermod -a -G "%(group_name)s" "%(username)s"' % {'group_name': group_name, 'username': self.name})

        if self.ssh is not None:
            with cd('/home/%(username)s' % {'username': self.name}):
                sync_dir('./.ssh', self.name, '700')

                sync_file('./users/%(username)s/.ssh/authorized_keys' % {'username': self.name}, './.ssh/authorized_keys', owner='the-tale', mode='600')
                sync_file('./users/%(username)s/.ssh/id_rsa' % {'username': self.name}, './.ssh/id_rsa', owner='the-tale', mode='600')
                sync_file('./users/%(username)s/.ssh/id_rsa.pub' % {'username': self.name}, './.ssh/id_rsa.pub', owner='the-tale', mode='644')

        print colors.green(u'user "%(username)s" synced' % {'username': self.name})
