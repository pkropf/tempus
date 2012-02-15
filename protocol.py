# -*- coding: utf-8 -*-
# -*- test-case-name: twisted.test.test_nmea -*-

"""RFID Card Reader
"""


import operator
from twisted.protocols import basic
from twisted.python.compat import reduce
from twisted.python import log


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
