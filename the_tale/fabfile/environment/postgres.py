# coding: utf-8
from fabric.api import sudo
from fabric import colors
from fabric import context_managers

from .service import Service

POSTGRES_USER = 'postgres'

class Postgres(Service):

    PACKAGES = ('postgresql', 'postgresql-server-dev-all', )
    MODES = []

    def __init__(self, project=None):
        super(Postgres, self).__init__()

        self.projects = set((project,))

    def merge(self, postgres):
        super(Postgres, self).merge(postgres)
        self.projects += postgres.projects


    def setup(self):

        for project in self.projects:
            with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
                createuser_result = sudo('createuser -D -A -R -S %(project)s' % {'project': project}, user=POSTGRES_USER)

                if createuser_result.return_code:
                    print colors.yellow('postgres user has been already created')

                sudo('psql --command="ALTER USER \\\\"%(project)s\\\\" WITH PASSWORD \'%(project)s\';"' % {'project': project}, user=POSTGRES_USER)

                createdb_result = sudo('createdb -O  %(project)s %(project)s' % {'project': project}, user=POSTGRES_USER)

                if createdb_result.return_code:
                    print colors.yellow('postgres database has been already created')
