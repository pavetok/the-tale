# coding: utf-8
import copy

from fabric.api import sudo
from fabric import colors
from fabric import context_managers


class Host(object):

    def __init__(self, name, users=(), projects=(), packages=(), services=(), upgrade=False):
        self._users = users
        self._projects = projects
        self._services = services

        self.name = name
        self.projects = {}
        self.services = {}
        self.users = {}
        self.packages = set(packages)
        self.upgrade = upgrade


    def sync(self):
        self.sync_projects()
        self.sync_services() # before users (see apache)
        self.sync_users()
        self.sync_packages() # after all

    def sync_projects(self):
        projects = dict( (project.name, project) for project in copy.deepcopy(self._projects))

        self.projects = projects


    def sync_users(self):
        users = dict( (user.name, user) for user in copy.deepcopy(self._users))

        for project in self.projects.values():
            for user in project._users:
                if user.name not in users:
                    users[user.name] = copy.deepcopy(user)
                else:
                    users[user.name].merge(user)

        for service in self.services.values():
            for user in service._users.values():
                if user.name not in users:
                    users[user.name] = copy.deepcopy(user)
                else:
                    users[user.name].merge(user)

        self.users = users


    def sync_services(self):

        services = dict( (service.name, service) for service in copy.deepcopy(self._services))

        for project in self.projects.values():
            for service in project._services:
                if service.name not in services:
                    services[service.name] = copy.deepcopy(service)
                else:
                    services[service.name].merge(service)

        self.services = services


    def sync_packages(self):

        for project in self.projects.values():
            self.packages |= project.packages

        for service in self.services.values():
            self.packages |= service.required_packages



    def setup(self):

        print colors.green(u'setup packages')

        sudo('aptitude update')

        if self.upgrade:
            sudo('aptitude upgrade -y')

        prefix = []
        packages = []

        for package in self.packages:
            if isinstance(package, (tuple, list)):
                prefix.append(package[1])
                packages.append(package[0])
            else:
                packages.append(package)

        with context_managers.prefix(' && '.join(prefix)):
            sudo('aptitude install -y %s' % ' '.join(packages) )

        print colors.green(u'packages setuped')

        print colors.green(u'setupe users')

        for user in self.users.values():
            print colors.green(u'setup %s' % user.name)
            user.setup()

        print colors.green(u'users setuped')

        print colors.green(u'setup projects')

        for project in self.projects.values():
            print colors.green(u'setup %s' % project.name)
            project.setup()

        print colors.green(u'projects setuped')

        print colors.green(u'setupe services')

        for service in self.services.values():
            print colors.green(u'setup %s' % service.name)
            service.setup()

        print colors.green(u'services setuped')
