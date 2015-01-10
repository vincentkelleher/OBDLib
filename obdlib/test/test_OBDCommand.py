# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
from ..OBDUtils import OBDCommand, DATA_SIZE
from mock import MagicMock, call


class TestOBDCommand(unittest.TestCase):
    def setUp(self):
        self.bluetooth_device_mock = MagicMock()

        self.obd_command = OBDCommand(self.bluetooth_device_mock, "AT Z")

    def test_send(self):
        extracted_data = ["AT Z", "ELM327 v2.1"]

        self.bluetooth_device_mock.recv = MagicMock(side_effect=["AT Z\r\r\rELM327 v2.1\r\r\r>"])

        self.obd_command.send()
        self.assertEquals(extracted_data, self.obd_command.data)

        self.bluetooth_device_mock.send.assert_called_once_with("AT Z\r")
        self.bluetooth_device_mock.recv.assert_has_calls([call(DATA_SIZE)])

if __name__ == '__main__':
    unittest.main()
