# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .ODBUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException
import serial


class ODBUtils:
    def __init__(self, serial_device_name, baudrate):
        self._serial_device = None

        self._serial_device_name = serial_device_name
        self._baudrate = baudrate

    def connect(self):
        if self.serial_device is None:
            self.serial_device = serial.Serial(self.serial_device_name, self.baudrate, timeout=1)
        else:
            self.serial_device.open()

    def send(self, mode, pid):
        odb_request = ODBRequest(self.serial_device, mode, pid)
        odb_request.send()

        return odb_request.data

    def engine_rpm(self):
        data = self.send("01", "0C")

        return int("0x" + data[2] + data[3], 0) / 4

    @property
    def serial_device(self):
        return self._serial_device

    @serial_device.setter
    def serial_device(self, serial_device):
        self._serial_device = serial_device

    @property
    def serial_device_name(self):
        return self._serial_device_name

    @serial_device_name.setter
    def serial_device_name(self, serial_device_name):
        self._serial_device_name = serial_device_name

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        self._baudrate = baudrate


class ODBRequest:
    def __init__(self, serial_device, mode, pid):
        self._serial_device = serial_device
        self._mode = mode
        self._pid = pid
        self._data = None

    def send(self):
        self.serial_device.write(self.mode + " " + self.pid + "\r")
        data = self.serial_device.readline().split(" ")

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

