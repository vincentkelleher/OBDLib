import unittest
from mock import MagicMock
from ..odbutils import ODBUtils
import serial


class TestODBUtils(unittest.TestCase):
    serial_device_name = "TEST_DEVICE"
    baudrate = 38400

    def setUp(self):
        self.odb_utils = ODBUtils(self.serial_device_name, self.baudrate)

        self.serial_mock = serial.Serial()
        self.serial_mock.open = MagicMock()
        self.serial_mock.write = MagicMock()

        self.odb_utils.set_serial_device(self.serial_mock)

        self.odb_utils.connect()
        self.serial_mock.open.assert_called()

    def test_send(self):
        self.serial_mock.readline = MagicMock(return_value="ok")

        self.assertEquals("ok", self.odb_utils.send("test"))

        self.serial_mock.write.assert_called_with("test")

    def test_engine_rpm(self):
        self.serial_mock.readline = MagicMock(return_value="41 0C 1A F8")
        self.odb_utils.send = MagicMock(return_value=self.serial_mock.readline())

        self.assertEquals(6904, self.odb_utils.engine_rpm())

        self.odb_utils.send.assert_called_with("01 0C\r")

if __name__ == '__main__':
    unittest.main()

