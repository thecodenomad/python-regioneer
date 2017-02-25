# coding: utf-8
"""
    core.utils.networking
    ~~~~~~~~~~~~~

    The purpose of this module is to contain any networking related utilities or helper functions for use throughout
    the project.

    :copyright: 2016 Ray Gomez (codenomad@gmail.com), see AUTHORS for more details
    :license: Apache 2.0, see LICENSE for more details
"""

from socket import socket

def ping_check(host, port=None):
    """ Check to see if the given host is pingable. If a port is specified, instead of an ICMP request,
    a socket connection will be attempted.

    :param host: host that should be ping checked
    :param port: (Optional) port to ping against.
    :return: True or False
    """

    import subprocess, platform

    ping_str = "ping -n 1"
    use_shell = False
    conn = False

    if platform.system().lower() != "windows":
        ping_str = "ping -c 1"
        use_shell = True

    if not port:
        cmd = "{ping_cmd} {host}".format(ping_cmd=ping_str, host=host)
        return subprocess.call(cmd, shell=use_shell) == 0
    else:

        if not isinstance(port, int):
            print("Port: '{}' isn't an integer, failing...".format(port))
            raise TypeError("Integer required")

        print("Port has been specified, using socket to test for availability")
        host = (host,port,)

        try:
            conn = socket()
            conn.connect(host)
            return True
        except Exception as e:
            print("Connection failed: {}".format(e))
            return False
        finally:
            if conn:
                conn.close()

