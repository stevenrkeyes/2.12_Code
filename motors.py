#!/usr/bin/env python

"""
   example1.py - Move the servos to random positions and print out their current positions
   www.pirobot.org
"""

import os
import dynamixel
import time

class Motors:
    def __init__(self, nServos):
        # The number of Dynamixels on our bus.
        self.nServos = nServos
        self.net = None
        self.actuators = list()

    def connect(self):
        # Set your serial port accordingly.
        if os.name == "posix":
            portName = "/dev/ttyUSB0"
        else:
            portName = "COM3"
            
        # Default baud rate of the USB2Dynamixel device.
        baudRate = 400000
        
        # Connect to the serial port
        print "Connecting to serial port", portName, '...',
        self._serial = dynamixel.serial_stream.SerialStream(port=portName, baudrate=baudRate, timeout=1)
        print "Connected!"
        self.net = dynamixel.dynamixel_network.DynamixelNetwork(self._serial)
        self.net.scan(1, self.nServos)
        
        print "Scanning for Dynamixels...",
        for dyn in self.net.get_dynamixels():
            print dyn.id,
            self.actuators.append(self.net[dyn.id])
        print "...Done"

        self.initialize_motors()
        print "Motors initialized"

    def disconnect(self):
        self._serial.close()

    def initialize_motors(self):
        # Set the default speed and torque
        for actuator in self.actuators:
            actuator.moving_speed = 100
            actuator.synchronized = True
            actuator.torque_enable = True
            actuator.torque_control_enable = False
            actuator.goal_torque = 0
            actuator.torque_limit = 800
            actuator.max_torque = 800

    # set the position of a single motor -- range 0 to 4095, centered at 2047
    def set_position(self, motor_index, position):
        self.actuators[motor_index].goal_position = position
        self.net.synchronize()

    def set_positions(self, positions):
        # TODO: possibly check if lengths match
        for i in range(len(positions)):
            self.actuators[i].goal_position = positions[i]
        self.net.synchronize()

    def read_motor_position(self, motor_index):
        self.actuators[motor_index].read_all()
        time.sleep(0.01)
        return self.actuators[motor_index].cache[dynamixel.defs.REGISTER['CurrentPosition']]
    
    def read_motor_positions(self):
        for actuator in self.actuators:
            actuator.read_all()
            time.sleep(0.01)
        readings = list()
        for actuator in self.actuators:
            readings.append(actuator.cache[dynamixel.defs.REGISTER['CurrentPosition']])
        return readings
