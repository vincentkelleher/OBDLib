# -*- coding: utf-8 -*-
from __future__ import absolute_import
import math
import bluetooth

from .ODBUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException
from bluetooth import BluetoothSocket, RFCOMM

DATA_SIZE = 1024


class ODBUtils:
    def __init__(self, bluetooth_device_address, bluetooth_device_port):
        self._bluetooth_device = None
        self._bluetooth_device_address = bluetooth_device_address
        self._bluetooth_device_port = bluetooth_device_port

    @staticmethod
    def scan():
        print("Scanning for nearby devices...")
        nearby_devices = bluetooth.discover_devices(duration=10, flush_cache=True, lookup_names=True)
        print("Found %d devices..." % len(nearby_devices))

        for nearby_device in nearby_devices:
            print(" - %s at %s" % (nearby_device[1], nearby_device[0]))

        return nearby_devices

    def connect(self):
        if self.bluetooth_device is None:
            self.bluetooth_device = BluetoothSocket(RFCOMM)

        self.bluetooth_device.connect((self.bluetooth_device_address, self.bluetooth_device_port))

    def initialize(self):
        self.send_command("AT Z")
        self.send_command("AT SP 0")

    def send(self, mode, pid):
        odb_request = ODBRequest(self.bluetooth_device, mode, pid)
        odb_request.send()

        return odb_request.data

    def send_command(self, command):
        odb_command = ODBCommand(self.bluetooth_device, command)
        odb_command.send()

        return odb_command.data

    def engine_load(self):
        data = self.send("01", "04")

        return math.floor(float(int("0x" + data[2], 0)) / 255 * 100)

    def engine_rpm(self):
        data = self.send("01", "0C")

        return int("0x" + data[2] + data[3], 0) / 4

    def vehicule_speed(self):
        data = self.send("01", "0D")

        return int("0x" + data[2], 0)

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


class ODBCommand(object):
    def __init__(self, serial_device, command):
        self._serial_device = serial_device
        self._command = command
        self._data = None

    def send(self):
        query_string = self.command + "\r"

        print("Sending %s..." % repr(query_string))
        self.serial_device.send(query_string)

        tmp_data = None
        while True:
            tmp_data = self.serial_device.recv(DATA_SIZE)
            if len(tmp_data) < 1:
                break

            self.data = tmp_data
            print("Received %s..." % repr(self.data))

    @property
    def serial_device(self):
        return self._serial_device

    @serial_device.setter
    def serial_device(self, serial_device):
        self._serial_device = serial_device

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command


class ODBRequest(ODBCommand):
    def __init__(self, serial_device, mode, pid):
        super(ODBRequest, self).__init__(serial_device, mode + " " + pid)
        self._mode = mode
        self._pid = pid

    def send(self):
        super(ODBRequest, self).send()

        self.validate_checksum()

    def validate_checksum(self):
        if self.data is None \
                or len(self.data) == 0:
            raise NoResponseException()

        self.data = self.data.split(" ")
        response_mode = int(self.data[0])

        if response_mode != int(self.mode) + 40:
            raise InvalidResponseModeException(self.mode, response_mode - 40)

        if self.data[1] != self.pid:
            raise InvalidResponsePIDException(self.pid, self.data[1])

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

