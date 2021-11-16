
from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt
import time as ti
import os as os 


intensite = Constant('intensite',5)
Duree = Constant('Duree', 800)
Ti = Constant('Ti',200)
laps = Constant('laps', 200)


input = Neuron(
        equations = """
            r = g(t-Ti,intensite,laps) - g(t-Duree-Ti+laps,intensite,laps)                              
        """,
        functions = """ 
            g(a,b,c) = ((b/c)*a + abs(b/c*a)) / 2  - (b/c*(a-c) + abs( b/c*(a-c) )) / 2
        """
    )

#g(t,pente,laps) = ((pente/laps)*t + abs(pente/laps*t)) / 2   - ((pente/laps)*(t-laps) + abs((pente/laps*(t-laps))) / 2
#
# f(t,a) = (a*t + abs(a*t)) / 2 
# g(t,pente,laps) = f(t,pente/laps) - f(t-laps,pente/laps) 
# stimulus(t,intensite,Duree,Ti,laps) = g(t-Ti,intensite,laps) - g(t-Duree-Ti+laps,intensite,laps)


POPinp = Population(geometry = 2, neuron = input, name='POPinp')


abc = Monitor(POPinp[1], 'r')


compile()
simulate(1000.0) # simulate for 1 second



r = abc.get('r')
plt.plot(dt()*np.arange(1000.0), r)
plt.show()
print(array(r))




















