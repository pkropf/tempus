#! /usr/bin/env python


from twisted.python import log
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('reader.cfg')


if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.internet.serialport import SerialPort

    logname = config.get('general', 'logname', None)
    if logname:
        logFile = open(logname, 'a')

    else:
        logFile = sys.stdout

    log.startLogging(logFile)

    from protocol import CardReceiver

    class reader(CardReceiver):
        def handle_rfid(self, *args):
            log.msg('rfid: %s' % args[0])


        def connectionMade(self):
            log.msg("Connected...")


        def connectionLost(self, reason):
            log.msg("Lost connection (%s)" % reason)
            log.msg("Reconnecting in %d seconds..." % self.reconnect_rate)
            self.retry = reactor.callLater(self.reconnect_rate, self.reconnect)


        def reconnect(self):
            try:
                SerialPort(self, self.port, self.reactor, baudrate=self.baudrate)
                log.msg("RECONNECTED")

            except:
                log.msg("Error opening serial port %s (%s)" % (self.port, sys.exc_info()[1]))
                log.msg("Reconnecting in %d seconds..." % self.reconnect_rate)
                self.retry = reactor.callLater(self.reconnect_rate, self.reconnect)

    r = reader()
    r.reactor = reactor
    r.port = config.get('general', 'port')
    r.baudrate = config.getint('general', 'baudrate')
    r.reconnect_rate = config.getint('general', 'reconnect_rate')

    log.msg('Attempting to open %s at %dbps' % (r.port, r.baudrate))
    s = SerialPort(r, r.port, r.reactor, baudrate=r.baudrate)
    reactor.run()
