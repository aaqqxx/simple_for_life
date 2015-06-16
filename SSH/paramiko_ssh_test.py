# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import paramiko

host = "192.168.14.100"
usr = "aaqqxx"
pwd = "abc123"


def get_file_from_ssh(ip="192.168.14.100", port=22, username="aaqqxx", pwd="abc123",
                      remote_path="/var/ftp/gather/gatherFile.txt", local_path="/home/aaqqxx/gatherFile.txt"):
    target = paramiko.Transport((ip, port))
    target.connect(username=username, password=pwd)
    sftp = paramiko.SFTPClient.from_transport(target)
    # remote_path = "/tmp/test.txt"
    # local_path = "/tmp/text.txt"
    # local_path = r"f:/text.txt"
    sftp.get(remote_path, local_path)
    target.close()


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
    # main()
    get_file_from_ssh()
