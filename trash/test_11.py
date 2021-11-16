from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt
import time as ti
import os as os 


for stim in L:
    exc += sum(stimulus(t,stim[0],stim[1],stim[2],stim[3]))
    



intensite = Constant('intensite',5)
Duree = Constant('Duree', 400)
Ti = Constant('Ti',200)
laps = Constant('laps', 50)

stringified_stimulus = "g(t-" + str(Ti) + "," + str(intensite) +","+ str(laps) + ",t-" + str(Duree) + "-" + str(Ti) + "+" + str(laps) + ")"

input = Neuron(
        equations = """ r = """ + """g(t-Ti,intensite,laps,t-Duree-Ti+laps)""" ,
        functions = """ 
            g(a,b,c,d) = ((b/c)*a + abs(b/c*a)) / 2  - (b/c*(a-c) + abs( b/c*(a-c) )) / 2 - ( ((b/c)*d + abs(b/c*d)) / 2  - (b/c*(d-c) + abs( b/c*(d-c) )) / 2 )
        """
    )



POPinp = Population(geometry = 2, neuron = input, name='POPinp')


abc = Monitor(POPinp[1], 'r')


compile()
simulate(1000.0) # simulate for 1 second



r = abc.get('r')
plt.plot(dt()*np.arange(1000.0), r)
plt.show()
print(array(r))
