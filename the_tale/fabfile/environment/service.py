# coding: utf-8

class Service(object):

    PACKAGES = []

    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self._users = {}

    @property
    def required_packages(self): return set(self.PACKAGES)

    def setup(self): raise NotImplementedError

    def merge(self, service):
        if self.type != service.type:
            raise Exception('merge services with non equal types: "%s" and "%s"' % (self.type, service.type))
