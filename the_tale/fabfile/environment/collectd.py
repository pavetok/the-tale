# coding: utf-8
from fabric.api import sudo, cd

from .logic import sync_template_file

from .service import Service


class Collectd(Service):

    PACKAGES = ('collectd', )

    def __init__(self, connect_to_librato=False):
        super(Collectd, self).__init__()
        self.connect_to_librato = connect_to_librato

    @property
    def required_packages(self):
        packages = super(Collectd, self).required_packages
        if self.connect_to_librato:
            packages |= set(['make', 'git'])
        return packages

    def setup(self):

        with cd('/tmp'):
            sudo('git clone git://github.com/librato/collectd-librato.git')

            with cd('collectd-librato'):
                sudo('make install')

            sudo('rm -rf ./collectd-librato')

        sync_template_file('./collectd/collectd.conf', '/etc/collectd/collectd.conf', owner='root', mode='644')

        sudo('service collectd restart')
