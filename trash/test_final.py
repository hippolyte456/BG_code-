from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt
import time as ti
import os as os 



#stimulus est défini par son intensite puis sa duree puis son Temps initial puis le laps de temps qu'il faut pour arriver son maximum    
stimuli = [[5,400,200,50],[8,200,600,20],[3,800,100,20],[3,500,250,20]]
stringified_stimuli = ""
for stimulus in stimuli :
    stringified_stimulus = "g(t-" + str(stimulus[2]) + "," + str(stimulus[0]) +","+ str(stimulus[3]) + ",t-" + str(stimulus[1]) + "-" + str(stimulus[2]) + "+" + str(stimulus[3]) + ")"
    stringified_stimuli = stringified_stimuli + "+" + stringified_stimulus
print(stringified_stimuli)



input = Neuron(
        equations = """ r = """ + stringified_stimuli ,
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

