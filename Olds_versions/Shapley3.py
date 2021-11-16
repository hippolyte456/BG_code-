##################################### rewriting of rBCBG with ANNarchy simulator ############################################
#############################################################################################################################

################################################## REMARQUES GENERALES ######################################################
### pour le firing rate at rest... directement dans la def de r ... ?
### trouver le moyen de donner des nom qui change dans les boucles ?? sinon ne peut le faire sous forme de boucles... )
### je ne comprends pas pourquoi il faut recompiler à chaque fois ça n'a aucun seeeeens ! #en plus ça marche la 2eme mais pas la troisieme fois...

### la grosse fonction a 3 parties : def du model precompile (mettre des paramètres dedans, compilation, option de ce qu'on veut faire avec le modele( simul et visu, avec paramétrage aussi))
###donc on va creer des programmes differents pour 1ère partie et 2ème partie 


#utiliser les fonctions de comptage du temps d'execution pour preparer le run 
#test des matrices de distorsion/efficacité pour le modèle rBCBG initial (comparé 4 valeurs et 11 valeurs) -->peut-on extrapoler ?
#regarder le comportmeent des selections lorsqu'il y a 2 canaux / lorsqu'il y a 6 canaux --> peut-on réduire à 2 canaux sans soucis ? 
#vérifier que le temps d'intégration ne provoque pas les oscillations ? 
#test de Gurney 2001 pour verifier l'histeresis du modèle
#regarder comment sauvegarder les modeles pour les recharger et les modifier seuelemnt un peu ensuite... estce que ça va plus vite ? 


#quel modèle utilisé ?
#pourquoi il n'y a jamais du one two one EET du all to all ??? ça pourrait pas changé complétmeent la chose ? 
############################################     IMPORTATION MODULES         ################################################

from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt
import time as ti
import os as os 
from itertools import chain, combinations
############################################     CHOIX DE LA MODELISATION         ############################################

os.getcwd()
os.chdir('/home/hippo/Bureau/GB_Folders')

modelID = 1
models_param = loadtxt(open("compact_weights.csv","rb"),delimiter=";",skiprows=1)
model = models_param[modelID]

