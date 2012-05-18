# coding: utf-8
import os
import tempfile

from fabric.api import sudo, put
from fabric import colors


from fabfile.utils import is_path_exists

TEMPLATES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')


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


def sync_file(source, destination, owner, mode, context=None, group=None, from_templates=True):

    if from_templates:
        source = os.path.join(TEMPLATES_DIR, source)

    put(source, destination, use_sudo=True)

    sync_fs_data(destination, owner, mode, group)

    print colors.green(u'file "%(destination)s" has been synced' % {'destination': destination})


def sync_template_file(source, destination, owner, mode, context=None, group=None):

    tmp_file = tempfile.TemporaryFile()

    from jinja2 import Environment, FileSystemLoader
    jenv = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    text = jenv.get_template(source).render(**context or {})

    tmp_file.write(text.encode('utf-8'))

    sync_file(tmp_file, destination, owner, mode, from_templates=False)

    tmp_file.close()

    print colors.green(u'template file "%(destination)s" has been synced' % {'destination': destination})
