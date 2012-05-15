# coding: utf-8

from fabric.api import task, run, cd, prefix
from fabric import context_managers

from fabfile.utils import close_to_503, stop_workers
from fabfile.backup import backup_project

from meta_config import meta_config

@task
def update():

    with close_to_503(), stop_workers():
        backup_project()
        update_project()

    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        run('killall apache2')


def update_project():

    with prefix('. /home/the-tale/env/bin/activate'):
        run('pip install --upgrade "git+git://github.com/Tiendil/dext.git#egg=Dext"')
        run('pip install -r https://raw.github.com/Tiendil/dext/master/requirements.txt')

        run('pip install --upgrade git+git://github.com/Tiendil/pynames.git#egg=Pynames')
        run('pip install --upgrade git+ssh://git@github.com/Tiendil/the-tale.git#egg=TheTale')

    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/the_tale /home/the-tale/project')
    run('ln -s /home/the-tale/conf/settings_local.py  /home/the-tale/project/settings_local.py')
    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/django/contrib/admin/static/admin/ /home/the-tale/project/static/admin')
    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/the_tale/static /home/the-tale/static/%s' % meta_config.static_data_version)

    with cd('/home/the-tale/project'):

        run('chmod +x ./manage.py')

        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py syncdb')
            run('./manage.py migrate')
            run('./manage.py portal_postupdate_operations')
