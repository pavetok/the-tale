# coding: utf-8

from fabric.api import task, run, cd, prefix

from fabfile.utils import close_to_503, stop_workers


@task
def backup():

    with close_to_503(), stop_workers():
        backup_project()


def backup_project():
    with cd('/home/the-tale/project'):

        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py portal_dump')

