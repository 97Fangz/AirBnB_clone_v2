#!/usr/bin/python3
"""
Fabric script that distributes an archive to a web server
"""
import os.path
from fabric.api import env, put, run

env.hosts = ['54.237.52.200', '34.224.62.212']


def do_deploy(archive_path):
    """
    Distributes an archive to a web server
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]

    try:
        put(archive_path, '/tmp/')
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(name))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(file_name, name))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(name, name))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(name))
        return True
    except Exception:
        return False
