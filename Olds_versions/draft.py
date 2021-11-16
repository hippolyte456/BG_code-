##################################### rewriting of rBCBG with ANNarchy simulator ############################################
#############################################################################################################################

################################################## REMARQUES GENERALES ######################################################
### pour le firing rate at rest... directement dans la def de r ... ?
### trouver le moyen de donner des nom qui change dans les boucles ?? sinon ne peut le faire sous forme de boucles... )
### je ne comprends pas pourquoi il faut recompiler à chaque fois ça n'a aucun seeeeens ! #en plus ça marche la 2eme mais pas la troisieme fois...

############################################     IMPORTATION MODULES         ################################################

from ANNarchy import *
clear()
from connexweights import * #pas besoin 
from math import * 
from numpy import *
import matplotlib.pyplot as plt

############################################     CHOIX DE LA MODELISATION         ############################################

modelID = 1 ### choisir un nombre entre 0 et 12 
NbChannels = 3 ### attention si plus de 9 à l'affichage...
                 
models_param = loadtxt(open("compact_weights.csv","rb"),delimiter=";",skiprows=1)
model = models_param[modelID]


##################### DEFINITION / RECUPERATION PARAMETRES NECESSAIRES ... A PASSER AUX CLASSES d'ANNarchy #################### 
def creation_model(time = 1000.0 ,input = 1):
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

    CSN_input = Constant('CSN_input', 2)
    PTN_input = Constant('PTN_input', 15)
    CmPf_input = Constant('CmPf_input', 4)

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
            r = f_activate(mp)                            
        """,
        functions = """
            f_activate(x) = Smax_MSN / ( 1.0 + exp( (theta_MSN-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_FSI = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activate(mp)                            
        """,
        functions = """
            f_activate(x) = Smax_FSI / ( 1.0 + exp( (theta_FSI-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_GPe = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activate(mp)                            
        """,
        functions = """
            f_activate(x) = Smax_GPe / ( 1.0 + exp( (theta_GPe-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_STN = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activate(mp)                            
        """,
        functions = """
            f_activate(x) = Smax_STN / ( 1.0 + exp( (theta_STN-x)/sigmap ) )
        """
    )

    LeakyIntegratorNeuron_GPiSNr = Neuron(              
                                                
        parameters = """
            tau = tau 
        """,
        equations = """
            tau * dmp/dt  + mp = sum(exc) - sum(inh)
            r = f_activate(mp)                            
        """,
        functions = """
            f_activate(x) = Smax_GPiSNr / ( 1.0 + exp( (theta_GPiSNr-x)/sigmap ) )
        """
    )

    if input == 1 : 
        input_CSN = Neuron(parameters="r=CSN_input")
        input_PTN = Neuron(parameters="r=PTN_input")
        input_CmPf = Neuron(parameters="r=CmPf_input")
        

    if input == 2:
        input_CSN = Neuron(
            equations ="""
            r = Uniform(-0.5, 0.5)
            """
        )
        
        input_PTN = Neuron(parameters="r=PTN_input")
        input_CmPf = Neuron(parameters="r=CmPf_input")
       

    ##### DEFINITION DES POPULATIONS 

    ### input ###
    CSN = Population(name='CSN', geometry=NbChannels, neuron = input_CSN )
    PTN = Population(name='PTN', geometry=NbChannels, neuron = input_PTN )
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

    proj_CSN_MSN = Projection(pre=CSN, post=MSN, target='exc', synapse=Basic) 
    proj_CSN_FSI = Projection(pre=CSN, post=FSI, target='exc', synapse=Basic)
    proj_PTN_MSN = Projection(pre=PTN, post=MSN, target='exc', synapse=Basic)
    proj_PTN_FSI = Projection(pre=PTN, post=FSI, target='exc', synapse=Basic)
    proj_PTN_STN = Projection(pre=PTN, post=STN, target='exc', synapse=Basic)
    proj_MSN_GPe = Projection(pre=MSN, post=GPe, target='inh', synapse=Basic)
    proj_MSN_GPiSNr = Projection(pre=MSN, post=GPiSNr, target='inh', synapse=Basic)
    proj_MSN_MSN = Projection(pre=MSN, post=MSN, target='inh', synapse=Basic)
    proj_STN_GPe = Projection(pre=STN, post=GPe, target='exc', synapse=Basic)
    proj_STN_GPiSNr = Projection(pre=STN, post=GPiSNr, target='exc', synapse=Basic)
    proj_STN_MSN = Projection(pre=STN, post=MSN, target='exc', synapse=Basic)
    proj_STN_FSI = Projection(pre=STN, post=FSI, target='exc', synapse=Basic)
    proj_GPe_STN = Projection(pre=GPe, post=STN, target='inh', synapse=Basic)
    proj_GPe_GPiSNr = Projection(pre=GPe, post=GPiSNr, target='inh', synapse=Basic)
    proj_GPe_MSN = Projection(pre=GPe, post=MSN, target='inh', synapse=Basic)
    proj_GPe_FSI = Projection(pre=GPe, post=FSI, target='inh', synapse=Basic)
    proj_GPe_GPe = Projection(pre=GPe, post=GPe, target='inh', synapse=Basic)
    proj_FSI_MSN = Projection(pre=FSI, post=MSN, target='inh', synapse=Basic)
    proj_FSI_FSI = Projection(pre=FSI, post=FSI, target='inh', synapse=Basic)
    proj_CmPf_MSN = Projection(pre=CmPf, post=MSN, target='exc', synapse=Basic)
    proj_CmPf_FSI = Projection(pre=CmPf, post=FSI, target='exc', synapse=Basic)
    proj_CmPf_STN = Projection(pre=CmPf, post=STN, target='exc', synapse=Basic)
    proj_CmPf_GPe = Projection(pre=CmPf, post=GPe, target='exc', synapse=Basic)
    proj_CmPf_GPiSNr = Projection(pre=CmPf, post=GPiSNr, target='exc', synapse=Basic)

    proj_CSN_MSN.connect_one_to_one(weights= W_CSN_MSN , delays = latency['dCSN_MSN'])
    proj_CSN_FSI.connect_one_to_one(weights= W_CSN_FSI , delays = latency['dCSN_FSI'])
    proj_PTN_MSN.connect_one_to_one(weights= W_PTN_MSN , delays = latency['dPTN_MSN'])
    proj_PTN_FSI.connect_one_to_one(weights= W_PTN_FSI , delays = latency['dPTN_FSI'])
    proj_PTN_STN.connect_one_to_one(weights= W_PTN_STN , delays = latency['dPTN_STN'])
    proj_MSN_GPe.connect_one_to_one(weights= W_MSN_GPe , delays = latency['dMSN_GPe'])
    proj_MSN_GPiSNr.connect_one_to_one(weights= W_MSN_GPiSNr , delays = latency['dMSN_GPiSNr'])
    proj_MSN_MSN.connect_all_to_all(weights = W_MSN_MSN , delays = latency['dMSN_MSN'], allow_self_connections=True) #attention il faut faire en sorte que la connexion se fasse sur tout le monde sauf le neurone qui envoie
    proj_STN_GPe.connect_all_to_all(weights = W_STN_GPe , delays = latency['dSTN_GPe']) 
    proj_STN_GPiSNr.connect_all_to_all(weights = W_STN_GPiSNr , delays = latency['dSTN_GPiSNr']) 
    proj_STN_MSN.connect_all_to_all(weights = W_STN_MSN , delays = latency['dSTN_MSN']) 
    proj_STN_FSI.connect_all_to_all(weights = W_STN_FSI , delays = latency['dSTN_FSI']) 
    proj_GPe_STN.connect_one_to_one(weights= W_GPe_STN , delays = latency['dGPe_STN'])
    proj_GPe_GPiSNr.connect_all_to_all(weights = W_GPe_GPiSNr , delays = latency['dGPe_GPiSNr']) 
    proj_GPe_MSN.connect_all_to_all(weights = W_GPe_MSN , delays = latency['dGPe_MSN']) 
    proj_GPe_FSI.connect_all_to_all(weights = W_GPe_FSI , delays = latency['dGPe_FSI']) 
    proj_GPe_GPe.connect_all_to_all(weights = W_GPe_GPe , delays = latency['dGPe_GPe'], allow_self_connections=True) 
    proj_FSI_MSN.connect_all_to_all(weights = W_FSI_MSN, delays = latency['dFSI_MSN'])
    proj_FSI_FSI.connect_all_to_all(weights = W_FSI_FSI, delays = latency['dFSI_FSI'], allow_self_connections=True)
    proj_CmPf_MSN.connect_all_to_all(weights = W_CmPf_MSN , delays = latency['dCmPf_MSN'])
    proj_CmPf_FSI.connect_all_to_all(weights = W_CmPf_FSI , delays = latency['dCmPf_FSI'])
    proj_CmPf_STN.connect_all_to_all(weights = W_CmPf_STN , delays = latency['dCmPf_STN'])
    proj_CmPf_GPe.connect_all_to_all(weights = W_CmPf_GPe , delays = latency['dCmPf_GPe'])
    proj_CmPf_GPiSNr.connect_all_to_all(weights = W_CmPf_GPiSNr , delays = latency['dCmPf_GPiSNr'])

    ##########################################################################################################################

    compile()
    visu_all_Channels(time)

    ####################################### VISUALISATION DU MODELE ##########################################################


def mean_firing_rate(time):
    mGPe = Monitor(GPe, 'r')
    mGPiSNr = Monitor(GPiSNr, 'r')
    mSTN = Monitor(STN, 'r')
    mFSI = Monitor(FSI, 'r')
    mMSN= Monitor(MSN, 'r')
    simulate(time)
    rGPe = mGPe.get('r')
    rGPiSNr = mGPiSNr.get('r')
    rSTN = mSTN.get('r')
    rFSI = mFSI.get('r')
    rMSN= mMSN.get('r')
    plt.subplot(151)
    plt.plot(dt()*np.arange(time), rGPe )
    plt.title('GPe')
    plt.subplot(152)
    plt.plot(dt()*np.arange(time), rGPiSNr)
    plt.title('GPiSNr')
    plt.subplot(153)
    plt.plot(dt()*np.arange(time), rSTN)
    plt.title('STN')
    plt.subplot(154)
    plt.plot(dt()*np.arange(time), rFSI)
    plt.title('FSI')
    plt.subplot(155)
    plt.plot(dt()*np.arange(time), rMSN)
    plt.title('MSN')
    plt.show()

def visu_all_Channels(time):

    channels = [ 'mono%d' %i for i in range(1,NbChannels+1)]
    MSNmonitors, FSImonitors, STNmonitors, GPemonitors, GPiSNrmonitors, = {} , {} , {} , {} , {} 
    for idx,channel in enumerate(channels):
            MSNmonitors[channel] = Monitor(MSN[idx], 'r')
            FSImonitors[channel] = Monitor(FSI[idx], 'r')
            STNmonitors[channel] = Monitor(STN[idx], 'r')
            GPemonitors[channel] = Monitor(GPe[idx], 'r')
            GPiSNrmonitors[channel] = Monitor(GPiSNr[idx], 'r')
    simulate(time)
    for idx,monitor in enumerate(MSNmonitors):
        r = MSNmonitors[monitor].get('r')
        plt.subplot(5 , NbChannels , idx+1)
        plt.plot(dt()*np.arange(time), r )
    for idx,monitor in enumerate(FSImonitors):
        r = FSImonitors[monitor].get('r')
        plt.subplot(5 , NbChannels , NbChannels + idx + 1)
        plt.plot(dt()*np.arange(time), r )
    plt.show()




creation_model(2)

########################## changement d'input #################################



################################################################################









### to use ###

#GPe.attributes

#save_parameters('network.json')
#load_parameters('network.json')





####### Etude de la selection faite par le modèle (valeur de Shapley) #######




#### mauvaise pratique ####
tab=["a","b","c"]
for idx,i in enumerate(tab):
  globals()["nom_var_%s"%i]=idx
#print(nom_var_a, nom_var_b, nom_var_c)


#### bonne pratique ###  
nuclei = ["a", "b", "c"]
nb_neurones = [5, 10, 15]
pops = {}
for i,noyau in enumerate(nuclei) : 
    pops[noyau] = nb_neurones[i]




def compile_simul_visu(type_of_monitoring, ):
    return 'oohh'

def simul_visu(simul_type,visu_type):
    return 'oohh'

def visu(visu_type):
    return 'oohh'




#for idx,monitor in enumerate(FSImonitors):
 #       r = FSImonitors[monitor].get('r')
  #      x = int('5'+'%d'%NbChannels + '%d'%(9+idx+1))
   #     plt.subplot(x)
    #    plt.plot(dt()*np.arange(time), r )



