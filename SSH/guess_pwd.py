# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import paramiko

host = "192.168.14.100"
usr = "aaqqxx"
pwd = "abc123"


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=usr, password=pwd)
    cmd = "ls"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for each in stdout.readlines():
        print each,
    pass


if __name__ == "__main__":
    main()
