# -*- coding: UTF-8 -*-
import os
from contextlib import contextmanager as __ctxmgr

from fabric.api import *
from fabric.decorators import runs_once

import fabsettings as cfg

#host settings
env.hosts = ['vicalloy@jstwind.com']
env.password = cfg.PASSWORD
#env.passwords = fabsettings.PASSWORDS

#custom settings
env.deploy_dir = '/home/vicalloy/webapps/jstwind/timeline-site'
env.activate = 'source %s' % os.path.join(env.deploy_dir, 'env/bin/activate')
env.mg = 'python %s' % os.path.join(env.deploy_dir, 'sites', 'manage.py ')

@__ctxmgr
def __virtualenv():
    with cd(env.deploy_dir):
        with prefix(env.activate):
            yield


def reload():
    wsgi = os.path.join(env.deploy_dir, 'deploy', 'dj_scaffold.wsgi')
    run("touch %s" % wsgi)


def update():
    with __virtualenv():
        run("git pull")
        run('%s syncdb' % env.mg)
        run('%s migrate' % env.mg)
        run('%s compress --force' % env.mg)
        reload()
