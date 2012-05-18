# coding: utf-8


class SSH(object):

    def __init__(self, keys=(), authorized_keys=False):
        self.keys = set(keys)
        self.authorized_keys = authorized_keys


    def merge(self, ssh):
        self.keys += ssh.keys
        self.authorized_keys = self.authorized_keys or ssh.authorized_keys
