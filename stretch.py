#Stretch Program, Testing Leg movements
#Version 1.0
#Date: 12.1.2014
#Details about Robot System:
#L1 refers to link 1, L2 -> link 2 and so forth
#Point A connects Link 1 and 2, B connects 2 and 3, C connects 3 and 4
import math
from workspace import Workspace
from robot_kinematics import Robot_Kinematics

#ronaldo is the robot test name, pele is tester for python code
#create the ronaldo kinematics object [CHANGE Z, and LINK LENGTHS]
ronaldo = Robot_Kinematics(166.25, 72.0, 24.0, 192.0, 144.0, 6.0, 11.0, 11.0)
pele = Robot_Kinematics(2.0, 2.0, 2.0, 192.0, 144.0, 1.0, 1.0, 1.0)

##Pele Section: Given a point in the world, tells you what the thetas of
##each motor should be to reach to the point. If the point is not reachable
##return string message instead. 

def pele_model():
    #Receive input from user as to which point in the world you want to reach
    #Receives input for pele
    x_pele = float(input("Enter your X: "))
    y_pele = float(input("Enter your Y: "))
    z_pele = float(input("Enter your Z: "))
    (xp, yp, zp) = pele.convertWorldCoord(x_pele, y_pele, z_pele)
    print("X: "+ str(xp))
    print("Y: "+ str(yp))
    print("Z: "+ str(zp))
    if pele.isReachable(xp, yp, zp):
        return pele.findThetas(xp, yp, zp)
    else:
        return "Point is not Reachable"

##Ronaldo Section: Given a point in the world, moves the motors to desired thetas
##If point is not reachable, returns a string message to console and places motors
##at desinated zeros

def ronaldo_model():
    #Receive input from user as to which point in the world you want to reach
    #Receives input for ronaldo
    x_ronaldo = float(input("Enter your X: "))
    y_ronaldo = float(input("Enter your Y: "))
    z_ronaldo = float(input("Enter your Z: "))
    (xr, yr, zr) = ronaldo.convertWorldCoord(x_ronaldo, y_ronaldo, z_ronaldo)
    print xr
    print yr
    print zr
    if ronaldo.isReachable(xr, yr, zr):
        #TO-DO: Add code to motors 
        return ronaldo.findThetas(xr, yr, zr)
    else:
        return "Point is not Reachable"


