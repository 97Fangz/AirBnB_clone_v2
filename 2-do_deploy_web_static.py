#!/usr/bin/python3
""" Function that compress a folder """
from datetime import datetime
from fabric.api import *
import os

env.hosts = ['35.175.135.195', '54.164.1.118']
env.user = "ubuntu"

def do_deploy(archive_path):
    """ Deploys """
    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.split('/')[-1]
        wname = name.split('.')[0]

        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        
        # Use "mv -f" to force the move and overwrite existing files
        run("mv -f {}/web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}/web_static".format(releases_path))
        run("rm -rf /data/web_static/current")

        symlink_cmd = "ln -s {} /data/web_static/current".format(releases_path)
        print("Creating symlink with command: {}".format(symlink_cmd))
        run(symlink_cmd)

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment error: {}".format(e))
        return False

