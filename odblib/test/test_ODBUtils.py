from __future__ import absolute_import

import unittest
from bluetooth import BluetoothSocket, RFCOMM
from mock import MagicMock
from ..ODBUtils import ODBUtils, DATA_SIZE


class TestODBUtils(unittest.TestCase):
    bluetooth_device_name = "TEST_DEVICE"
    port = 1

    def setUp(self):
        self.odb_utils = ODBUtils(self.bluetooth_device_name, self.port)

        self.bluetooth_device_mock = BluetoothSocket(RFCOMM)
        self.bluetooth_device_mock.connect = MagicMock()
        self.bluetooth_device_mock.send = MagicMock()

        self.odb_utils.bluetooth_device = self.bluetooth_device_mock

        self.odb_utils.connect()
        self.bluetooth_device_mock.connect.assert_called_once_with((self.bluetooth_device_name, self.port))

    def test_send(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals("41 0C 1A F8".split(" "), self.odb_utils.send("01", "0C"))

        self.bluetooth_device_mock.send.assert_called_once_with("01 0C\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

    def test_engine_rpm(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals(1726, self.odb_utils.engine_rpm())

        self.bluetooth_device_mock.send.assert_called_once_with("01 0C\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

if __name__ == '__main__':
    unittest.main()

