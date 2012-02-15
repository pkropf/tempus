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
