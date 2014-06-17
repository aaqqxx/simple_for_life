# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

from twisted.internet.protocol import ClientCreator, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys

class Sender(Protocol):
    def sendCommand(self, command):
        print "invio", command
        self.transport.write(command)

    def dataReceived(self, data):
        print "DATA", data

PORT = 1234
HOST = 'localhost'

def sendCommand(command):
    def test(d):
        print "Invio ->", command
        d.sendCommand(command)
    c = ClientCreator(reactor, Sender)
    c.connectTCP(HOST, PORT).addCallback(test)

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['stop', 'next_call', 'force']:
        sys.stderr.write('Usage: %s: {stop|next_call|force}\n' % sys.argv[0])
        sys.exit(1)
    sendCommand(sys.argv[1]+'\n')
    reactor.run()