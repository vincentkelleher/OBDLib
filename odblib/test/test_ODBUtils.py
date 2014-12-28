from __future__ import absolute_import

import unittest
import bluetooth
from mock import MagicMock, patch
from ..ODBUtils import ODBUtils, DATA_SIZE


class TestODBUtils(unittest.TestCase):
    available_devices = [
        ("TEST_DEVICE_ADDRESS", "TEST_DEVICE"),
        ("TEST_DEVICE_2_ADDRESS", "TEST_DEVICE_2"),
    ]
    bluetooth_device_name = "TEST_DEVICE"
    port = 1

    def setUp(self):
        self.odb_utils = ODBUtils(self.bluetooth_device_name, self.port)

        self.bluetooth_device_mock = MagicMock()
        self.bluetooth_device_mock.connect = MagicMock()
        self.bluetooth_device_mock.send = MagicMock()

        self.odb_utils.bluetooth_device = self.bluetooth_device_mock

        self.odb_utils.connect()
        self.bluetooth_device_mock.connect.assert_called_once_with((self.bluetooth_device_name, self.port))

    @patch("bluetooth.discover_devices")
    def test_scan(self, bluetooth_discover_devices_mock):
        bluetooth_discover_devices_mock.return_value = self.available_devices

        scanned_devices = ODBUtils.scan()
        bluetooth_discover_devices_mock.assert_called_once_with(duration=10, flush_cache=True, lookup_names=True)

        self.assertEquals(len(self.available_devices), len(scanned_devices))
        self.assertEquals(self.available_devices[0][0], scanned_devices[0][0])
        self.assertEquals(self.available_devices[0][1], scanned_devices[0][1])
        self.assertEquals(self.available_devices[1][0], scanned_devices[1][0])
        self.assertEquals(self.available_devices[1][1], scanned_devices[1][1])

    def test_send(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals("41 0C 1A F8".split(" "), self.odb_utils.send("01", "0C"))

        self.bluetooth_device_mock.send.assert_called_once_with("010C\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

    def test_engine_load(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 04 55")

        self.assertEquals(33, self.odb_utils.engine_load())

        self.bluetooth_device_mock.send.assert_called_once_with("0104\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

    def test_engine_rpm(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 0C 1A F8")

        self.assertEquals(1726, self.odb_utils.engine_rpm())

        self.bluetooth_device_mock.send.assert_called_once_with("010C\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

    def test_vehicule_speed(self):
        self.bluetooth_device_mock.recv = MagicMock(return_value="41 0D B4")

        self.assertEquals(180, self.odb_utils.vehicule_speed())

        self.bluetooth_device_mock.send.assert_called_once_with("010D\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

if __name__ == '__main__':
    unittest.main()

