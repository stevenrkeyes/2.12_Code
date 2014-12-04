# main.py
# Author: Steven Keyes for 2.12 team
# Date: 30 November 2014

import sys # for stopping everthing if there's an error
import socket # for handling connection errors
import time
import numpy as np
from matplotlib import pyplot as plt

import network_vision
import trajectory_tracker
import computational_geometry as cg
import kick

def extract_vision_network_data(vision_network_data):
    return (np.array(vision_network_data[:2]), vision_network_data[6])

nv = network_vision.NetworkVision()
# uncomment below line if you're debugging locally
nv.serverIP = 'localhost'

# try to connect; if the connection isn't successful, stop the program
try:
    print "connecting to vision network server..."
    nv.connect()
except socket.error:
    print "unable to connect to server; stopping program"
    sys.exit(0)
#Robot sets up for kick
kick.wake_up()
# Start polling the vision network server
nv.start_polling()

# create a trajectory tracker object with the workspace of the robot
def sliding_ball_model(t, v_initial, acc, angle):
    return np.array([(v_initial*t**2.0 + acc*t)*np.sin(angle) + 20,
                     (v_initial*t**2.0 + acc*t)*np.cos(angle) + 20])
initial_guess = [-1,1,1]
# uncomment value for actual field
robot_ground_position_x_in_px = 1500#160.25*664/180
workspace_boundary = cg.Segment(np.array([robot_ground_position_x_in_px, 12]),
                                np.array([robot_ground_position_x_in_px, 880]))
tt = trajectory_tracker.TrajectoryTracker(sliding_ball_model,
                                          initial_guess,
                                          workspace_boundary)

# TODO: wait to start trajectory stuff until the ball is actually on the field
# for now, i'm just waiting until a user specifies that the ball is released
# but it would be good to detect it somehow
raw_input("press enter when ball is released")
# read out all the old data from the vision network because we don't need it
nv.read()

start_time = time.time()

# make a plot for the field
fig = plt.figure()
plt.axis([0, 664*4, 0, 472*4])
# Uncomment for actual field
#plt.axis([0, 664, 0, 472])
plt.ion()
plt.show()

# plot the workspace boundary line
plt.plot([robot_ground_position_x_in_px, robot_ground_position_x_in_px],[12, 880])

# for the first few samples (maybe 1/2 a second),
# read points from the vision server, feed them to the trajectory model,
# and plot the points
# for the first few samples (maybe 1/2 a second),
div10 = 0
while len(tt.model.xsamples) < 15:
    new_data = nv.read()
    for datum in new_data:
        (coordinates, timestamp) = extract_vision_network_data(datum)
        tt.model.add_sample(timestamp, coordinates)
        div10 += 1
        # draw the new points every 10th point or so
        if div10 % 15 == 0:
            plt.scatter(*coordinates)
            plt.draw()
    time.sleep(0.0166)
print "150 samples collected"

# then, until the ball is close enough,
# read points from the vision server, feed them to the trajectory model,
# and recalculate a new trajectory and intersection point
# and plot the points and trajectory
estimated_arrival_time = 10000
time_to_arrival = 10000
while len(tt.model.xsamples) < 900 and time_to_arrival > 2.0: #TIME THRESHOLD
    new_data = nv.read()
    for datum in new_data:
        (coordinates, timestamp) = extract_vision_network_data(datum)
        tt.model.add_sample(timestamp, coordinates)
        div10 += 1
        if div10 % 15 == 0:
            plt.scatter(*coordinates)
            plt.draw()
    # re-tune the ball trajectory curve fit
    tt.model.optimize_parameters()

    # plot the predicted ball trajectory
    t_for_fit = np.array([tt.model.xsamples[0], tt.model.xsamples[-1]+5])
    x_fitted = tt.model.evaluate(t_for_fit)
    curve_fit = plt.plot(*x_fitted)
    plt.draw()

    # estimate the time until arrival
    e = tt.estimate_arrival_time(tt.model.xsamples[-1])
    # check if an intersection is predicted
    if e != None:
        estimated_arrival_time = e
    print estimated_arrival_time - tt.model.xsamples[-1]
    time_to_arrival = estimated_arrival_time - tt.model.xsamples[-1]
    print "estimated time to arrival:", time_to_arrival

kick_motion_time = 0.5
time.sleep(time_to_arrival - kick_motion_time)

# then, do the kick trajectory
kick.kick()
time.sleep(1.5)
kick.zero()
    
# stop polling the vision network server
nv.stop_polling()

kick.m.disconnect()

# close the connection with the vision network server
print('Closing Connection...')
nv.disconnect()
