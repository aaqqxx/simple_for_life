#coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
from tkinter import *

import os, sys
from threading import Thread
from queue import Queue, Empty

import _thread
import time

from paramiko import SSHClient, Transport, AutoAddPolicy, WarningPolicy
import getpass


def start(client):
    try:
        client.connect(hostname='127.0.0.1', port=22, username='root', password=pw)
        return True
    except Exception as e:
        client.close()
        print(e)
        return False


def check(client, outqueue, inqueue):
    chan = client.get_transport().open_session()
    cmd = inqueue.get()
    #print(cmd)
    chan.exec_command(cmd)
    while True:
        if chan.recv_ready():
            data = chan.recv(4096).decode('ascii')
            outqueue.put("recv:\n%s" % data)
        #print("recv:\n%s" %data )
        #text.insert(END, "recv:\n%s" % chan.recv(4096).decode('ascii'))
        if chan.recv_stderr_ready():
            error = chan.recv_stderr(4096).decode('ascii')
            outqueue.put("error:\n%s" % error)
        #print("error:\n%s" %error)
        #text.insert(END, "error:\n%s" % chan.recv_stderr(4096).decode('ascii'))
        if chan.exit_status_ready():
            exitcode = chan.recv_exit_status()
            outqueue.put("exit status: %s" % exitcode)
            #print("exit status: %s" %exitcode)
            #text.insert(END, "exit status: %s" % chan.recv_exit_status())
            #key = False
            time.sleep(0.01)
            client.close()
            break


def reader(outqueue):
    while True:
        while outqueue.qsize():
            try:
                data = outqueue.get()
                if data:
                    print(data)
            except Excetpiton as e:
                print(e)
            #print(time.ctime())
            #time.sleep(0.5)


def sender(outqueue, inqueue):
    while True:
        while outqueue.empty():
            #cmd = input("Command to run: ")
            outqueue.put("Command to run: ")
            cmd = input()
            if cmd == "exit":
                client.close()
                #print(cmd)
                break
            #print("running '%s'" % cmd)
            outqueue.put("running '%s'" % cmd)
            inqueue.put(cmd)


if __name__ == '__main__':
    pw = getpass.getpass()

    client = SSHClient()
    #client.set_missing_host_key_policy(WarningPolicy())
    client.set_missing_host_key_policy(AutoAddPolicy())

    if not start(client):
        #os._exit(0)
        sys.exit(0)

    outqueue = Queue()
    inqueue = Queue()
    #check(client)
    #_thread.start_new_thread(check,(client,))
    #time.sleep(100)


    s = Thread(target=sender, args=(outqueue, inqueue, ))
    s.daemon = True
    s.start()
    #s.join()

    r = Thread(target=reader, args=(outqueue,))
    r.daemon = True
    r.start()
    #r.join()

    t = Thread(target=check, args=(client, outqueue, inqueue, ))
    #t.daemon = True
    t.start()
    t.join()

    #r.join()
    #client.close()