#Robot Kinematics
import math


##Class of functions dedicated to do the inverse kinematics of the robot system
##for 2.12 robotics soccer competition.
class Robot_Kinematics:
    """
    Constructor for Robot_Kin Class.
        The Robot's coordinates refers to the location of the base plate's
        center of mass that is connected to link 1
        X_origin: Robot X coordinate in the world: float
        Y_origin: Robot Y coordinate in the world: float
        Z_origin: Robot Z coordinate in the world: float
        X_limit: The length of the field in the X direction: float
        Y_limt: The length of the field in the Y direction: float
        LX: The length of link X
        """
    def __init__(self, X_origin, Y_origin, Z_origin, X_limit, Y_limit,
                 L1, L2, L3, L4):
        self.x_o = float(X_origin)
        self.y_o = float(Y_origin)
        self.z_o = float(Z_origin)
        self.MAX_X = float(X_limit)
        self.MAX_Y = float(Y_limit)
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        

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
    def convertWorldCoord(X, Y, Z):
        xr = X - self.x_o
        yr = Y - self.y_o
        zr = Z
        return (xr, yr, zr)

    """
    Given the coordinates of Point C(the endpoint of Link 3 connected to
    Link 4), returns the angles of theta1, theta2,and theta3 in a tuple.
    XC: X coord of Point C: float
    YC: Y coord of Point C: float
    ZC: Y coord of Point C: float

    return tuple(theta1, theta2, theta3) in radians
    """
    def findThetas(XC, YC, ZC):
        theta1 = math.atan2(XC, YC) # Theta1
        
        # Point A Coords (Point connected to Link 1 and 2)
        XA = self.x_o - self.LI*math.sin(theta1)
        YA = self.y_o - self.L1*math.cos(theta1)
        ZA = self.z_o

        #Distance of Point A and Point C in XY Plane
        rc = math.sqrt(math.pow((XC-XA), 2) + math.pow((YC-YA),2))

        #Distance of Point A and Point C in XYZ Space
        dc = math.sqrt(math.pow((ZC-ZA), 2) + math.pow(rc, 2))

        gamma_arg = ((math.pow(dc,2) + math.pow(self.L2,2) - math.pow(self.L3,2))/(2*dc*self.L2))
        theta2 = math.atan2(rc, ZA) - math.acos(gamma_arg)

        beta_arg = ((math.pow(self.L2, 2)+math.pow(self.L3, 2) - math.pow(dc, 2))/(2*self.L2*self.L3))
        theta3 = math.pi - math.acos(beta_arg)

        return(theta1, theta2, theta3)

    
        
