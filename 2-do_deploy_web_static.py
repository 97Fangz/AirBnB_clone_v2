#!/usr/bin/python3
""" Fabric script that distribute an archive to web servers
"""
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['35.175.135.195', '54.164.1.118']
env.user = 'ubuntu'


def do_pack():
    try:
        if not path.exists("versions"):
            local('mkdir versions')
        now = datetime.utcnow()
        ft = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(ft)
        local("tar -cvzf {}  web_static/".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    if not path.exists(archive_path):
        return False
    try:
        tgz_file = archive_path.split('/')[-1]
        fname = tgz_file.split('.')[0]

        put(archive_path, '/tmp/')

        releases_path = "/data/web_static/releases/{}/".format(fname)
        run("mkdir -p {}".format(releases_path))

        run("tar -xzf /tmp/{} -C {}".format(tgz_file, releases_path))
        run("rm /tmp/{}".format(tgz_file))

        run("mv {}/web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))

        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))

        run('sudo service nginx restart')

        print("New version deployed!")
        return True
    except Exception as e:
        return False
