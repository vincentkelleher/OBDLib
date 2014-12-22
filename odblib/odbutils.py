# -*- coding: utf-8 -*-
import serial

class ODBUtils:

    def __init__(self, serial_device_name, baudrate):
        self.serial_device = None
        self.serial_device_name = serial_device_name
        self.baudrate = baudrate

    def connect(self):
        if self.serial_device is None:
            self.serial_device = serial.Serial(self.serial_device_name, self.baudrate, timeout=1)
        else:
            self.serial_device.open()

    def send(self, data):
        self.serial_device.write(data)

        return self.serial_device.readline()

    def engine_rpm(self):
        self.send("01 0C\r")

    def set_serial_device(self, serial_device):
        self.serial_device = serial_device
