#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Peter Kropf. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from twisted.web import server, resource
from twisted.python import log
import sys
from datetime import datetime
import json
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
import operator
from twisted.protocols import basic
from twisted.python.compat import reduce


class Holder():
    def __init__(self):
        self.rfid = ''
        self.rfid_stamp = None
        self.port = None
        self.bauderate = None
        self.connection_stamp = None
        self.connection_status = 'unknown'

    def set_rfid(self, rfid):
        self.rfid = rfid
        self.rfid_stamp = datetime.now()
        log.msg('rfid: %s @ %s' % (self.rfid, str(self.rfid_stamp)))

    def json(self):
        return json.dumps({'rfid': self.rfid,
                           'rfid_stamp': str(self.rfid_stamp),
                           'port': self.port,
                           'baudrate': str(self.baudrate),
                           'connection_stamp': str(self.connection_stamp),
                           'connection_status': self.connection_status,
                           'connection_time': str(datetime.now() - self.connection_stamp),
                           })


class RfidJson(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.defaultContentType = 'application/json'
        return self.holder.json()


class InvalidChecksum(Exception):
    pass


class CardReceiver(basic.LineReceiver):
    """This parses ascii strings read from an rfid tag serial reader at 9,600 bps

    From http://www.sparkfun.com/datasheets/Sensors/ID-12-Datasheet.pdf

    Output Data Structure – ASCII
    STX (02h) DATA (10 ASCII) CHECK SUM (2 ASCII) CR LF ETX (03h) 
    [The 1byte (2 ASCII characters) Check sum is the “Exclusive OR” of the 5 hex bytes (10 ASCII) Data characters.]

    For a read of

    0100E2850E68<cr><lf>

    int('68', 16) == reduce(operator.xor, [int(x, 16) for x in '01', '00', 'E2', '85', '0E'])
    """

    delimiter = '\r\n\03'

    def lineReceived(self, line):
        if not line.startswith('\02'):
            raise InvalidSentence("%r does not begin with \\02" % (line,))

        rfid, checksum = line[1:-2], line[-2:]

        checksum, calculated_checksum = int(checksum, 16), reduce(operator.xor, [int(rfid[x:x+2], 16) for x in range(0,len(rfid), 2)])
        if checksum != calculated_checksum:
            raise InvalidChecksum("Given 0x%02X != 0x%02X" % (checksum, calculated_checksum))

        return self.handle_rfid(rfid)


class Reader(CardReceiver):
    def handle_rfid(self, *args):
        self.holder.set_rfid(args[0])
        self.holder.factory.broadcast(self.holder.json())


    def connectionMade(self):
        self.holder.port = self.port
        self.holder.baudrate = self.baudrate
        self.holder.connection_stamp = datetime.now()
        self.holder.connection_status = 'connected'
        log.msg("Connected...")


    def connectionLost(self, reason):
        self.holder.connection_status = 'disconnected'
        log.msg("Lost connection (%s)" % reason)
        log.msg("Reconnecting in %d seconds..." % self.reconnect_rate)
        self.retry = reactor.callLater(self.reconnect_rate, self.reconnect)


    def reconnect(self):
        try:
            SerialPort(self, self.port, self.reactor, baudrate=self.baudrate)

        except:
            log.msg("Error opening serial port %s (%s)" % (self.port, sys.exc_info()[1]))
            log.msg("Reconnecting in %d seconds..." % self.reconnect_rate)
            self.retry = reactor.callLater(self.reconnect_rate, self.reconnect)


class BroadcastRfidProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        if not binary:
            self.factory.broadcast("%s" % msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastRfidFactory(WebSocketServerFactory):

    protocol = BroadcastRfidProtocol

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.tickcount = 0

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            self.clients.remove(client)

    def broadcast(self, msg):
        print "broadcasting message '%s' .." % msg
        for c in self.clients:
            print "send to " + c.peerstr
            c.sendMessage(msg)


if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.internet.serialport import SerialPort
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('reader.cfg')

    logname = config.get('general', 'logname', None)
    if logname:
        logFile = open(logname, 'a')

    else:
        logFile = sys.stdout

    log.startLogging(logFile)

    holder = Holder()

    resource = RfidJson()
    resource.holder = holder

    top = server.Site(resource)
    http_port = config.getint('http', 'port')
    reactor.listenTCP(http_port, top)

    r = Reader()
    r.reactor = reactor
    r.port = config.get('serial', 'port')
    r.baudrate = config.getint('serial', 'baudrate')
    r.reconnect_rate = config.getint('serial', 'reconnect_rate')
    r.holder = holder

    log.msg('Attempting to open %s at %dbps' % (r.port, r.baudrate))
    s = SerialPort(r, r.port, r.reactor, baudrate=r.baudrate)

    factory = BroadcastRfidFactory("ws://localhost:9000")
    holder.factory = factory
    listenWS(factory)

    reactor.run()
