# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import time
from odblib.ODBUtils import ODBUtils

main_parser = argparse.ArgumentParser(prog="ODB", description="Connect to a bluetooth ODB II device")

scanning_group = main_parser.add_argument_group("Scanning for devices")
scanning_group.add_argument("--scan",
                    action="store_true",
                    help="scan for nearby devices")

connection_group = main_parser.add_argument_group("Connection to a device")
connection_group.add_argument("-a", "--address",
                    dest="address",
                    type=str,
                    help="specify the bluetooth device's address")
connection_group.add_argument("-p", "--port",
                    dest="port",
                    type=int,
                    help="specify the bluetooth device's port")

command_group = main_parser.add_argument_group("Send a command to a device")
command_group.add_argument("--mode",
                    dest="mode",
                    type=str,
                    help="mode of the command to send to the bluetooth device")
command_group.add_argument("--pid",
                    dest="pid",
                    type=str,
                    help="PID of the command to send to the bluetooth device")

interpreted_command_group = main_parser.add_argument_group("Interpreted commands")
interpreted_command_group.add_argument("--engine-load",
                    action="store_true",
                    help="get the current engine load")
interpreted_command_group.add_argument("--engine-rpm",
                    action="store_true",
                    help="get the current engine RPM")
interpreted_command_group.add_argument("--vehicule-speed",
                    action="store_true",
                    help="get the current vehicule speed")

args = main_parser.parse_args()

odbutils = None
if args.scan:
    scanned_devices = ODBUtils.scan()
elif args.address is not None \
        and args.port is not None:
    odbutils = ODBUtils(args.address, args.port)
    odbutils.connect()
elif args.address is not None \
        and args.port is not None \
        and args.mode is not None \
        and args.pid is not None:
    odbutils = ODBUtils(args.address, args.port)
    odbutils.connect()

    data = odbutils.send(args.mode, args.port)
    print("Returned data : %s" % data)
elif args.address is not None \
        and args.port is not None \
        and args.engine_load:
    odbutils = ODBUtils(args.address, args.port)
    odbutils.connect()

    print("Collecting engine load...")
    while True:
        current_load = odbutils.engine_load()
        print("Current engine load : %d%%" % current_load)
        time.sleep(200)
elif args.address is not None \
        and args.port is not None \
        and args.engine_rpm:
    odbutils = ODBUtils(args.address, args.port)
    odbutils.connect()

    print("Collecting engine RPM...")
    while True:
        current_rpm = odbutils.engine_rpm()
        print("Current RPM : %d rpm" % current_rpm)
        time.sleep(200)
elif args.address is not None \
        and args.port is not None \
        and args.vehicule_speed:
    odbutils = ODBUtils(args.address, args.port)
    odbutils.connect()

    print("Collecting vehicule speed...")
    while True:
        current_speed = odbutils.vehicule_speed()
        print("Current speed : %d km/h" % current_speed)
        time.sleep(200)
else:
    main_parser.print_help()
