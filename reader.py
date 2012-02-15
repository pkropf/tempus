#! /usr/bin/env python


from twisted.python import log
import sys


if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.internet.serialport import SerialPort

    #logFile = 'reader.log'
    logFile = None
    if logFile is None:
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
    r.port = '/dev/tty.usbserial-A900UCVB'
    r.reactor = reactor
    r.baudrate = 9600
    r.reconnect_rate = 1

    log.msg('Attempting to open %s at %dbps' % (r.port, r.baudrate))
    s = SerialPort(r, r.port, r.reactor, baudrate=r.baudrate)
    reactor.run()
