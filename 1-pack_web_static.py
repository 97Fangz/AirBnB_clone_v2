#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive from the contents of the web_static folder in the AirBnB repository """

from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """
    Generates a gzipped tar archive from the contents of the web_static folder.

    Returns:
        Archive path if the archive has been correctly generated, otherwise None.
    """
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        now = datetime.now()
        ft = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(ft)
        local("tar -czvf {} web_static/".format(archive_path))

        # Check if the archive has all the files from web_static
        with local('tar -tf {} | grep web_static'.format(archive_path), capture=True) as output:
            if len(output.stdout.strip()) == 0:
                return None

        return archive_path

    except Exception:
        return None
