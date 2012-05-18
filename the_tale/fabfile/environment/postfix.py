# coding: utf-8

from .logic import sync_template_file

from .service import Service


class Postfix(Service):

    PACKAGES = (('postfix', 'export DEBIAN_FRONTEND=noninteractive'), )

    def __init__(self):
        super(Postfix, self).__init__()

    def setup(self):
        sync_template_file('./postfix/main.cf', '/etc/postfix/main.cf', owner='root', mode='644')
