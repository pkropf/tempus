Tempus
======

Tempus is a time tracking system using an rfid cardreader to allow
people to clock in and out. The time stamps can be associated with
different projects, there will be some reporting, possible graphs, and
most likely other things.

Currently working is a simple Twisted_ Python_ application that will
read an rfid tag via a Innovations ID-12 (or such) card reader. The
rfid value is made available through a websocket as a json structure.

.. _Python: http://python.org
.. _Twisted: http://twistedmatrix.com

The rfid reader is an Innovations ID-12 available from SparkFun_.

.. _SparkFun: http://www.sparkfun.com/products/9875

Drivers for the rfid reader can be found on the FTDI_ website.

.. _FTDI: http://www.ftdichip.com/Drivers/VCP.htm
