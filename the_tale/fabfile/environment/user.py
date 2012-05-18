# coding: utf-8

from fabric.api import sudo, run
from fabric import colors
from fabric import context_managers

from .ssh import SSH


class User(object):

    def __init__(self, name, ssh=None, groups=[]):
        self.name = name
        self.ssh = ssh if ssh is not None else SSH()
        self.groups = set([name] + list(groups))

    def merge(self, user):

        if self.name != user.name:
            raise Exception('can not merge users with different names: "%s" and "%s"' % (self.name, user.name))

        self.ssh.merge(user.ssh)
        self.groups |= user.groups


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

        self.ssh.setup(self)
