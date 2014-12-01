# field_recorder.py
# Author: Steven Keyes
# Date: 30 November 2014
# A utility to record ball movements on the field for debugging later

import network_vision
import pickle as pkl
import socket
import time

recording_time = 7 # seconds
filename = "field_recording_bouncing_1.pkl"
data = []

nv = network_vision.NetworkVision()
nv.connect()
print "connected"
nv.start_polling()
start_time = time.time()
while (time.time() - start_time < recording_time):
    data += nv.read()
    time.sleep(0.5)
nv.stop_polling()
nv.disconnect()
print "disconnected"

#pkl.dump(data, open(filename, "wb"))
#print "data recorded"

#pkl.load(open("field_recording.pkl", "rb"))
