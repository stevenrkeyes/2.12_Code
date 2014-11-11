# leastsq.py
# Author: Steven Keyes, for 2.12
# Date: 10 November 2014
# This file has some exmples of fitting a curve to a trajectory in 2D space
# though I guess it would also work in 3D. I was playing around with this code
# to figure out how to do this. Enjoy the examples!

from scipy import optimize as opt
import numpy as np
import matplotlib.pyplot as plt

# Example fitting a 1D model trajectory to sample points
'''
def f(t, a, b, c):
    return a*t**2.0 + b*t + c

def residual(p, t, x):
    return x - f(t, *p)

tdata = np.array([0, 1, 2, 3, 4])
xdata = np.array([1, 3, 6, 10, 15])

p0 = [0,0,0]

optparams = opt.leastsq(residual, p0, args = (tdata, xdata))[0]

plt.plot(tdata, xdata)
t = np.linspace(0, 5)
plt.plot(t, [f(time, *optparams) for time in t])
plt.show()
'''

'''
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def dist(self, other):
        return ((self.x-other.x)**2.0 - (self.y-other.y)**2.0)**0.5
'''

# Example fitting a 2D model trajectory to sample points, using numpy
# I'm pretty sure this can be done with curve_fit instead, but I'm not sure
# how to do this with points of several dimensions
def residual(p, t, x):
    x1 = g(t, *p)
    # (x1 - xdata) are the taxicab distances
    return sum(((x1 - xdata)**2.0))**0.5

# remember that g should be friendly with respect to t!
# specifically, it should return a column vector, whether t is
# a scalar or a vector
# well, nah, actually, it should return a row vector if t is a scalar
# but a column vector if t is even a vector with length 1.
# this is the way I have it now; the top commented out lines always return
# a column vector while the bottom uncommented lines follow the convention
# i describe.
def g(t, a, b, c, d, e):
    #return t**2.0 * np.array([[d], [e]]) + \
    #       t * np.array([[a], [2*a]]) + \
    #       np.array([[b], [c]])
    return np.array([d*t**2.0 + a*t + b,
                     e*t**2.0 + 2*a*t + c])

tdata = np.array([0,1,2,3,4])
# i'm tranposing this to perserve the convention that x,y coordinates are
# column vectors, and the horizontal dimension of a matrix is time
xdata = np.array([[3,3],[4,5],[7,9],[10,13],[15,15]]).transpose()

optparams = opt.leastsq(residual, [0,0,0,0,0], args = (tdata, xdata))[0]


# plot the sample points
plt.plot(*xdata, marker='o', linestyle="none")

# simulate the curve fit and plot it
t = np.linspace(0, 5)
x_fitted = g(t, *optparams)
plt.plot(*x_fitted)

plt.show()
