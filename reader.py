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
    baudrate = 9600

    class reader(CardReceiver):
        def handle_rfid(self, *args):
            log.msg('rfid: %s' % args[0])

    port = '/dev/tty.usbserial-A900UCVB'
    log.msg('Attempting to open %s at %dbps' % (port, baudrate))
    s = SerialPort(reader(), port, reactor, baudrate=baudrate)
    reactor.run()
