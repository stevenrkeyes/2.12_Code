# main.py
# Author: Steven Keyes for 2.12 team
# Date: 30 November 2014

# note: in networ
import network_vision
import sys # for stopping everthing if there's an error
import socket # for handling connection errors
import time

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

# TODO: wait to start trajectory stuff until the ball is actually on the field
# for now, i'm just waiting until a user specifies that the ball is released
# but it would be good to detect it somehow
raw_input("press enter when ball is released")
# read out all the old data from the vision network because we don't need it
nv.read()

# for the first few samples (maybe 1/2 a second),
# read points from the vision server, feed them to the trajectory model,
# and plot the points

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
