# -*- coding: utf-8 -*-
from __future__ import absolute_import
import math
import bluetooth

from .OBDUtilsExceptions import InvalidResponseModeException, InvalidResponsePIDException, NoResponseException, \
    InvalidCommandResponseException
from bluetooth import BluetoothSocket, RFCOMM

DATA_SIZE = 1024


class OBDUtils:
    def __init__(self, bluetooth_device_address, bluetooth_device_port, debug=False):
        self._bluetooth_device = None
        self._bluetooth_device_address = bluetooth_device_address
        self._bluetooth_device_port = bluetooth_device_port
        self._debug = debug

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

    def close(self):
        if self.debug is True:
            print("Closing socket...")

        self.bluetooth_device.close()

    def initialize(self):
        print("Initializing ELM327...")
        atz_response = self.send_command("AT WS")
        if "ELM" not in atz_response[-1]:
            raise InvalidCommandResponseException("***ELM***", atz_response[-1])

        print("Deleting stored protocol...")
        at_sp_00_response = self.send_command("AT SP 00")
        if at_sp_00_response[-1] != "OK":
            raise InvalidCommandResponseException("OK", at_sp_00_response[-1])

        print("Selecting protocol...")
        at_sp_0_response = self.send_command("AT SP 0")
        if at_sp_0_response[-1] != "OK":
            raise InvalidCommandResponseException("OK", at_sp_0_response[-1])

    def send(self, mode, pid, number_of_lines=None):
        obd_request = OBDRequest(self.bluetooth_device, mode, pid, number_of_lines, self.debug)
        obd_request.send()

        return obd_request.data

    def send_command(self, command):
        obd_command = OBDCommand(self.bluetooth_device, command, self.debug)
        obd_command.send()

        return obd_command.data

    def engine_load(self):
        data = self.send("01", "04", "1")

        return math.floor(float(int("0x" + data[2], 0)) / 255 * 100)

    def engine_rpm(self):
        data = self.send("01", "0C", "1")

        return int("0x" + data[2] + data[3], 0) / 4

    def vehicule_speed(self):
        data = self.send("01", "0D", "1")

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

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug


class OBDCommand(object):
    def __init__(self, serial_device, command, debug=False):
        self._serial_device = serial_device
        self._command = command
        self._data = None
        self._debug = debug

    def send(self):
        query_string = self.command + "\r"

        if self.debug is True:
            print("Sending %s..." % repr(query_string))
        self.serial_device.send(query_string)

        self.data = ""
        while True:
            tmp_data = self.serial_device.recv(DATA_SIZE)
            if self.debug is True:
                print("Received %s..." % repr(tmp_data))

            self.data += tmp_data

            if len(tmp_data) < 1 \
                    or tmp_data[-1] == ">":
                break

        self.extract_data()

    def extract_data(self):
        extracted_data = []
        for data_value in self.data.split("\r"):
            if len(data_value) > 0:
                extracted_data.append(data_value)

        self.data = extracted_data[:-1]

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

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug


class OBDRequest(OBDCommand):
    def __init__(self, serial_device, mode, pid, number_of_lines=None, debug=False):
        command = mode + " " + pid
        if number_of_lines is not None:
            command += " " + number_of_lines

        super(OBDRequest, self).__init__(serial_device, command)
        self._mode = mode
        self._pid = pid
        self._number_of_lines = number_of_lines
        self._debug = debug

    def send(self):
        super(OBDRequest, self).send()
        self.validate_checksum()

    def validate_checksum(self):
        if self.data is None \
                or len(self.data) == 0:
            raise NoResponseException()

        self.data = self.data[-1].split(" ")
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
    def number_of_lines(self):
        return self._number_of_lines

    @number_of_lines.setter
    def number_of_lines(self, number_of_lines):
        self._number_of_lines = number_of_lines

    @property
    def command(self):
        command = self.mode + " " + self.pid
        if self.number_of_lines is not None:
            command += " " + self.number_of_lines

        return command


