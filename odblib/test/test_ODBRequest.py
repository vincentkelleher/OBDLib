import unittest
from ..ODBUtils import ODBRequest
from ..ODBUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException
from mock import MagicMock


class TestODBRequest(unittest.TestCase):
    test_valid_input = "41 0C 1A F8"

    def setUp(self):
        self.serial_device_mock = MagicMock()

        self.odb_request = ODBRequest(self.serial_device_mock, "01", "0C")

    def test_successful_response(self):
        self.serial_device_mock.readline = MagicMock(return_value=self.test_valid_input)

        try:
            self.odb_request.send()
        except InvalidResponseModeException:
            self.fail("InvalidResponseModeException has been raised !")
        except InvalidResponsePIDException:
            self.fail("InvalidResponsePIDException has been raised !")

    def test_wrong_mode_response(self):
        self.serial_device_mock.readline = MagicMock(return_value="42 0C 1A F8")

        self.assertRaises(InvalidResponseModeException, lambda: self.odb_request.send())

    def test_wrong_pid_response(self):
        self.serial_device_mock.readline = MagicMock(return_value="41 01 1A F8")

        self.assertRaises(InvalidResponsePIDException, lambda: self.odb_request.send())

    def test_no_response(self):
        self.assertRaises(NoResponseException, lambda: self.odb_request.send())

    def test_empty_response(self):
        self.assertRaises(NoResponseException, lambda: self.odb_request.send())

    def test_send(self):
        self.odb_request.validate_checksum = MagicMock()
        self.serial_device_mock.readline = MagicMock(return_value="41 0C 1A F8")

        self.odb_request.send()
        self.assertEquals(self.test_valid_input.split(" "), self.odb_request.data)

        self.serial_device_mock.write.assert_called_once_with("01 0C\r")
        self.odb_request.validate_checksum.assert_called_once_with(self.test_valid_input.split(" "))


if __name__ == '__main__':
    unittest.main()