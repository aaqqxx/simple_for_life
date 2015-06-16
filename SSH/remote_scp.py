__author__ = 'XingHua'

import os
import paramiko


def remote_scp(host_ip, remote_path, local_path, username, password):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)  # 登录远程服务器
    sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
    src = remote_path
    des = local_path
    sftp.get(src, des)
    t.close()


def main():
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect('192.168.1.13', username='root', password='xxxxxx')
    sftp = ssh.open_sftp()
    remote_file = sftp.file('~/www', 'wb')
    remote_file.set_pipelined(True)
    remote_file.write('wwwwwwwwwwwwwwwwwwwwwwww')
    sftp.close()
    ssh.close()


if __name__ == '__main__':
    main()
