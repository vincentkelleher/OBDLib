# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .ODBUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException
import bluetooth
from bluetooth import BluetoothSocket, RFCOMM

DATA_SIZE = 1024


class ODBUtils:
    def __init__(self, bluetooth_device_address, bluetooth_device_port):
        self._bluetooth_device = None
        self._bluetooth_device_address = bluetooth_device_address
        self._bluetooth_device_port = bluetooth_device_port

    @staticmethod
    def scan():
        return bluetooth.discover_devices()

    def connect(self):
        if self.bluetooth_device is None:
            self.bluetooth_device = BluetoothSocket(RFCOMM)

        self.bluetooth_device.connect((self.bluetooth_device_address, self.bluetooth_device_port))

    def send(self, mode, pid):
        odb_request = ODBRequest(self.bluetooth_device, mode, pid)
        odb_request.send()

        return odb_request.data

    def engine_rpm(self):
        data = self.send("01", "0C")

        return int("0x" + data[2] + data[3], 0) / 4

    @property
    def bluetooth_device(self):
        return self._bluetooth_device

    @bluetooth_device.setter
    def bluetooth_device(self, bluetooth_device):
        self._bluetooth_device = bluetooth_device

    @property
    def bluetooth_device_address(self):
        return self._bluetooth_device_address

    @bluetooth_device_address.setter
    def bluetooth_device_address(self, bluetooth_device_address):
        self._bluetooth_device_address = bluetooth_device_address

    @property
    def bluetooth_device_port(self):
        return self._bluetooth_device_port

    @bluetooth_device_port.setter
    def bluetooth_device_port(self, bluetooth_device_port):
        self._bluetooth_device_port = bluetooth_device_port


class ODBRequest:
    def __init__(self, serial_device, mode, pid):
        self._serial_device = serial_device
        self._mode = mode
        self._pid = pid
        self._data = None

    def send(self):
        self.serial_device.send(self.mode + " " + self.pid + "\r")
        data = self.serial_device.recv(DATA_SIZE).split(" ")

        self.validate_checksum(data)
        self.data = data

    def validate_checksum(self, data):
        if data is None \
                or len(data) == 0:
            raise NoResponseException()

        response_mode = int(data[0])

        if response_mode != int(self.mode) + 40:
            raise InvalidResponseModeException(self.mode, response_mode - 40)

        if data[1] != self.pid:
            raise InvalidResponsePIDException(self.pid, data[1])

    @property
    def serial_device(self):
        return self._serial_device

    @serial_device.setter
    def serial_device(self, serial_device):
        self._serial_device = serial_device

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        self._pid = pid

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

