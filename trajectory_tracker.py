# trajectory_tracker.py
# Author: Steven Keyes for 2.12 team
# Date: 10 November 2014

import numpy as np
import computational_geometry as cg
import tunable_model

# A TrajectoryTracker an object that predicts the motion of a physical
# object, such as a ball, and that can predict the arrival of that object
# into some zone. To accomplish this, a Trajectory_Tracker includes some
# tunable model for the general motion for the object as well as a
# geometric representation of the arrival area. Consequently, it can
# predict the time of arrival of the object as well as its exact
# coordinates upon arrive in the space. This could be used for estimating
# time to a collision or for estimating time for an uncontrolled object
# to arrive within the workspace of a robot.

class TrajectoryTracker:
    # trajectory_model is a function of time, to be passed to a TunableModel
    # and has time as its first argument and all other parameters next
    # trajectory_model_parameters is a guess of those other initial parameters
    # arrival_zone is an instance from cg, maybe a GeometryEntity of some kind,
    # though I haven't fleshed that out yet
    def __init__(self, trajectory_model, model_parameters, arrival_zone, t_max = 5):

        self.model = tunable_model.TunableModel(trajectory_model, model_parameters, dimensions=2)
        
        # inverse time solution function would be nice

        self.arrival_zone = arrival_zone

        # farthest time to look into the future for planning
        self.t_max = t_max
        self.t_divisions = 500

    def estimate_arrival_time(self, current_time):
        # we're going to estimate the time of arrival by approximating the predicated
        # path as a string of line segments and checking which of these line segments
        # intersects the workspace, if any
        t_points = np.linspace(current_time, current_time+self.t_max, self.t_divisions)
        curr_t = t_points[0]
        curr_point = self.model.evaluate(curr_t)
        for i in range(self.t_divisions)[1:]:
            # shift down to the next line segment
            prev_t = curr_t
            prev_point = curr_point
            
            curr_t = t_points[i]
            curr_point = self.model.evaluate(curr_t)
            
            segment = cg.Segment(prev_point, curr_point)
            if self.arrival_zone.intersects(segment):
                return curr_t
        return None
        
        
if __name__ == "__main__":
    # model where a is acceleration, (2*a + b) is the initial velocity
    # and the object is moving at angle c starting from [20,20]
    def g(time, a, b, c):
        return np.array([(a*time**2.0 + b*time)*np.sin(c)+20,
                         (a*time**2.0 + b*time)*np.cos(c)+20])
    tdata = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    xdata = np.array([[20,20],[63,70],[90,114],[117,158],[143,200],
                      [166,240],[195,280],[221,322],[246,362],[268,400],
                      [288,436],[304,466],[324,500],[345,532],[362,554]]).transpose()

    #tt = TrajectoryTracker(g, [-1,1,1], sg.Circle(sg.Point(435, 665), 50))
    tt = TrajectoryTracker(g, [-1,1,1], cg.Segment(np.array([380, 600]), np.array([410, 580])))
    tt.model.add_samples(tdata, xdata)
    tt.model.optimize_parameters()
    
    print tt.estimate_arrival_time(15)

'''
class bouncing_ball_trajectory(trajectory):
    def __init__(self):
        pass

# A Trajectory object is a representation of the predicted trajectory of
# an object. This is not limited by dimensionality.
# it includes a list of sample points already traversed, a general model
# for the motion of an object, and specific parameters tunings of the model
# For example, a trajectory might model a bouncing ball, rolling ball, or
# sliding ball and include sample points from a recording of those.


# workspace is an instance of sg.entity.GeometryEntity
class workspace:
    def __init__(self):
        pass

    # return true if the workspace contains the indicated point
    def contains(self, point):
        pass

if __name__ == "__main__":
    def sliding_ball_model(t, parameters):
        v0x = parameters[0]
        v0y = parameters[1]
        x_coord = max(0.0, 1.0*v0x*t - t**2.0)
        y_coord = max(0.0, 1.0*v0y*t - t**2.0)
        return point(x_coord, y_coord)

    sliding_ball_trajectory = trajectory(sliding_ball_model, [6.0, 6.0])
'''
