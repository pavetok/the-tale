# coding: utf-8

from fabric.api import sudo, cd

from fabfile.utils import is_path_exists
from fabric import context_managers

from .service import Service


class Python(Service):

    PACKAGES = ('python', 'python-pip')

    def __init__(self, project=None, packages=()):
        super(Python, self).__init__()
        self.projects = {project: set(packages)}


    @property
    def required_packages(self):
        packages = super(Python, self).required_packages

        all_pip_packages = []
        for pip_packages in self.projects.values():
            all_pip_packages.extend(pip_packages)

        if set(['psycopg2']) & set(all_pip_packages):
            packages |= set(('gcc', 'python-dev'))

        return packages


    def merge(self, python):
        super(Python, self).merge(python)

        for project_name, project_packages in python.projects.items():
            if project_name in self.projects:
                self.projects[project_name] += project_packages
            else:
                self.projects[project_name] = project_packages

    def get_packages_for_project(self, project):
        if project is None:
            return self.projects.get(None, []) + ['virtualenv']
        return self.projects[project]

    def install_packages(self, project):
        cmd = 'pip install %(packages)s' % {'packages': ' '.join(self.get_packages_for_project(project))}

        if project is None:
            sudo(cmd)
        else:
            sudo(cmd, user=project)


    def setup(self):

        self.install_packages(None)

        for project, project_packages in self.projects.items():

            if project is None:
                continue

            with cd('/home/%(project)s' % {'project': project}):

                venv_path = './env'
                if not is_path_exists(venv_path, use_sudo=True):
                    sudo('virtualenv "%(venv_path)s"' % {'venv_path': venv_path}, user='the-tale')


                with context_managers.prefix('. ./env/bin/activate'):
                    sudo('pip install pip==1.0.2', user=project) # TODO: remove when pip > 1.1 become available, see: https://github.com/pypa/pip/issues/486

                    self.install_packages(project)
