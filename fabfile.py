#!/usr/bin/python
# _*_ codeing:utf-8 _*_

import os,re
from datetime import datetime

from fabric.api import *

env.user='yang'
env.password='yang123456'
env.sudo_user='root'
env.sudo_password='yang123456'
env.hosts=['192.168.1.11']

db_user='root'
db_password='yang123456'

_TAR_FILE = 'dist-awesome.tar.gz'

def _current_path():
    return os.path.abspath('.')

def build():
    '''
    Build dist package.
    '''
    includes = ['static', 'templates', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(_current_path(), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/home/yang/workspace/python/awesome'

def deploy():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    print(newdir)
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)

    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR,newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -r www')
        sudo('ln -s %s www' % newdir)
        sudo('chown yang:yang www')
        sudo('chown -R yang:yang %s' % newdir)


