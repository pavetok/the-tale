# coding: utf-8
from contextlib import contextmanager

from fabric.api import run, cd, prefix

@contextmanager
def close_to_503():

    with cd('/home/the-tale'):
        run('cp ./conf/503.html ./dcont/503.html')

    yield
        
    with cd('/home/the-tale'):
        run('rm -f ./dcont/503.html')


@contextmanager
def stop_workers():

    with cd('/home/the-tale/project'):
        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py game_stop')
        run('./scripts/workers.sh stop')

    yield
        
    with cd('/home/the-tale/project'):
        run('nohup ./scripts/workers.sh start 2>&1 1>/dev/null </dev/null')

