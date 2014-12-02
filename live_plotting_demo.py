from matplotlib import pyplot as plt
import numpy as np
import time

fig=plt.figure()
plt.axis([0,10,0,1])
plt.ion()
plt.show()

i=0
x=list()
y=list()

for i in range(10):
    temp_y=np.random.random()
    x.append(i)
    y.append(temp_y)
    plt.scatter(i,temp_y)
    plt.draw()
    time.sleep(0.05)