##################### DEFINITION / RECUPERATION PARAMETRES NECESSAIRES ... A PASSER AUX CLASSES d'ANNarchy #################### 
def creation_model(time = 1000.0, NbChannels = 3, perturb = [ [1,1,1], [1,1,1,1], [1,1,1,1,1], [1,1], [1,1,1,1,1] ], Shapley = False, channel_test = False ):


    

    clear()
    tau = Constant('tau', 5.0)

    sigma = 7*1e3			#microV
    sigmap = Constant('sigmap', (sigma * sqrt(3) / pi) )

    Smax_MSN = Constant('Smax_MSN', 300.0)
    Smax_STN = Constant('Smax_STN', 300.0)
    Smax_GPe = Constant('Smax_GPe', 400.0)
    Smax_GPiSNr = Constant('Smax_GPiSNr', 400.0)
    Smax_FSI = Constant('Smax_FSI', model[29])

    theta_MSN = Constant('theta_MSN', model[24]*1e3)
    theta_FSI = Constant('theta_FSI', model[25]*1e3)
    theta_STN = Constant('theta_STN', model[26]*1e3)
    theta_GPe = Constant('theta_GPe', model[27]*1e3)
    theta_GPiSNr = Constant('theta_GPiSNr', model[28]*1e3)

    W_CSN_MSN = model[0]   
    W_CSN_FSI = model[1]
    W_PTN_MSN = model[22]
    W_PTN_FSI = model[23]
    W_PTN_STN = model[2]
    W_MSN_GPe = model[3]
    W_MSN_GPiSNr = 0.82 *model[4]       # corrects an error: the probability of projection 0.82 was forgotten when generating compact_weights.csv
    W_MSN_MSN = model[16]/ NbChannels
    W_STN_GPe = model[5]/ NbChannels
    W_STN_GPiSNr = model[6]/ NbChannels
    W_STN_MSN = model[7]/ NbChannels
    W_STN_FSI = model[8]/ NbChannels
    W_GPe_STN = model[9]
    W_GPe_GPiSNr = model[10]/ NbChannels
    W_GPe_MSN = model[11]/ NbChannels
    W_GPe_FSI = model[12]/ NbChannels
    W_GPe_GPe = model[13]/ NbChannels
    W_FSI_MSN = model[14]/ NbChannels
    W_FSI_FSI = model[15]/ NbChannels
    W_CmPf_MSN = model[17]/ NbChannels
    W_CmPf_FSI = model[18]/ NbChannels
    W_CmPf_STN = model[19]/ NbChannels
    W_CmPf_GPe = model[20]/ NbChannels
    W_CmPf_GPiSNr = model[21]/ NbChannels

    latency  = {"dCSN_MSN" : 7 , "dCSN_FSI" : 7 , "dPTN_MSN" : 7 , "dPTN_FSI" : 7 , "dPTN_STN" : 3 , "dMSN_GPe" : 7 , "dMSN_GPiSNr" : 11 , "dMSN_MSN" : 0 , "dSTN_GPe" : 3 ,"dSTN_GPiSNr" : 3 , "dSTN_MSN" : 3 ,"dSTN_FSI" : 3 , "dGPe_STN" : 10 , "dGPe_GPiSNr" :3 , "dGPe_MSN" : 3 , "dGPe_FSI" : 3 , "dGPe_GPe" : 0 , "dFSI_MSN" : 0 , "dFSI_FSI" : 0 ,"dCmPf_MSN" : 0 , "dCmPf_FSI" : 0 ,"dCmPf_STN" : 0 ,"dCmPf_GPe" : 0 ,"dCmPf_GPiSNr" : 0 }


    #############################################     MODELE rBCBG AVEC ANNarchy        ############################################


    ##### NEURONES TYPES DU MODELE

    LeakyIntegratorNeuron_MSN = Neuron(               
                                                ### A TESTER : qu'est ce qu'on peut mettre dans ces strings ? les parametres sont à passer forcement avec la class "Constant" ? on peut les definir direct dedans ? on peut mettre des commentaires avec un # au sein de la string ? ...bref comprendre comment ça fonctionne ces strings...
                                                ### le exc se refère aux projections qui sont définies comme arrivant sur le neurone (et ses projections dépendent de la pop dans laquelle il a été mis)
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)               
            r = f_activateMSN(mp)                            
        """,
        functions = """
            f_activateMSN(x) = Smax_MSN / ( 1.0 + exp( (theta_MSN-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_FSI = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activateFSI(mp)                            
        """,
        functions = """
            f_activateFSI(x) = Smax_FSI / ( 1.0 + exp( (theta_FSI-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_GPe = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activateGPe(mp)                            
        """,
        functions = """
            f_activateGPe(x) = Smax_GPe / ( 1.0 + exp( (theta_GPe-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_STN = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activateSTN(mp)                            
        """,
        functions = """
            f_activateSTN(x) = Smax_STN / ( 1.0 + exp( (theta_STN-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_GPiSNr = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activateGPiSNr(mp)                            
        """,
        functions = """
            f_activateGPiSNr(x) = Smax_GPiSNr / ( 1.0 + exp( (theta_GPiSNr-x)/sigmap ) )
        """
    )

    
    input_CSN = Neuron(parameters="r=2")
    input_CSNstim = Neuron(parameters="r=2")
    input_PTN = Neuron(parameters="r=15")
    input_PTNstim = Neuron(parameters="r=15")
    input_CmPf = Neuron(parameters="r=4")

    ##### DEFINITION DES POPULATIONS 

    ### input ###    
    CSN = Population(name='CSN', geometry=NbChannels-1, neuron = input_CSN )
    PTN = Population(name='PTN', geometry=NbChannels-1, neuron = input_PTN )
    CSNstim = Population(name='CSNstim', geometry=1, neuron = input_CSNstim )
    PTNstim = Population(name='PTNstim', geometry=1, neuron = input_PTNstim )
    CmPf = Population(name='CMPf', geometry=NbChannels, neuron = input_CmPf )
     

    ### BG ###
    FSI = Population(name='FSI', geometry=NbChannels, neuron=LeakyIntegratorNeuron_FSI)
    MSN = Population(name='MSN', geometry=NbChannels, neuron=LeakyIntegratorNeuron_MSN)
    GPe = Population(name='GPe', geometry=NbChannels, neuron=LeakyIntegratorNeuron_GPe)
    GPiSNr = Population(name='GPiSNr', geometry=NbChannels, neuron=LeakyIntegratorNeuron_GPiSNr)
    STN = Population(name='STN', geometry=NbChannels, neuron=LeakyIntegratorNeuron_STN)

    ### output / thalamus ###
    

    ### DEFINITION DES SYNAPSES UTILISEES

    Basic = Synapse(parameters="""alpha = 1.0""")


    ### CREATION DES PROJECTIONS ENTRE LES POPULATIONS 

    proj_CSN_MSN = Projection(pre=CSN, post=MSN[1:NbChannels], target='exc', synapse=Basic).connect_one_to_one(weights= W_CSN_MSN , delays = latency['dCSN_MSN'])
    proj_CSN_FSI = Projection(pre=CSN, post=FSI[1:NbChannels], target='exc', synapse=Basic).connect_one_to_one(weights= W_CSN_FSI , delays = latency['dCSN_FSI'])
    proj_PTN_MSN = Projection(pre=PTN, post=MSN[1:NbChannels], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_MSN , delays = latency['dPTN_MSN'])
    proj_PTN_FSI = Projection(pre=PTN, post=FSI[1:NbChannels], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_FSI , delays = latency['dPTN_FSI'])
    proj_PTN_STN = Projection(pre=PTN, post=STN[1:NbChannels], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_STN , delays = latency['dPTN_STN'])
    proj_CSN_MSN_stim = Projection(pre=CSNstim, post=MSN[0], target='exc', synapse=Basic).connect_one_to_one(weights= W_CSN_MSN , delays = latency['dCSN_MSN'])
    proj_CSN_FSI_stim = Projection(pre=CSNstim, post=FSI[0], target='exc', synapse=Basic).connect_one_to_one(weights= W_CSN_FSI , delays = latency['dCSN_FSI'])
    proj_PTN_MSN_stim = Projection(pre=PTNstim, post=MSN[0], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_MSN , delays = latency['dPTN_MSN'])
    proj_PTN_FSI_stim = Projection(pre=PTNstim, post=FSI[0], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_FSI , delays = latency['dPTN_FSI'])
    proj_PTN_STN_stim = Projection(pre=PTNstim, post=STN[0], target='exc', synapse=Basic).connect_one_to_one(weights= W_PTN_STN , delays = latency['dPTN_STN'])

    if perturb[0][0] :
        proj_MSN_GPe = Projection(pre=MSN, post=GPe, target='inh', synapse=Basic).connect_one_to_one(weights= W_MSN_GPe , delays = latency['dMSN_GPe'])
    if perturb[0][1] :
        proj_MSN_GPiSNr = Projection(pre=MSN, post=GPiSNr, target='inh', synapse=Basic).connect_one_to_one(weights= W_MSN_GPiSNr , delays = latency['dMSN_GPiSNr'])
    if perturb[0][2] :
        proj_MSN_MSN = Projection(pre=MSN, post=MSN, target='inh', synapse=Basic).connect_all_to_all(weights = W_MSN_MSN , delays = latency['dMSN_MSN'], allow_self_connections=True) #attention il faut faire en sorte que la connexion se fasse sur tout le monde sauf le neurone qui envoie
    if perturb[1][0] :
        proj_STN_GPe = Projection(pre=STN, post=GPe, target='exc', synapse=Basic).connect_all_to_all(weights = W_STN_GPe , delays = latency['dSTN_GPe']) 
    if perturb[1][1] :   
        proj_STN_GPiSNr = Projection(pre=STN, post=GPiSNr, target='exc', synapse=Basic).connect_all_to_all(weights = W_STN_GPiSNr , delays = latency['dSTN_GPiSNr']) 
    if perturb[1][2] :   
        proj_STN_MSN = Projection(pre=STN, post=MSN, target='exc', synapse=Basic).connect_all_to_all(weights = W_STN_MSN , delays = latency['dSTN_MSN']) 
    if perturb[1][3] :    
        proj_STN_FSI = Projection(pre=STN, post=FSI, target='exc', synapse=Basic).connect_all_to_all(weights = W_STN_FSI , delays = latency['dSTN_FSI']) 
    if perturb[2][0] :    
        proj_GPe_STN = Projection(pre=GPe, post=STN, target='inh', synapse=Basic).connect_one_to_one(weights= W_GPe_STN , delays = latency['dGPe_STN'])
    if perturb[2][1] :    
        proj_GPe_GPiSNr = Projection(pre=GPe, post=GPiSNr, target='inh', synapse=Basic).connect_all_to_all(weights = W_GPe_GPiSNr , delays = latency['dGPe_GPiSNr']) 
    if perturb[2][2] :    
        proj_GPe_MSN = Projection(pre=GPe, post=MSN, target='inh', synapse=Basic).connect_all_to_all(weights = W_GPe_MSN , delays = latency['dGPe_MSN']) 
    if perturb[2][3] :    
        proj_GPe_FSI = Projection(pre=GPe, post=FSI, target='inh', synapse=Basic).connect_all_to_all(weights = W_GPe_FSI , delays = latency['dGPe_FSI']) 
    if perturb[2][4] :    
        proj_GPe_GPe = Projection(pre=GPe, post=GPe, target='inh', synapse=Basic).connect_all_to_all(weights = W_GPe_GPe , delays = latency['dGPe_GPe'], allow_self_connections=True)
    if perturb[3][0] :    
        proj_FSI_MSN = Projection(pre=FSI, post=MSN, target='inh', synapse=Basic).connect_all_to_all(weights = W_FSI_MSN, delays = latency['dFSI_MSN'])
    if perturb[3][1] :    
        proj_FSI_FSI = Projection(pre=FSI, post=FSI, target='inh', synapse=Basic).connect_all_to_all(weights = W_FSI_FSI, delays = latency['dFSI_FSI'], allow_self_connections=True)
    if perturb[4][0] :    
        proj_CmPf_MSN = Projection(pre=CmPf, post=MSN, target='exc', synapse=Basic).connect_all_to_all(weights = W_CmPf_MSN , delays = latency['dCmPf_MSN'])
    if perturb[4][1] :    
        proj_CmPf_FSI = Projection(pre=CmPf, post=FSI, target='exc', synapse=Basic).connect_all_to_all(weights = W_CmPf_FSI , delays = latency['dCmPf_FSI'])
    if perturb[4][2] :    
        proj_CmPf_STN = Projection(pre=CmPf, post=STN, target='exc', synapse=Basic).connect_all_to_all(weights = W_CmPf_STN , delays = latency['dCmPf_STN'])
    if perturb[4][3] :    
        proj_CmPf_GPe = Projection(pre=CmPf, post=GPe, target='exc', synapse=Basic).connect_all_to_all(weights = W_CmPf_GPe , delays = latency['dCmPf_GPe'])
    if perturb[4][4] :    
        proj_CmPf_GPiSNr = Projection(pre=CmPf, post=GPiSNr, target='exc', synapse=Basic).connect_all_to_all(weights = W_CmPf_GPiSNr , delays = latency['dCmPf_GPiSNr'])


    ##########################################################################################################################



    compile()

  


    CSN_levels = [2,4,6,8,10,12,14, 16, 18, 20]
    PTN_levels = [15,19,23,27,31, 34,37, 40,43, 46]
    n = len(CSN_levels)
    



    channels = [ 'mono%d' %i for i in range(1,NbChannels+1)]
    MSNmonitors, FSImonitors, STNmonitors, GPemonitors, GPiSNrmonitors, = {} , {} , {} , {} , {} 
    for idx,channel in enumerate(channels):
            MSNmonitors[channel] = Monitor(MSN[idx], 'r')
            FSImonitors[channel] = Monitor(FSI[idx], 'r')
            STNmonitors[channel] = Monitor(STN[idx], 'r')
            GPemonitors[channel] = Monitor(GPe[idx], 'r')
            GPiSNrmonitors[channel] = Monitor(GPiSNr[idx], 'r')
    
    CSN_order = [CSN_levels[i] for i in range(n) for k in range(n-i) ]         
    CSN_order_stim = [CSN_levels[i] for k in range(n) for i in range(k,n)]
    PTN_order = [PTN_levels[i] for i in range(n) for k in range(n-i) ]
    PTN_order_stim = [PTN_levels[i] for k in range(n) for i in range(k,n)]
    CSNsaliences = [(CSN_order[i],CSN_order_stim[i]) for i in range(len(CSN_order_stim))]
    PTNsaliences = [(PTN_order[i],PTN_order_stim[i]) for i in range(len(CSN_order_stim))]

    nb_stim = len(CSNsaliences)
    all_time = time * nb_stim
    

    for i in range(nb_stim):
        CSN.r = CSNsaliences[i][0]
        PTN.r = PTNsaliences[i][0]
        CSNstim.r = CSNsaliences[i][1]
        PTNstim.r = PTNsaliences[i][1]

        simulate(all_time / nb_stim)

    

    rGPi = view_all_firing_rate(NbChannels, MSNmonitors, STNmonitors,FSImonitors,GPemonitors,GPiSNrmonitors, all_time, Shapley = Shapley)
    eff , dist, list_eff, list_dist = calcul_eff_dist(rGPi[0], rGPi[1],nb_stim)
    if not Shapley :
        view_matrix_eff_dist(list_eff,list_dist,n, NbChannels)

    if channel_test:
        np.save('log/channels_test/eff_dist_%d_channels'%NbChannels, [eff,dist])
    if Shapley:
        np.save('log/Shapley_test/eff_dist_' +str(perturb), [eff,dist])
   
   
    return(eff,dist)

    

    ####################################### VISUALISATION DU MODELE ##########################################################



def view_all_firing_rate(NbChannels, MSNmonitors, STNmonitors,FSImonitors,GPemonitors,GPiSNrmonitors, all_time, Shapley = False):
    f,axs = plt.subplots(nrows=5 , ncols= NbChannels , sharey='row')
    for idx,monitor in enumerate(MSNmonitors):
        r = MSNmonitors[monitor].get('r')
        axs[0,idx].plot(dt()*np.arange(all_time), r) 
        axs[0,idx].title.set_text('Channels')
    for idx,monitor in enumerate(FSImonitors):
        r = FSImonitors[monitor].get('r')
        axs[1,idx].plot(dt()*np.arange(all_time), r) 
    for idx,monitor in enumerate(STNmonitors):
        r = STNmonitors[monitor].get('r')
        axs[2,idx].plot(dt()*np.arange(all_time), r) 
    for idx,monitor in enumerate(GPemonitors):
        r = GPemonitors[monitor].get('r')
        axs[3,idx].plot(dt()*np.arange(all_time), r) 

    rGPi = []
    for idx,monitor in enumerate(GPiSNrmonitors):
        r = GPiSNrmonitors[monitor].get('r')
        axs[4,idx].plot(dt()*np.arange(all_time), r)
        if idx <= 1:
            rGPi.append(r)
    if not Shapley:
        plt.show()
    return(rGPi)



def calcul_eff_dist(firing_rate,firing_rate_stim,nb_stim):
    subarrays, subarrays_stim = {} , {}
    for i in range(nb_stim): 
        subarrays['%d'%i] = firing_rate[int('%d250'%i) : int('%d750'%i)]         
        subarrays_stim['%d'%i] = firing_rate_stim[int('%d250'%i) : int('%d750'%i)]

    rGPi_rest = mean(subarrays['1'])
    efficacity, distortion = [],[]
    for i in range(nb_stim):
        rGPi = mean(subarrays['%d'%i])
        rGPi_stim = mean(subarrays_stim['%d'%i])
        eff1 = max(0, 1 - rGPi / rGPi_rest)
        eff2 = max(0, 1 - rGPi_stim / rGPi_rest)
        eff = max( eff1, eff2)
        dist = 1 - abs( eff1 - eff2 ) / (eff+0.00000001)
        efficacity.append(eff)
        distortion.append(dist)
    
    value_efficacity = mean(efficacity)
    value_distortion = mean(distortion)
    #tot_selection_value = mean(np.array(1-value_distortion,value_efficacity))   #à normaliser
    return (value_efficacity,value_distortion,efficacity,distortion)



def view_matrix_eff_dist(list_eff,list_dist, n, NbChannels):
    
    matrix_eff = np.matrix( [ [ 0 for k in range(j) ]  +  [list_eff[ int(sum([((n) - k) for k in range(j)]) ) + l ] for l in range(n - j) ]   for j in range(n) ] )
    matrix_dist = np.matrix( [ [ 0 for k in range(j) ]  +  [list_dist[ int(sum([((n) - k) for k in range(j)]) ) + l ] for l in range(n - j) ]   for j in range(n) ] )
    #matrix_eff = np.matrix([[list_eff[i] for i in range(5)],[list_eff[5 + i] for i in range(4)] + [0] , [list_eff[5+4 + i] for i in range(3)] + [0,0], [list_eff[5+4+3 + i] for i in range(2)] + [0,0,0], [list_eff[5+4+3+2 + i] for i in range(1)] + [0,0,0,0]])
    #matrix_dist = np.matrix([[list_dist[i] for i in range(5)],[list_dist[5 + i] for i in range(4)] + [0] , [list_dist[5+4 + i] for i in range(3)] + [0,0], [list_dist[5+4+3 + i] for i in range(2)] + [0,0,0], [list_dist[5+4+3+2 + i] for i in range(1)] + [0,0,0,0]])
    plt.subplot(121)
    plt.imshow(matrix_eff)
    plt.subplot(122)
    plt.imshow(matrix_dist)
    #plt.show()

    plt.imsave(fname = "log/channels_test/matrice_eff%d" %NbChannels, arr = matrix_eff, format = 'png' )
    plt.imsave(fname = "log/channels_test/matrice_dist%d" %NbChannels, arr = matrix_dist, format = 'png' )



def nucleus_Shapley_test(time = 1000.0, NbChannels = 6, perturb = [ [1,1,1], [1,1,1,1], [1,1,1,1,1], [1,1], [1,1,1,1,1] ]):
    perturbation = perturb
    leff,ldist = [],[]
    eff,dist = creation_model(time , NbChannels , perturb = perturbation)
    leff.append(eff)
    ldist.append(dist)
    for i in range(5):
        for j in perturbation[i]:
            perturbation[i][j] = 0

        eff,dist = creation_model(time , NbChannels , perturb = perturbation)
        leff.append(eff)
        ldist.append(dist)
        perturbation = perturb
    return(leff,ldist)



def Shapley_test():
    perturbation = [ [1,1,1], [1,1,1,1], [1,1,1,1,1], [1,1], [1,1,1,1,1] ]
    for nucleus in range(2,len(perturbation)):
        for projection in range(len(perturbation[nucleus])):
            perturbation[nucleus][projection] = 0 
            creation_model(perturb = perturbation, Shapley = True)
            perturbation[nucleus][projection] = 1
            


def channels_test():
    for i in range(2,10):
        eff, dist = creation_model(NbChannels = i)
        




# faire des sous ensembles de projections et regarder qu'est-ce qui sert à quoi (pas long) //// tester l'ensemble des connexions en même temps (long )
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1))
            





list(powerset([0,1,2,3,4]))

nucleus_Shapley_test()

creation_model()

Shapley_test()







#plt.imsave(fname = "log/matrice_dist%d" %5, arr = np.array([[0,1,0],[1,0,0]]), format = 'png' )


#[(2,2) , (2,8) , (2,14) , (2,20) , (8,8) , (8,14) , (8,20) , (14,14) , (14,20) , (20,20)]
#[(15,15) , (15,25) , (15,35) , (15,46) , (25,25) , (25,35) , (25,46) , (35,35) , (35,46) , (46,46)]


#r = GPiSNrmonitors['mono1'].get('r')
    #axs[4,0].plot(dt()*np.arange(all_time), r) 
    #rstim = GPiSNrmonitors['mono2'].get('r')
    #axs[4,1].plot(dt()*np.arange(all_time), rstim)
    #rstimbis = GPiSNrmonitors['mono3'].get('r')
    #axs[4,2].plot(dt()*np.arange(all_time), rstimbis)
    #eff , dist = calcul_eff_dist(r , rstim] 


file= open('log/BG_'+str(modelID)+'.py','w')		
file.write('# model ; ' + '\n' + '# NbChannels ; '+ str(6)+ '\n')
file.writelines(', '.join([str(i) for i in range(10)]) +', ')
file.close()



np.load('log/example_log.npy')



dir = os.path.join("log","channels_test")
if not os.path.exists(dir):
    os.mkdir(dir)