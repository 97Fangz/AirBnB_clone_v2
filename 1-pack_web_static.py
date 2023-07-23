#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents of the
web_static folder in the AirBnB repository"""
from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Generates a tgz archive"""
    try:
        if not isdir("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_filename = 'web_static_{}.tgz'.format(t.strftime(f))
        archive_path = 'versions/{}'.format(archive_filename)
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        print("An exception occurred: {}".format(e))
        return None
