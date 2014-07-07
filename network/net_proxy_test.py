# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'

"""
具备简单的管理功能，运行后 telnet localhost 9000 端口可以进行管理主要功能就是做包转发，
如果有一个桥服务器，可以用来外网访问内网用，还是很管用的
"""

import socket,select,sys,time
import thread

s_list = []

def loop(cs,addr,s_ip,s_port):
    print '%s %d connected.' % addr
    ts = socket.socket()

    try:
        ts.connect((s_ip,s_port))
    except:
        cs.close()
        print '%s %d closed.' % addr
        sys.exit(0)

    while True:

        rl,wl,xl = select.select([cs.fileno(),ts.fileno()],[],[cs.fileno(),ts.fileno()])

        if len(xl) > 0:
            cs.close()
            ts.close()
            print '%s %d closed.' % addr
            sys.exit(0)

        if len(rl) > 0:
            if rl[0] == cs.fileno():
                rs = ts
                ws = cs
            else:
                rs = cs
                ws = ts

            try:
                buffer = ws.recv(10000)
                if len(buffer) == 0:
                    raise
                rs.send(buffer)
            except:
                rs.close()
                ts.close()
                print '%s %d closed.' % addr
                sys.exit(0)

def mainserver(l_port,s_ip,s_port):
    global s_list
    try:
        ss = socket.socket()
        ss.bind(('0.0.0.0',l_port))
        ss.listen(10)
        s_list.append((l_port,s_ip,s_port))
    except:
        sys.exit(0)

    while True:
        cs,addr = ss.accept()

        thread.start_new_thread(loop,(cs,addr,s_ip,s_port))

def manager(l_port):
    global start,s_list

    ss = socket.socket()
    ss.bind(('0.0.0.0',l_port))
    ss.listen(10)

    while True:
        cs,addr = ss.accept()
        cs.send("""trans server 1.0\r\ntype 'help' to get help\r\n""")
        buffer = ''
        while True:
            buf = cs.recv(10000)
            if len(buf) == 0:
                cs.close()
                break
            if buf[-1] not in ('\r','\n'):
                buffer += buf
                continue
            buffer += buf
            cmd = buffer.strip()
            buffer = ''
            if cmd == 'exit':
                cs.close()
                break
            elif cmd == 'stop':
                start = 0
                cs.close()
                sys.exit(0)
            elif cmd == 'list':
                b = ''
                for l in s_list:
                    b += '%4d %s:%d\r\n' % l

                if len(b) > 0:
                    cs.send(b)
            elif cmd in ('help','?'):
                cs.send("""-------------------------------------------\r
exit\r
    exit telnet\r
start localport serverip:serverport\r
    start a new server\r
list\r
    list all server\r
-------------------------------------------\r
""")
            else:
                cmds = cmd.split(" ",1)
                if len(cmds) > 1 and cmds[0] == 'start':
                    args = cmds[1].strip().split(" ",1)
                    if len(args) != 2:
                        cs.send('start localport serverip:serverport\r\n')
                        continue
                    arg = args[1].split(":",1)
                    if len(arg) != 2:
                        cs.send('start localport serverip:serverport\r\n')
                        continue

                    try:
                        l_port = int(args[0])
                        s_ip = arg[0]
                        s_port = int(arg[1])
                    except:
                        cs.send('start localport serverip:serverport\r\n')
                        continue

                    thread.start_new_thread(mainserver,(l_port,s_ip,s_port))
                    cs.send('start OK!\r\n')
                else:
                    cs.send('no command [%s]\r\n' % cmd)
                    continue

def main():
    global start

    if len(sys.argv) == 3:
        try:
            l_port = int(sys.argv[1])
            s_ip,s_port = sys.argv[2].split(":")
            s_port = int(s_port)
            thread.start_new_thread(mainserver,(l_port,s_ip,s_port))
        except:
            pass

    start = 1

    thread.start_new_thread(manager,(9000,))

    while start:
        time.sleep(1)

if __name__ == '__main__':

    start = 0

    main()

