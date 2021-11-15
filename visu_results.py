from matplotlib import pyplot as plt
from matplotlib import image 
import numpy as np
import os as os 


#verification que les modeles sont les mêmes que le rBCBG
#...








#verification que la distorsion et l'efficacité ne varient pas selon le modèle 
strings = "eff","dist"
for string in strings:
    for i in range(2,10):
        plt.subplot(2,4,i-1)
        img = image.imread("log/channels_test/matrice_"+string+"%d" %i)
        plt.imshow(img)

    plt.show(block = True)
   
folder =os.listdir("log/channels_test")
for file in folder:
    if file[0:3] == 'eff':
        eff_dist = np.load('log/channels_test/' +file)
        print(eff_dist)





###### visualize le graphes eff_dist après avoir enlevé chaque connexion 
folder =os.listdir("log/Shapley_test")
eff,dist = [], []
for file in folder:
    if file[0:3] == 'eff':
        eff_dist = np.load('log/Shapley_test/' +file)
        eff.append(eff_dist[0])
        dist.append(eff_dist[1])
plt.plot( eff[:3] , dist[:3] , 'g+')
plt.plot( eff[3:7] , dist[3:7] , 'bo')
plt.plot( eff[7:12] , dist[7:12] , 'md' )
plt.plot( eff[12:14] , dist[12:14] , 'rD' )
plt.plot( eff[14:] , dist[14:] , 'c8' )
plt.show()

### **kwargs à comprendre ... .markersize() à reussir à utiliser...


#a = '1er arg :  %(az)s \n 2eme arg : %(ar)s \n fin de string' %{'az' : 999, 'ar' : 'bloublou'}
#print(a)