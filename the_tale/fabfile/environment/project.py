# coding: utf-8

from fabric.api import cd

from .logic import sync_dir

class Project(object):

    def __init__(self, name, users=(), packages=(), services=()):
        if not users:
            raise Exception('at most one user MUST be specified for project')

        self._users = users
        self._services = services

        self.name = name
        self.users = set(user.name for user in self._users)
        self.packages = set(packages)

        if self.name not in self.users:
            raise Exception('project MUST contain user with name equal to project name')


    def setup(self):

        with cd('/home/%(projectname)s' % {'projectname': self.name}):
            sync_dir('./dcont', self.name, '755')
            sync_dir('./conf', self.name, '750')
            sync_dir('./logs', self.name, '750')
            sync_dir('./static', self.name, '755')
