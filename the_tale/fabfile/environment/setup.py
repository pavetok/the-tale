# coding: utf-8
import os
import tempfile

from fabric.api import task, sudo, run, cd, put
from fabric import colors
from fabric import context_managers


TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

@task
def environment_setup():
    sync_user('the-tale')

    sync_package_manager()

    for package_name in ['apache2',
                         'postgresql',
                         'rabbitmq-server',
                         'python-pip',
                         'git',
                         'emacs',
                         'postgresql-server-dev-all',
                         'gcc',
                         'python-dev',
                         'libapache2-mod-wsgi',
                         'psmisc']:
        sync_package(package_name)

    sync_postfix()
    sync_pip_package('virtualenv')

    with cd('/home/the-tale'):
        sync_virtualenv('./env')

        sync_dir('./dcont', 'the-tale', '644') # 777
        sync_dir('./conf', 'the-tale', '644')
        sync_dir('./logs', 'the-tale', '644')
        sync_dir('./static', 'the-tale', '644')

        sync_template_file('./project/conf/503.html', './conf/503.html', owner='root', mode='644')
        sync_template_file('./project/conf/wsgi.py', './conf/wsgi.py', owner='root', mode='644')
        sync_template_file('./project/conf/settings_local.py', './conf/settings_local.py', owner='root', mode='644')

        with context_managers.prefix('. ./env/bin/activate'):
            for pip_package_name in ['kombu', 'psycopg2', 'south', 'postmarkup', 'markdown', 'pymorphy', 'xlrd', 'mock']:
                sync_pip_package(pip_package_name)


def sync_user(username):
    user_data = run('id "%(username)s"' % {'username': username})

    if user_data.return_code == 1:
        sudo('useradd "%(username)s" -d "/home/%(username)s" -m -s /bin/bash -U' % {'username': username})
        print colors.green(u'user "%(username)s" created' % {'username': username})
    else:
        print colors.green(u'user "%(username)s" has been already exists' % {'username': username})


def sync_dir(path, owner, mode, group=None):

    if group is None:
        group = owner

    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        is_path_exists = sudo('ls "%(path)s"' % {'path': path})

    if is_path_exists.return_code == 2:
        sudo('mkdir "%(path)s"' % {'path': path})
    else:
        pass

    sudo('chmod %(mode)s "%(path)s"' % {'path': path, 'mode': mode})
    sudo('chown "%(owner)s:%(group)s" "%(path)s"' % {'path': path, 'owner': owner, 'group': group})

    print colors.green(u'directory "%(path)s" has been synced' % {'path': path})


def sync_template_file(source, destination, owner, mode, context=None, group=None):
    if group is None:
        group = owner

    tmp_file = tempfile.TemporaryFile()

    from jinja2 import Environment, FileSystemLoader
    jenv = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    text = jenv.get_template(source).render(**context or {})

    tmp_file.write(text.encode('utf-8'))
    put(tmp_file, destination, use_sudo=True)

    tmp_file.close()

    sudo('chmod %(mode)s "%(destination)s"' % {'destination': destination, 'mode': mode})
    sudo('chown "%(owner)s:%(group)s" "%(destination)s"' % {'destination': destination, 'owner': owner, 'group': group})

    print colors.green(u'file "%(destination)s" has been synced' % {'destination': destination})



def sync_package_manager():
    sudo('aptitude update')
    sudo('aptitude upgrade -y')
    print colors.green(u'package manager synced')


def sync_package(package_name):
    sudo('aptitude install -y "%(package_name)s"' % {'package_name': package_name})
    print colors.green(u'package "%(package_name)s" synced' % {'package_name': package_name})


def sync_pip_package(package_name):
    sudo('pip install "%(package_name)s"' % {'package_name': package_name})
    print colors.green(u'pip package "%(package_name)s" synced' % {'package_name': package_name})

def sync_virtualenv(venv_path):
    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        is_path_exists = sudo('ls "%(venv_path)s"' % {'venv_path': venv_path})

    if is_path_exists.return_code == 2:
        sudo('virtualenv "%(venv_path)s"' % {'venv_path': venv_path})
    else:
        pass

    print colors.green(u'virtualenv synced')


def sync_postfix():
    # "with" statement need for non-interactive posrfix instllation
    with context_managers.prefix('export DEBIAN_FRONTEND=noninteractive'):
        sync_package('postfix')

    sync_template_file('./postfix/main.cf', '/etc/postfix/main.cf', owner='root', mode='644')
