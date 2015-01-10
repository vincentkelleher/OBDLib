# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
from ..OBDUtilsExceptions import InvalidCommandResponseException
from mock import MagicMock, patch, call
from ..OBDUtils import OBDUtils, DATA_SIZE


class TestOBDUtils(unittest.TestCase):
    available_devices = [
        ("TEST_DEVICE_ADDRESS", "TEST_DEVICE"),
        ("TEST_DEVICE_2_ADDRESS", "TEST_DEVICE_2"),
    ]
    bluetooth_device_name = "TEST_DEVICE"
    port = 1

    def setUp(self):
        self.obd_utils = OBDUtils(self.bluetooth_device_name, self.port)

        self.bluetooth_device_mock = MagicMock()
        self.bluetooth_device_mock.connect = MagicMock()
        self.bluetooth_device_mock.send = MagicMock()

        self.obd_utils.bluetooth_device = self.bluetooth_device_mock

        self.obd_utils.connect()
        self.bluetooth_device_mock.connect.assert_called_once_with((self.bluetooth_device_name, self.port))

    def test_initialize(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["AT Z\r\r\rELM327 v2.1\r\r\r>", "AT SP 00\rOK\r\r>", "AT SP 0\rOK\r\r>"])
        self.obd_utils.initialize()

        self.bluetooth_device_mock.send.assert_has_calls([call("AT Z\r"), call("AT SP 00\r"), call("AT SP 0\r")])
        self.bluetooth_device_mock.recv.assert_has_calls(
            [call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE)])

    def test_initialize_with_ATZ_error(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["AT Z\r\r\rNOT OK\r\r\r>", "AT SP 00\rOK\r\r>", "AT SP 0\rOK\r\r>"])

        self.assertRaises(InvalidCommandResponseException, lambda: self.obd_utils.initialize())

        self.bluetooth_device_mock.send.assert_called_once_with("AT Z\r")
        self.bluetooth_device_mock.recv.assert_called_once_with(DATA_SIZE)

    def test_initialize_with_AT_SP_00_error(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["AT Z\r\r\rELM327 v2.1\r\r\r>", "AT SP 00\rNOT OK\r\r>", "AT SP 0\rOK\r\r>"])

        self.assertRaises(InvalidCommandResponseException, lambda: self.obd_utils.initialize())

        self.bluetooth_device_mock.send.assert_has_calls([call("AT Z\r"), call("AT SP 00\r")])
        self.bluetooth_device_mock.recv.assert_has_calls([call(DATA_SIZE), call(DATA_SIZE)])

    def test_initialize_with_AT_SP_0_error(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["AT Z\r\r\rELM327 v2.1\r\r\r>", "AT SP 00\rOK\r\r>", "AT SP 0\rNOT OK\r\r>"])

        self.assertRaises(InvalidCommandResponseException, lambda: self.obd_utils.initialize())

        self.bluetooth_device_mock.send.assert_has_calls([call("AT Z\r"), call("AT SP 00\r"), call("AT SP 0\r")])
        self.bluetooth_device_mock.recv.assert_has_calls(
            [call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE)])

    @patch("bluetooth.discover_devices")
    def test_scan(self, bluetooth_discover_devices_mock):
        bluetooth_discover_devices_mock.return_value = self.available_devices

        scanned_devices = OBDUtils.scan()
        bluetooth_discover_devices_mock.assert_called_once_with(duration=10, flush_cache=True, lookup_names=True)

        self.assertEquals(len(self.available_devices), len(scanned_devices))
        self.assertEquals(self.available_devices[0][0], scanned_devices[0][0])
        self.assertEquals(self.available_devices[0][1], scanned_devices[0][1])
        self.assertEquals(self.available_devices[1][0], scanned_devices[1][0])
        self.assertEquals(self.available_devices[1][1], scanned_devices[1][1])

    def test_engine_load(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["01 04 1\rSEARCHING...\r", "41 04 55 \r", "\r>", "01 04 1\r41 04 55 \r", "\r>"])

        self.assertEquals(33, self.obd_utils.engine_load())
        self.assertEquals(33, self.obd_utils.engine_load())

        self.bluetooth_device_mock.send.assert_has_calls([call("01 04 1\r"), call("01 04 1\r")])
        self.bluetooth_device_mock.recv.assert_has_calls(
            [call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE)])

    def test_engine_rpm(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["01 0C 1\rSEARCHING...\r", "41 0C 1A F8 \r", "\r>", "01 0C 1\r41 0C 1C 20 \r", "\r>"])

        self.assertEquals(1726, self.obd_utils.engine_rpm())
        self.assertEquals(1800, self.obd_utils.engine_rpm())

        self.bluetooth_device_mock.send.assert_has_calls([call("01 0C 1\r"), call("01 0C 1\r")])
        self.bluetooth_device_mock.recv.assert_has_calls(
            [call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE)])

    def test_vehicule_speed(self):
        self.bluetooth_device_mock.recv = MagicMock(
            side_effect=["01 0D 1\rSEARCHING...\r", "41 0D B4 \r", "\r>", "01 0D 1\r41 0D B4 \r", "\r>"])

        self.assertEquals(180, self.obd_utils.vehicule_speed())
        self.assertEquals(180, self.obd_utils.vehicule_speed())

        self.bluetooth_device_mock.send.assert_has_calls([call("01 0D 1\r"), call("01 0D 1\r")])
        self.bluetooth_device_mock.recv.assert_has_calls(
            [call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE), call(DATA_SIZE)])


if __name__ == '__main__':
    unittest.main()

