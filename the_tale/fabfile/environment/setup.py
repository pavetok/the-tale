# coding: utf-8
import os
import tempfile

from fabric.api import task, sudo, run, cd, put
from fabric import colors
from fabric import context_managers

from fabfile.utils import is_path_exists


TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

@task
def environment_setup():

    sync_package_manager()
    for package_name in ['python-pip',
                         'git',
                         'emacs',
                         'gcc',
                         'python-dev',
                         'psmisc']:
        sync_package(package_name)

    sync_postgres() #must be before psycopg2 install

    sync_user('the-tale')

    with cd('/home/the-tale'):

        sync_dir('./dcont', 'the-tale', '755')
        sync_dir('./conf', 'the-tale', '750')
        sync_dir('./logs', 'the-tale', '750')
        sync_dir('./static', 'the-tale', '755')
        sync_dir('./.ssh', 'the-tale', '700')

        sync_template_file('./project/.ssh/authorized_keys', './.ssh/authorized_keys', owner='the-tale', mode='600')
        sync_template_file('./project/.ssh/id_rsa', './.ssh/id_rsa', owner='the-tale', mode='600')
        sync_template_file('./project/.ssh/id_rsa.pub', './.ssh/id_rsa.pub', owner='the-tale', mode='644')

        sync_template_file('./project/conf/503.html', './conf/503.html', owner='the-tale', mode='640')
        sync_template_file('./project/conf/wsgi.py', './conf/wsgi.py', owner='the-tale', mode='640')
        sync_template_file('./project/conf/settings_local.py', './conf/settings_local.py', owner='the-tale', mode='640')

        sync_pip_package('virtualenv')
        sync_virtualenv('./env')

        with context_managers.prefix('. ./env/bin/activate'):
            sync_pip_package('pip', '1.0.2', user='the-tale') # TODO: remove when pip > 1.1 become available, see: https://github.com/pypa/pip/issues/486

            for pip_package_name in ['kombu', 'psycopg2', 'south', 'postmarkup', 'markdown', 'pymorphy', 'xlrd', 'mock']:
                sync_pip_package(pip_package_name, user='the-tale')

    sync_apache2() # require log directories from project
    sync_rabbitmq()
    sync_postfix()
    sync_collectd()



def sync_user(username, groups=[]):

    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        user_data = run('id "%(username)s"' % {'username': username})

    if user_data.return_code == 1:
        sudo('useradd "%(username)s" -d "/home/%(username)s" -m -s /bin/bash -U' % {'username': username})
    else:
        pass

    if groups:
        for group_name in groups:
            if group_name is not username:
                sudo('usermod -a -G "%(group_name)s" "%(username)s"' % {'group_name': group_name, 'username': username})

    print colors.green(u'user "%(username)s" synced' % {'username': username})


def sync_fs_data(path, owner, mode, group=None):
    if group is None:
        group = owner

    sudo('chmod %(mode)s "%(path)s"' % {'path': path, 'mode': mode})
    sudo('chown "%(owner)s:%(group)s" "%(path)s"' % {'path': path, 'owner': owner, 'group': group})


def sync_dir(path, owner, mode, group=None):

    if not is_path_exists(path, use_sudo=True):
        sudo('mkdir "%(path)s"' % {'path': path})
    else:
        pass

    sync_fs_data(path, owner, mode, group)

    print colors.green(u'directory "%(path)s" has been synced' % {'path': path})


def sync_template_file(source, destination, owner, mode, context=None, group=None):

    tmp_file = tempfile.TemporaryFile()

    from jinja2 import Environment, FileSystemLoader
    jenv = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    text = jenv.get_template(source).render(**context or {})

    tmp_file.write(text.encode('utf-8'))
    put(tmp_file, destination, use_sudo=True)

    tmp_file.close()

    sync_fs_data(destination, owner, mode, group)

    print colors.green(u'file "%(destination)s" has been synced' % {'destination': destination})



def sync_package_manager():
    sudo('aptitude update')
    sudo('aptitude upgrade -y')
    print colors.green(u'package manager synced')


def sync_package(package_name):
    sudo('aptitude install -y "%(package_name)s"' % {'package_name': package_name})
    print colors.green(u'package "%(package_name)s" synced' % {'package_name': package_name})


def sync_pip_package(package_name, version=None, user=None):
    if version:
        package_name = '%s==%s' % (package_name, version)

    cmd = 'pip install "%(package_name)s"' % {'package_name': package_name}

    if user is None:
        sudo(cmd)
    else:
        sudo(cmd, user=user)

    print colors.green(u'pip package "%(package_name)s" synced' % {'package_name': package_name})

def sync_virtualenv(venv_path):

    if not is_path_exists(venv_path, use_sudo=True):
        sudo('virtualenv "%(venv_path)s"' % {'venv_path': venv_path}, user='the-tale')
    else:
        pass

    print colors.green(u'virtualenv synced')


def sync_postfix():
    # "with" statement need for non-interactive posrfix instllation
    with context_managers.prefix('export DEBIAN_FRONTEND=noninteractive'):
        sync_package('postfix')

    sync_template_file('./postfix/main.cf', '/etc/postfix/main.cf', owner='root', mode='644')

    print colors.green(u'postfix synced')


def sync_apache2():
    sync_package('apache2')
    sync_package('libapache2-mod-wsgi')

    sync_template_file('./apache2/httpd.conf', '/etc/apache2/httpd.conf', owner='root', mode='644')
    sync_template_file('./apache2/sites-available/the-tale.org', '/etc/apache2/sites-available/the-tale.org', owner='root', mode='644')

    sudo('rm -f "/etc/apache2/sites-enabled/the-tale.org"')
    sudo('ln -s "/etc/apache2/sites-available/the-tale.org" "/etc/apache2/sites-enabled/the-tale.org"')

    sync_user('www-data', groups=['the-tale'])

    sudo('a2enmod rewrite')
    sudo('service apache2 restart')

    print colors.green(u'apache2 synced')


def sync_postgres():
    sync_package('postgresql')
    sync_package('postgresql-server-dev-all')

    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        createuser_result = sudo('createuser -D -A -R -S the-tale', user='postgres')

        if createuser_result.return_code:
            print colors.yellow('postgres user has been already created')

        sudo('psql --command="ALTER USER \\\\"the-tale\\\\" WITH PASSWORD \'the-tale\';"', user='postgres')

        createdb_result = sudo('createdb -O the-tale the-tale', user='postgres')

        if createdb_result.return_code:
            print colors.yellow('postgres database has been already created')

    print colors.green(u'postgres synced')


def sync_rabbitmq():
    sync_package('rabbitmq-server')

    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        add_user_result = sudo('rabbitmqctl add_user "the-tale" "the-tale"')

        if add_user_result.return_code:
            print colors.yellow('rabbitmq user has been already created')

        add_vhost_result = sudo('rabbitmqctl add_vhost "/the-tale"')

        if add_vhost_result.return_code:
            print colors.yellow('rabbitmq vhost has been already created')

        sudo('rabbitmqctl  set_permissions -p "/the-tale" "the-tale" ".*" ".*" ".*"')

    print colors.green(u'rabbitmq synced')


def sync_collectd():
    sync_package('collectd')

    # install librate plugin
    sync_package('make')
    with cd('/tmp'):
        sudo('git clone git://github.com/librato/collectd-librato.git')

        with cd('collectd-librato'):
            sudo('make install')

        sudo('rm -rf ./collectd-librato')

    sync_template_file('./collectd/collectd.conf', '/etc/collectd/collectd.conf', owner='root', mode='644')

    sudo('service collectd restart')

    print colors.green(u'collectd synced')
