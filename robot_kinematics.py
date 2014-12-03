#Robot Kinematics
#Version 1.2
#-includes workspace
#Date 11/29/2014
#Details about Robot System:
#L1 refers to link 1, L2 -> link 2 and so forth
#Point A connects Link 1 and 2, B connects 2 and 3, C connects 3 and 4
import math
from workspace import Workspace


##Class of functions dedicated to do the inverse kinematics of the robot system
##for 2.12 robotics soccer competition.
class Robot_Kinematics:
    """
    Constructor for Robot_Kin Class.
        The Robot's coordinates refers to the location of the base plate's
        center of mass that is connected to link 1
        X_origin: Robot X coordinate in the world: float(inches)
        Y_origin: Robot Y coordinate in the world: float(inches)
        Z_origin: Robot Z coordinate in the world: float(inches)
        X_limit: The length of the field in the X direction: float(inches)
        Y_limt: The length of the field in the Y direction: float(inches)
        LX: The length of link X
        """
    def __init__(self, X_origin, Y_origin, Z_origin, X_limit, Y_limit,
                 L1, L2, L3):
        self.x_o = float(X_origin)
        self.y_o = float(Y_origin)
        self.z_o = float(Z_origin)
        self.MAX_X = float(X_limit)
        self.MAX_Y = float(Y_limit)
        self.L1 = float(L1)
        self.L2 = float(L2)
        self.L3 = float(L3)
        self.workspace = Workspace(X_origin, Y_origin, Z_origin, L1, L2, L3)
        

    """
    Converts the coordinates of a point in the world system to coordinates
    of a point in the robots system, where the robot's location is the origin.
    To keep things simple, the axis of the robots system are alined with the
    axis of the world's:
    X: World's X coord: float
    Y: World's Y coord: float
    Z: World's Z coord: float

    returns tuple of (xp, yp, zp) of robot coordinates
    """
    def convertWorldCoord(self, X, Y, Z):
        xr = self.x_o - X
        yr = self.y_o - Y
        zr = Z - self.z_o
        return (xr, yr, zr)

    """
    Given the coordinates of Point C(the endpoint of Link 3 connected to
    Link 4), returns the angles of theta1, theta2,and theta3 in a tuple.
    XC: X coord of Point C: float
    YC: Y coord of Point C: float
    ZC: Y coord of Point C: float

    return tuple(theta1, theta2, theta3) in radians
    """
    def findThetas(self, XC, YC, ZC):
        theta1 = math.atan2(YC, XC) # Theta1
        
        # Point A Coords (Point connected to Link 1 and 2)
        XA = self.L1*math.cos(theta1)
        YA = self.L1*math.sin(theta1)
        ZA = 0.0

        #Distance of Point A and Point C in XY Plane
        rc = math.sqrt(math.pow((XC-XA), 2) + math.pow((YC-YA),2))

        #Distance of Point A and Point C in XYZ Space
        dc = math.sqrt(math.pow((ZC-ZA), 2) + math.pow(rc, 2))

        gamma_arg = ((math.pow(dc,2) + math.pow(self.L2,2) - math.pow(self.L3,2))/(2*dc*self.L2))
        theta2 = math.atan2(rc, ZC) - math.acos(gamma_arg)

        beta_arg = ((math.pow(self.L2, 2)+math.pow(self.L3, 2) - math.pow(dc, 2))/(2*self.L2*self.L3))
        theta3 = math.pi - math.acos(beta_arg)

        return(theta1, theta2, theta3)

    """
    Returns a boolean to determine if point is reachable(within the workspace
    of the robot)
    X: X coord in the world: float (inches)
    Y: Y coord in the world: float (inches)
    Z: Z coord in the wolrd: float (inches)
    """
    def isReachable(self, X, Y, Z):
        return self.workspace.containsPoint(X, Y, Z)

    """
    Creates the Jacobian representation for kinematics using theta 1, 2, and 3
    """
    def makeJacobian(theta1, theta2, theta3):
        #Forward kinematics derivative for theta1
        Xd1 = self.L1*math.cos(theta1) + self.L2*math.sin(theta2)*math.cos(theta1) + self.L3*math.sin(theta2+theta3)*math.cos(theta1)
        Yd1 = (self.L1*math.sin(theta1)+self.L2*math.sin(theta2)*math.sin(theta1)+ self.L3*math.sin(theta2+theta3)*math.sin(theta1))*(-1)
        Zd1 = 0.0

        #Forward kinematics derivative for theta2
        Xd2 = self.L2*math.cos(theta2)*math.sin(theta1) + self.L3*math.cos(theta2+theta3)*math.sin(theta1)
        Yd2 = self.L2*math.cos(theta2)*math.cos(theta1) + self.L3*math.cos(theta2+theta3)*math.cos(theta1)
        Zd2 = self.L2*math.sin(theta2) + self.L3*math.sin(theta2+theta3)

        #Forward kinematics derivative for theta3
        Xd3 = self.L3*math.cos(theta2+theta3)*math.sin(theta1)
        Yd3 = self.L3*math.cos(theta2+theta3)*math.cos(theta1)
        Zd3 = self.L3*math.sin(theta2+theta3)

        return ((Xd1, Xd2, Xd3),(Yd1, Yd2, Yd3), (Zd1, Zd2, Zd3))


    """
    Finds the torque 2 and 3 to order to provide Fx, Fy, and Fz
    """
    def findTorques(Fx, Fy, theta1, theta2, theta3):
        Jacobian = makeJacobian(theta1, theta2, theta3)
        torque2 = Jacobian[0,1]*Fx + Jacobian[1,1]*Fy + Jacobian[2,1]*Fz
        torque3 = Jacobian[0,2]*Fx + Jacobian[1,2]*Fy + Jacobian[2,2]*Fz
        return(torque2, torque3)

    
        

    
        

    
        
