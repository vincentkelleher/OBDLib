from __future__ import absolute_import

import unittest
from ..ODBUtils import ODBRequest
from ..ODBUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException
from mock import MagicMock


class TestODBRequest(unittest.TestCase):
    def setUp(self):
        self.bluetooth_device_mock = MagicMock()

        self.odb_request = ODBRequest(self.bluetooth_device_mock, "01", "0C")

    def test_successful_response(self):
        self.bluetooth_device_mock.recv = MagicMock(side_effect=["01 0C\r41 0C 1A F8 \r", "\r>"])

        try:
            self.odb_request.send()
        except InvalidResponseModeException:
            self.fail("InvalidResponseModeException has been raised !")
        except InvalidResponsePIDException:
            self.fail("InvalidResponsePIDException has been raised !")

    def test_wrong_mode_response(self):
        self.bluetooth_device_mock.recv = MagicMock(side_effect=["01 0C\r42 0C 1A F8 \r", "\r>"])

        self.assertRaises(InvalidResponseModeException, lambda: self.odb_request.send())

    def test_wrong_pid_response(self):
        self.bluetooth_device_mock.recv = MagicMock(side_effect=["01 0C\r41 01 1A F8 \r", "\r>"])

        self.assertRaises(InvalidResponsePIDException, lambda: self.odb_request.send())

    def test_no_response(self):
        self.assertRaises(NoResponseException, lambda: self.odb_request.send())

    def test_empty_response(self):
        self.assertRaises(NoResponseException, lambda: self.odb_request.send())

    def test_send(self):
        self.odb_request.validate_checksum = MagicMock()
        self.bluetooth_device_mock.recv = MagicMock(side_effect=["01 0C\r41 0C 1A F8 \r", "\r>"])

        self.odb_request.send()
        self.assertEquals(['01 0C', '41 0C 1A F8 '], self.odb_request.data)

        self.bluetooth_device_mock.send.assert_called_once_with("01 0C\r")
        self.odb_request.validate_checksum.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
