# network_vision.py
# Author: Steven Keyes for 2.12 team
# Date: 26 November 2014

# This code is based on the code by TA DGonz.
# NetworkVision is an object that represents the connection to the
# camera vision network; it can be used to return the most recent
# network vision data points.

import socket # for the network connection
import time # for polling timing
import struct # for packaging / unpackaging data
import signal
import Queue # for thread safe lists

import repeated_timer # for threads that are called repeatedly

class NetworkVision:
    
    def __init__(self):
        ########  Set up TCP/IP Connection ####
        # TCP/IP Connection Attributes
        #serverIP = '192.168.1.212'  #Use with the 2.12 Servers
        self.serverIP = 'localhost'      #Use for loopback testing on your own computer
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.sample_rate = 60 # Hz
        self.interval = 1.0 / self.sample_rate
        
        # a queue for the received data;
        # could have multiple data points if it hasn't been checked in a while
        # note: using Queue.Queue because its pop method is thread safe
        self.data_received = Queue.Queue()

        # used to check if the value has been updated or not
        self.last_value = ()

        # object to control the timer thread that polls the network
        # (initilized when start_polling method is called)
        self.rt = None

    def connect(self):
        print 'Connecting...'
        self.s.connect((self.serverIP,2121))

    # get the current value published by the server
    def get_current_value(self):
        # the server responds if you send it a request for an update
        self.s.send('r')
        # here's the response
        raw = self.s.recv(16)
        x1 = struct.unpack('>H', raw[0:2])[0]
        y1 = struct.unpack('>H', raw[2:4])[0]
        a1 = struct.unpack('>H', raw[4:6])[0]
        x2 = struct.unpack('>H', raw[6:8])[0]
        y2 = struct.unpack('>H', raw[8:10])[0]
        a2 = struct.unpack('>H', raw[10:12])[0]
        timestamp = struct.unpack('>f', raw[12:16])[0]
        return (x1, y1, a1, x2, y2, a2, timestamp)

    # get values from the server and, if they're new, store them away
    # for the user to read later
    # otherwise, discard them because they're values we've already read
    def _poll_server(self):
        try:
            curr_value = self.get_current_value()
            # if the coordinates match, the values aren't new for 2.12
            if curr_value[:5] != self.last_value[:5]:
                self.data_received.put(curr_value)
                self.last_value = curr_value
        # but if the server has disconnected or otherwise broken, stop
        # polling (so repeated errors aren't raised), but raise a single error
        except socket.error as serr:
            # this line doesn't work because it looks like, with the
            # implementation i have, a repeated_timer can't stop itself
            # from inside the function it calls--perhaps because the next
            # timer has already started?
            #self.stop_polling()
            print "polling stopped -- connection error"
            raise serr
            
    
    # read the newest values from the network
    def read(self):
        ret = []
        # pop the entire queue
        while not self.data_received.empty():
            ret.append(self.data_received.get())
        return ret

    def start_polling(self):
        self.rt = repeated_timer.RepeatedTimer(self.interval, self._poll_server)

    def stop_polling(self):
        self.rt.stop()
    
    def disconnect(self):
        self.s.close()


if __name__ == "__main__":
    # an object for getting data from the vision network server
    nv = NetworkVision()
    # Connect to the vision network server
    # note: I'm just letting the code break if it's not connected, but in the final
    # code, you'd want to handle a failed connection attempt with
    # try: ... except socket.error: ...
    nv.connect()
    # Start polling the vision network server
    nv.start_polling()

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
