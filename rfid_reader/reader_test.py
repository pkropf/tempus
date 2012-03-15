from nose.tools import raises, assert_raises
from reader import Holder, InvalidChecksum, InvalidSentence, CardReceiver
import json


class Holder_Test():
    def setup(self):
        pass

    def json_field_test(self):
        holder = Holder()
        h = holder.json()
        j = json.loads(h)

        assert 'rfid' in j
        assert 'rfid_stamp' in j
        assert 'port' in j
        assert 'baudrate' in j
        assert 'connection_stamp' in j
        assert 'connection_status' in j
        assert 'connection_time' in j

    def rfid_test(self):
        holder = Holder()
        stamp = holder.rfid_stamp
        holder.set_rfid('12345')
        assert holder.rfid_stamp != stamp


class CardReceiver_Test():
    def setup(self):
        pass

    def card_good_rfid_test(self):
        cr = CardReceiver()
        cr.handle_rfid = lambda x: 0
        cr.lineReceived('\x020100E2850E68')

    @raises(InvalidSentence)
    def card_invalid_rfid_test(self):
        cr = CardReceiver()
        cr.lineReceived('xyzzy')

    @raises(InvalidChecksum)
    def card_invalid_checksum_test(self):
        cr = CardReceiver()
        cr.handle_rfid = lambda x: 0
        cr.lineReceived('\x020100E2850E67')
