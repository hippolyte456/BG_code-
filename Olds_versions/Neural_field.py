
from ANNarchy import *
clear()


InputNeuron = Neuron(   
    parameters="""
        baseline = 0.0
    """,
    equations="""
        r = pos(baseline + Uniform(-0.5, 0.5))
    """ 
)


NeuralFieldNeuron = Neuron(
    parameters=""" 
        tau = 10.0 : population
    """,
    equations="""
        tau * dr/dt + r = sum(exc) + sum(inh) + Uniform(-0.5, 0.5) : min=0.0, max=1.0
    """
)


N = 20
inp = Population(geometry = (N, N), neuron = InputNeuron, name='Input')
focus = Population(geometry = (N, N), neuron = NeuralFieldNeuron, name='Focus')

ff = Projection(pre=inp, post=focus, target='exc')
ff.connect_one_to_one(weights=1.0, delays = 20.0)

lat = Projection(pre=focus, post=focus, target='inh')
lat.connect_dog(amp_pos=0.2, sigma_pos=0.1, amp_neg=0.1, sigma_neg=0.7)

compile()

simulate(1000.0)


import matplotlib.pyplot as plt

plt.figure(figsize=(15, 10))
plt.subplot(221)
plt.imshow(inp.r, interpolation='nearest', cmap=plt.cm.gray)
plt.subplot(224)
plt.imshow(focus.r, interpolation='nearest', cmap=plt.cm.gray)
plt.show()
