# coding: utf-8
from contextlib import contextmanager

from fabric.api import run, cd, prefix, sudo
from fabric import context_managers

def is_path_exists(path, use_sudo=False):
    with context_managers.settings(context_managers.hide('warnings', 'running'), warn_only=True):
        if use_sudo:
            is_path_exists = sudo('ls "%(path)s"' % {'path': path})
        else:
            is_path_exists = run('ls "%(path)s"' % {'path': path})

    return is_path_exists.return_code != 2


@contextmanager
def close_to_503():

    with cd('/home/the-tale'):
        run('cp ./conf/503.html ./dcont/503.html')

    yield

    with cd('/home/the-tale'):
        run('rm -f ./dcont/503.html')


@contextmanager
def stop_workers():

    if not is_path_exists('/home/the-tale/project'):
        print 'skeep "stop workers" action since projects does not exists'
        yield
        return

    with cd('/home/the-tale/project'):
        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py game_stop')
        run('./scripts/workers.sh stop')

    yield

    with cd('/home/the-tale/project'):
        run('nohup ./scripts/workers.sh start 2>&1 1>/dev/null </dev/null')
