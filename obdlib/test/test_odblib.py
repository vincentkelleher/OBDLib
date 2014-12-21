import unittest
from ..odblib import ODBLib
from mock import patch


class TestODBLib(unittest.TestCase):
    serial_device_name = "TEST_DEVICE"
    baudrate = 38400

    @patch("serial.Serial")
    @patch.object(ODBLib, "connect")
    def setUp(self, serial_mock, odblib_mock):
        self.odbLib = ODBLib(self.serial_device_name, self.baudrate)

        odblib_mock.return_value = serial_mock()
        self.odbLib.connect()

    def test_engine_rpm(self):
        pass

if __name__ == '__main__':
    unittest.main()

