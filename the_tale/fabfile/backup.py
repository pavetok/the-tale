# coding: utf-8

from fabric.api import task, run, cd, prefix

from fabfile.utils import close_to_503, stop_workers, is_path_exists


@task
def backup():

    if not is_path_exists('/home/the-tale/project'):
        print 'skeep backup actions since projects does not exists'
        return

    with close_to_503(), stop_workers():
        backup_project()


def backup_project():

    if not is_path_exists('/home/the-tale/project'):
        print 'skeep backup actions since projects does not exists'
        return

    with cd('/home/the-tale/project'):

        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py portal_dump')
