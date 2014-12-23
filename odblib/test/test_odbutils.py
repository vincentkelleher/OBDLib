import unittest
from mock import MagicMock
from ..ODBUtils import ODBUtils
import serial


class TestODBUtils(unittest.TestCase):
    serial_device_name = "TEST_DEVICE"
    baudrate = 38400

    def setUp(self):
        self.odb_utils = ODBUtils(self.serial_device_name, self.baudrate)

        self.serial_device_mock = serial.Serial()
        self.serial_device_mock.open = MagicMock()
        self.serial_device_mock.write = MagicMock()

        self.odb_utils.serial_device = self.serial_device_mock

        self.odb_utils.connect()
        self.serial_device_mock.open.assert_called_once_with()

    def test_send(self):
        self.serial_device_mock.readline = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals("41 0C 1A F8".split(" "), self.odb_utils.send("01", "0C"))

        self.serial_device_mock.write.assert_called_once_with("01 0C\r")
        self.serial_device_mock.readline.assert_called_once_with()

    def test_engine_rpm(self):
        self.serial_device_mock.readline = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals(6904, self.odb_utils.engine_rpm())

        self.serial_device_mock.write.assert_called_once_with("01 0C\r")
        self.serial_device_mock.readline.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

