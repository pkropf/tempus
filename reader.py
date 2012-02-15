#! /usr/bin/env python


from twisted.web import server, resource
from twisted.python import log
from protocol import CardReceiver
import sys
from datetime import datetime
import json


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


class Reader(CardReceiver):
    def handle_rfid(self, *args):
        self.holder.set_rfid(args[0])


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
    reactor.listenTCP(8080, top)

    r = Reader()
    r.reactor = reactor
    r.port = config.get('general', 'port')
    r.baudrate = config.getint('general', 'baudrate')
    r.reconnect_rate = config.getint('general', 'reconnect_rate')
    r.holder = holder

    log.msg('Attempting to open %s at %dbps' % (r.port, r.baudrate))
    s = SerialPort(r, r.port, r.reactor, baudrate=r.baudrate)

    reactor.run()
