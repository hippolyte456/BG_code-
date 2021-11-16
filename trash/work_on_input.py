# on veut creer une fonction qui renvoie des chaines de caractere à mettre dans le firing rate 
#(tester les delays aussi)
# 
# input_CSN = Neuron(parameters="r=2")


from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt
import time as ti
import os as os 

########ou est-ce qu'il faut definir une fonction pour qu'elle soit reconnue par ANNarchy quand on l'appelle dans les chaines de caractères lors de la definition des neurones ? 

#les fonctions utilisables sur quel temps ? quel concaténation 
#puis on duplique à n channels avec differentes modalités sur les n 
#integrer ces fonctions aux neurones


def stringify_formula(variable):

    string = "exp(" + variable + ")"
    return( string )
    input_CSNstim = Neuron(parameters="r=2")
    input_PTN = Neuron(parameters="r=15")
    input_PTNstim = Neuron(parameters="r=15")
    input_CmPf = Neuron(parameters="r=4")


#stringify_formula = " f(x) "



def f(t,a):
    return (a*t + abs(a*t)) / 2 

def g(t,pente,laps):
    return  f(t,pente/laps) - f(t-laps,pente/laps) 

def stimulus(t,intensite,Duree,Ti,laps):
    return g(t-Ti,intensite,laps) - g(t-Duree-Ti+laps,intensite,laps)





def stimuli(t,L):
    exc = 0
    for stim in L:
        exc += sum(stimulus(t,stim[0],stim[1],stim[2],stim[3]))
    return exc










if __name__ == '__main__':
    steps = 10000
    T = linspace(0, 10, steps)
    Y = [ stimuli( T[i], [[2,5,2,1],[4,3,4.5,1]] )       for i in range(steps)]
    #Y = [ stimulus(T[i], intensite = 2, Duree = 6.5, Ti = 2, laps = 1) for i in range(steps)]
    #Y = [ g(X[i],3) for i in range(steps)]
    plt.plot(T,Y)                         #comment on scale comme ylim ? (tout le temps le même)
    plt.show()
    


















