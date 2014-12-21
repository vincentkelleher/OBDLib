# -*- coding: utf-8 -*-
import serial

class ODBLib:

    def __init__(self, serial_device_name, baudrate):
        self.serial_device_name = serial_device_name
        self.baudrate = baudrate

    def connect(self):
        self.serial = serial.Serial(self.serial_device_name, self.baudrate, timeout=1)
