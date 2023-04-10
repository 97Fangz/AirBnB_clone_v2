 #!/usr/bin/python3
"""
Fabfile to delete out-of-date archives.

This script deletes out-of-date archives from the web servers. The number of archives
to keep is determined by the `number` argument passed to the `do_clean` function.
"""

import os
from fabric.api import *

# Set the IP addresses of the web servers
env.hosts = ['54.237.52.200', '34.224.62.212']

def do_clean(number=0):
    """Delete out-of-date archives.

    Params:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If number is 2, keeps
    the most and second-most recent archives, etc.
    """

    # Ensure that number is an integer
    number = int(number)

    # If number is 0 or 1, set it to 1
    number = 1 if number < 2 else number

    # Get a list of all archives and sort them by name
    archives = sorted(os.listdir("versions"))

    # Remove the `number` most recent archives
    [archives.pop() for i in range(number)]

    # Delete the archives from the local `versions` folder
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Delete the archives from the remote servers
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]

