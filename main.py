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

# Start polling the vision network server
nv.start_polling()

# create a trajectory tracker object with the workspace of the robot
def sliding_ball_model(t, v_initial, acc, angle):
    return np.array([(v_initial*t**2.0 + acc*t)*np.sin(angle) + 20,
                     (v_initial*t**2.0 + acc*t)*np.cos(angle) + 20])
initial_guess = [-1,1,1]
tt = trajectory_tracker.TrajectoryTracker(sliding_ball_model, initial_guess,
                                          cg.Segment(np.array([380, 600]), np.array([410, 580])))

# TODO: wait to start trajectory stuff until the ball is actually on the field
# for now, i'm just waiting until a user specifies that the ball is released
# but it would be good to detect it somehow
raw_input("press enter when ball is released")
# read out all the old data from the vision network because we don't need it
nv.read()

start_time = time.time()

# make a plot for the field
fig = plt.figure()
#plt.axis([0, 664, 0, 472])
plt.axis([0, 6640, 0, 4720])
plt.ion()
plt.show()

# for the first few samples (maybe 1/2 a second),
# read points from the vision server, feed them to the trajectory model,
# and plot the points
# for the first few samples (maybe 1/2 a second),
while len(tt.model.xsamples) < 300:
    new_data = nv.read()
    for datum in new_data:
        (coordinates, timestamp)  = extract_vision_network_data(datum)
        tt.model.add_sample(timestamp, coordinates)
        # draw the new points
        plt.scatter(*coordinates)
        plt.draw()
    time.sleep(0.0166)    

# plot the sample points
#sample_points_plot = plt.plot(*tt.model.ysamples)#, marker='o', linestyle="none")


# then, until the ball is close enough,
# read points from the vision server, feed them to the trajectory model,
# and recalculate a new trajectory and intersection point
# and plot the points and trajectory

# then, command the foot to go to x,y position above the intersection point
# and z position above the ball
# and, at the time of intersection, lower the foot

# then, (optionally) push the ball somewhere better

# then, do the kick trajectory

N = 10
for n in range(0,N):
    # nv.read() returns any new data points published by the server
    print "number of new points read:", len(nv.read())
    time.sleep(0.5)
    
# stop polling the vision network server
nv.stop_polling()

# close the connection with the vision network server
print('Closing Connection...')
nv.disconnect()
