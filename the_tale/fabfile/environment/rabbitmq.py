# coding: utf-8

from fabric.api import sudo
from fabric import colors
from fabric import context_managers

from .service import Service


class RabbitMQ(Service):

    PACKAGES = ('rabbitmq-server', )

    def __init__(self, project=None):
        super(RabbitMQ, self).__init__()

        self.projects = set() if project is None else set((project,))

    def merge(self, rabbit):
        super(RabbitMQ, self).merge(rabbit)
        self.projects += rabbit.projects


    def setup(self):

        for project in self.projects:
            with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
                add_user_result = sudo('rabbitmqctl add_user "%(project)s" "%(project)s"' % {'project': project})

            if add_user_result.return_code:
                print colors.yellow('rabbitmq user has been already created')

            add_vhost_result = sudo('rabbitmqctl add_vhost "/%(project)s"' % {'project': project})

            if add_vhost_result.return_code:
                print colors.yellow('rabbitmq vhost has been already created')

            sudo('rabbitmqctl  set_permissions -p "/%(project)s" "%(project)s" ".*" ".*" ".*"' % {'project': project})
