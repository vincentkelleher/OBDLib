import unittest
from mockito import mock, spy, when
from ..odbutils import ODBUtils


class TestODBUtils(unittest.TestCase):
    serial_device_name = "TEST_DEVICE"
    baudrate = 38400

    def setUp(self):
        self.odb_utils = ODBUtils(self.serial_device_name, self.baudrate)

        self.serial_mock = mock()
        when(self.serial_mock).open().thenReturn()

        self.odbutils_spy = spy(self.odb_utils)
        self.odbutils_spy.set_serial(self.serial_mock)

        self.odbutils_spy.connect()

    def test_engine_rpm(self):
        pass

if __name__ == '__main__':
    unittest.main()

