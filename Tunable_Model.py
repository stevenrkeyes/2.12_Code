# Tunable_Model.py
# Author: Steven Keyes, 2.12 team
# Date: 10 November 2014

import numpy as np
from scipy import optimize as opt

# I suspect Shapely would be faster than sumpy for this purpose at least
# because it contains wrappers of C function calls instead of python
# implementations, but I haven't been able to successfully install shapely
# on a windows machine.
# Python wrappers for OpenCV might be a good alternative.
# -Steven


# TunableModel is an object for storing a function, samples, and optimal
# tunings to fit the function to that sample data.
# dimensions is the dimensionality of the y vector; the x vector is assumed
# to be 1 dimensional
class TunableModel:
    def __init__(self, function, initial_parameter_guess, dimensions=2):
        self.function = function
        self.parameters = initial_parameter_guess
        self.dimensions = dimensions
        
        # the samples of the independent variable
        self.xsamples = np.array([])

        # the samples of the dependent variable
        self.ysamples = np.array([]).reshape(dimensions, 0)

    def add_sample(self, xsample, ysample):
        self.xsamples = np.append(self.xsamples, xsample)

        # turn the ysample into a column vector (2 dmins) instead of a
        # row vector (1 dim) by resizing
        # and append it to the ysamples
        sample_to_append = ysample.copy()
        sample_to_append.resize(testmodel.dimensions, 1)
        self.ysamples = np.hstack((self.ysamples, sample_to_append))

    def add_samples(self, xsamples, ysamples):
        # TODO: check that the inputs are of equal lengths
        self.xsamples = np.append(self.xsamples, xsamples)
        self.ysamples = np.hstack((self.ysamples, ysamples))

    def optimize_parameters(self):
        # compute new parameters using the last parameters as a starting point
        self.parameters = opt.leastsq(self.function_residual,
                                      self.parameters,
                                      args = (self.xsamples, self.ysamples))[0]

    def function_residual(self, parameters, x_sample, y_sample):
        y_predicted = self.function(x_sample, *parameters)
        return sum(((y_predicted - y_sample)**2.0))**0.5

    def evaluate(self, x_point):
        return self.function(x_point, *self.parameters)


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg
    import time

    # model where a is acceleration, (2*a + b) is the initial velocity
    # and the object is moving at angle c starting from [20,20]
    def g(t, a, b, c):
        #return t**2.0 * np.array([[d], [e]]) + \
        #       t * np.array([[a], [2*a]]) + \
        #       np.array([[b], [c]])
        #return np.array([a*t**1.5 + b*t + 20,
        #                 c*t**1.5 + d*t + 20])
        #return np.array([(1.0-0.8**(a*t))*b*np.sin(c)+20,
        #                 (1.0-0.8**(a*t))*b*np.cos(c)+20])
        return np.array([(a*t**2.0 + b*t)*np.sin(c)+20,
                         (a*t**2.0 + b*t)*np.cos(c)+20])

    tdata = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    # i'm tranposing this to perserve the convention that x,y coordinates are
    # column vectors, and the horizontal dimension of a matrix is time
    xdata = np.array([[20,20],[55,70],[75,114],[117,158],[143,200],
                      [166,240],[195,280],[221,322],[246,362],[268,400],
                      [288,436],[304,466],[324,500],[345,532],[362,554]]).transpose()

    test_model = TunableModel(g, [-1,1,1])
    #testmodel.add_samples(tdata, xdata)

    #testmodel.optimize_parameters()
    #print testmodel.parameters

    # drop a sample background
    field_background = mpimg.imread('field.png')
    plt.imshow(field_background)

    # limit the axes to the size of the image
    plt.axis([0, 600, 900, 0])
    
    # plot the sample points
    #plt.plot(*xdata, marker='o', linestyle="none")

    # simulate the curve fit and plot it
    #t = np.linspace(0, 15)
    #x_fitted = g(t, *test_model.parameters)
    #x_fitted = test_model.evaluate(t)
    #curve_fit = plt.plot(*x_fitted)

    # simulate the curve fit and plot it
    #t_prediction = np.linspace(15, 20)
    #x_predcted = g(t_prediction, *test_model.parameters)
    #curve_fit_predicted = plt.plot(*x_predcted, linestyle="dashed")


    #plt.show()
    #plt.show(block=False)
    #time.sleep(1)
    #curve_fit.pop(0).remove()
    #plt.show()


    # number of samples to wait until first prediction
    waitSamples = 14

    # plot the sample points
    sample_points_plot = plt.plot(*xdata[:, :waitSamples], marker='o', linestyle="none")
    
    test_model.add_samples(tdata[:waitSamples], xdata[:,:waitSamples])

    # simulate the curve fit and plot it
    t = np.linspace(0, tdata[waitSamples])
    #x_fitted = g(t, *test_model.parameters)
    x_fitted = test_model.evaluate(t)
    curve_fit = plt.plot(*x_fitted)

    # simulate the curve fit and plot it
    #t_prediction = np.linspace(waitSamples, waitSamples+5)
    #x_predicted = g(t_prediction, *test_model.parameters)
    #curve_fit_predicted = plt.plot(*x_predicted, linestyle="dashed")

    plt.show()
    #plt.show(block=False)

    #for i in range(waitSamples,15):
    #    test_model.add_sample(tdata[i], xdata[:,i])
    #    test_model.optimize_parameters()
    #    print test_model.parameters
    #
    #plt.show()
