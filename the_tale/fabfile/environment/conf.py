# coding: utf-8

from .host import Host
from .project import Project
from .user import User
from .ssh import SSH
from .apache import Apache
from .postgres import Postgres
from .rabbitmq import RabbitMQ
from .postfix import Postfix
from .collectd import Collectd
from .python import Python


project_the_tale =  Project('the-tale',
                            users=(User('the-tale', ssh=SSH(keys=('id_rsa',), authorized_keys=True)),),
                            packages=('git', 'psmisc'),
                            services=(Apache('the-tale', modes=('rewrite',)),
                                      Postgres('the-tale'),
                                      RabbitMQ('the-tale'),
                                      Postfix(),
                                      Collectd(connect_to_librato=True),
                                      Python('the-tale',
                                             packages=('kombu', 'psycopg2', 'south', 'postmarkup', 'markdown', 'pymorphy', 'xlrd', 'mock'))))


HOST = Host('vps',
            packages=('emacs', ),
            projects=(project_the_tale,),
    )
