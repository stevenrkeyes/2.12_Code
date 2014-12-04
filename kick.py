#kick trajectory
#Version 1.0
#Date: 12/3/2014

import time
import math
import motors
from workspace import Workspace
from robot_kinematics import Robot_Kinematics
m = motors.Motors(4)
m.connect()
m.set_position_rad(0, 0.0)
m.set_position_rad(1, 0.0)
m.set_position_rad(2, 0.0)
m.set_position_rad(3, 0.0)
robot = Robot_Kinematics(166.25, 72.0, 24.25, 192.0, 144.0, 6.0, 8.5, 12.25)

#Relationship functions for the curve of the kick
#F1(t) = theta2_backlimit - alpha_o*time
#F2(t) = theta1_backlimit - beta_o*time
#F3(t) = gamma_o*time
# Trying to kick the ball in the an interval of 2sec:
# 1 sec to kick the ball and 1 sec to follow through
theta1_backlimit = -math.pi/8
theta2_backlimit = math.pi/8
theta1_forelimit = theta1_backlimit
alpha_0 = theta1_backlimit
beta_0 = theta2_backlimit
gamma_0 = theta1_forelimit

def zero():
    m.set_position_rad(0, 0.0)
    m.set_position_rad(1, 0.0)
    m.set_position_rad(2, 0.0)
    m.set_position_rad(3, 0.0)

"""
Moves leg into raising kicking position
"""

def wake_up():
    m.set_position_rad(0, theta1_backlimit)
    m.set_position_rad(1, theta2_backlimit)
    #m.set_position_rad(3, aim(x,y))

"""
Swing leg through to kick ball
"""

def kick():
    time_counter = 0
    interval = 0.2
    while (time_counter <= 1):
        theta1 = theta1_backlimit + alpha_0*time_counter
        theta2 = theta2_backlimit - beta_0*time_counter
        m.set_position_rad(0, theta2)
        m.set_position_rad(1, theta1)
        #print theta1
        #print theta2
        time_counter = time_counter+interval
        time.sleep(interval)

"""
Given the X and Y of the ball in the robot coord,
returns the desired ankle angle
"""

def aim(x,y):
    Goal_p = (154.0, 0.0) #INCHESS
    return math.atan2(Goal_p[1] - y, Goal_p[0] - x)

"""
Positions the leg at proper x,y,z point for kicking
"""
def positioning_leg(x,y):
    (xr,yr,zr) = robot.convertWorldCoord(x,y,0)
    if robot.isReachable(xr,yr,zr):
        (thetaMotor2, thetaMotor1, thetaMotor0) = robot.findThetas(xr, yr, 0.0)
        m.set_position_rad(2, thetaMotor2)

"""
Given the X, Y, Z coords of the ball in the world coord and the time of
intersection in the robot work space, robot kicks the ball
"""
def kicking_trajetory(x, y, z):
    wake_up()
    time.sleep(1)
    positioning_leg(x,y,z)
    time.sleep(1)
    kick()
    time.sleep(2)
    zero()

    
    
    

