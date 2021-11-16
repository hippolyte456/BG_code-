from ANNarchy import *
clear()
#setup(paradigm="cuda")



tau = Constant("blush",1000)

InputNeuron = Neuron(
    parameters=""" 
        tau = blush
    """,
    equations = """
        r = blush * Uniform(-0.5, 0.5)  * t                     
    """,
    functions = """ 
    
        """
)
# f(t,a) = (a*t + abs(a*t)) / 2 
#     g(t,pente,laps) = f(t,pente/laps) - f(t-laps,pente/laps) 
#     stimulus(t,intensite,Duree,Ti,laps) = g(t-Ti,intensite,laps) - g(t-Duree-Ti+laps,intensite,laps)
        

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
simulate(1000.0) # simulate for 1 second


import matplotlib.pyplot as plt

plt.figure(figsize=(15, 10))
plt.subplot(121)
plt.imshow(inp.r, interpolation='nearest', cmap=plt.cm.gray)
plt.subplot(122)
plt.imshow(focus.r, interpolation='nearest', cmap=plt.cm.gray)
plt.show()


inp.r