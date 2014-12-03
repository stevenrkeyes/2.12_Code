#Workspace.py
#Version 1.0
#Date 11/29/2014
#Details about Robot System:
#L1 refers to link 1, L2 -> link 2 and so forth
#Point A connects Link 1 and 2, B connects 2 and 3, C connects 3 and 4

import math

#Class designed to represent the Workspace of the Striker Bot
class Workspace:
    """
    Constructor for the Workspace Class, needs the length of each
    link in the robot.
    LX: the length of link X: float
    X0, Y0, Z0: points of origin in robot system: float
    """
    def __init__(self, X0, Y0, Z0, L1, L2, L3):
        self.X0 = float(X0)
        self.Y0 = float(Y0)
        self.Z0 = float(Z0)
        self.L1 = float(L1)
        self.L2 = float(L2)
        self.L3 = float(L3)

    """
    Given a point in the ROBOT COORDINATE SYSTEM, figures out whether a point
    would be in the workspace of the robot or not.
    This function assumes the following constraints on the angles:
    theta1: 0 to pi
    theta2: -pi/2 to pi/2
    theta3: -pi/2 to pi/2
    NOTE: Due to the problem, the workspace has been reduced a bit to avoid
    singularities
    xp: x coord of the point: float
    yp: y coord of the point: float
    zp: z coord of the point: float
    returns True if point is in workspace, false otherwise
    """
    def containsPoint(self, xp, yp, zp):

        AB_offset = 0.0 #Offset between Link 1 and Link 2
        
        if math.atan2(xp, yp) < -math.pi and math.atan2(xp, yp) > 0.0:
            print("Failure of theta 1")
            return False

        #Derive Point A from pseudo-angle
        xap = self.L1*math.sin(math.atan2(xp, yp))
        yap = self.L1*math.cos(math.atan2(xp, yp))
        zap = 0.0

        z_limit = zap - self.L2
        dist_from_A = math.sqrt(math.pow(xp-xap, 2) + math.pow(yp-yap,2) +
                                math.pow(zp-zap, 2))
        print dist_from_A

        if zp > z_limit:
            print("Point too high")
            return False

        if dist_from_A < self.L2 or dist_from_A > self.L2 + self.L3:
            print("Point not in radius")
            return False

        return True

        
        
    
