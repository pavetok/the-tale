# coding: utf-8
import copy
import itertools

from fabric.api import sudo, cd

from .logic import sync_template_file

from .service import Service
from .user import User

APACHE_USER = 'www-data'

class Apache(Service):

    PACKAGES = ('apache2', 'libapache2-mod-wsgi')
    MODES = []

    def __init__(self, project=None, modes=()):
        super(Apache, self).__init__()

        self._users = {APACHE_USER: User(APACHE_USER, groups=[project]) }

        self.modes = set(modes)
        self.projects = set() if project is None else set((project,))

    def merge(self, apache):
        super(Apache, self).merge(apache)
        self.projects += apache.projects
        self.modes += apache.modes

        users = copy.deepcopy(self._users)

        for user in apache._users.values:
            if user.name not in users:
                users[user.name] = copy.deepcopy(user)
            else:
                users[user.name].merge(user)

        self._users = users



    def setup(self):
        sync_template_file('./apache2/httpd.conf', '/etc/apache2/httpd.conf', owner='root', mode='644')

        for project in self.projects:
            project_config = '/etc/apache2/sites-available/%(project)s' % {'project': project}
            config_link = '/etc/apache2/sites-enabled/%(project)s' % {'project': project}

            sync_template_file('./apache2/sites-available/django', project_config, owner='root', mode='644')
            sudo('rm -f "%(config_link)s"' % {'config_link': config_link})
            sudo('ln -s "%(project_config)s" "%(config_link)s"' % {'project_config': project_config, 'config_link': config_link})

            with cd('/home/%(project)s' % {'project': project}):
                sync_template_file('./project/conf/503.html', './conf/503.html', owner='the-tale', mode='640')
                sync_template_file('./project/conf/wsgi.py', './conf/wsgi.py', owner='the-tale', mode='640')
                sync_template_file('./project/conf/settings_local.py', './conf/settings_local.py', owner='the-tale', mode='640')


        for mode in itertools.chain(self.modes, self.MODES):
            sudo('a2enmod %s' % mode)

        sudo('service apache2 restart')
