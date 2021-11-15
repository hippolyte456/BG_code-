
#include "ANNarchy.h"



/*
 * Internal data
 *
 */
double dt;
long int t;
std::vector<std::mt19937> rng;

// Custom constants

double tau_MSN;
void set_tau_MSN(double value){tau_MSN = value;};
double tau_FSI;
void set_tau_FSI(double value){tau_FSI = value;};
double tau_STN;
void set_tau_STN(double value){tau_STN = value;};
double tau_GPe;
void set_tau_GPe(double value){tau_GPe = value;};
double tau_GPiSNr;
void set_tau_GPiSNr(double value){tau_GPiSNr = value;};
double sigmap;
void set_sigmap(double value){sigmap = value;};
double Smax_MSN;
void set_Smax_MSN(double value){Smax_MSN = value;};
double Smax_STN;
void set_Smax_STN(double value){Smax_STN = value;};
double Smax_GPe;
void set_Smax_GPe(double value){Smax_GPe = value;};
double Smax_GPiSNr;
void set_Smax_GPiSNr(double value){Smax_GPiSNr = value;};
double Smax_FSI;
void set_Smax_FSI(double value){Smax_FSI = value;};
double theta_MSN;
void set_theta_MSN(double value){theta_MSN = value;};
double theta_FSI;
void set_theta_FSI(double value){theta_FSI = value;};
double theta_STN;
void set_theta_STN(double value){theta_STN = value;};
double theta_GPe;
void set_theta_GPe(double value){theta_GPe = value;};
double theta_GPiSNr;
void set_theta_GPiSNr(double value){theta_GPiSNr = value;};

// Populations
PopStruct0 pop0;
PopStruct1 pop1;
PopStruct2 pop2;
PopStruct3 pop3;
PopStruct4 pop4;
PopStruct5 pop5;
PopStruct6 pop6;
PopStruct7 pop7;
PopStruct8 pop8;
PopStruct9 pop9;


// Projections
ProjStruct0 proj0;
ProjStruct1 proj1;
ProjStruct2 proj2;
ProjStruct3 proj3;
ProjStruct4 proj4;
ProjStruct5 proj5;
ProjStruct6 proj6;
ProjStruct7 proj7;
ProjStruct8 proj8;
ProjStruct9 proj9;
ProjStruct10 proj10;
ProjStruct11 proj11;
ProjStruct12 proj12;
ProjStruct13 proj13;
ProjStruct14 proj14;
ProjStruct15 proj15;
ProjStruct16 proj16;
ProjStruct17 proj17;
ProjStruct18 proj18;
ProjStruct19 proj19;
ProjStruct20 proj20;
ProjStruct21 proj21;
ProjStruct22 proj22;
ProjStruct23 proj23;
ProjStruct24 proj24;
ProjStruct25 proj25;
ProjStruct26 proj26;
ProjStruct27 proj27;
ProjStruct28 proj28;


// Global operations


// Recorders
std::vector<Monitor*> recorders;
int addRecorder(Monitor* recorder){
    int found = -1;

    for (unsigned int i=0; i<recorders.size(); i++) {
        if (recorders[i] == nullptr) {
            found = i;
            break;
        }
    }

    if (found != -1) {
        // fill a previously cleared slot
        recorders[found] = recorder;
        return found;
    } else {
        recorders.push_back(recorder);
        return recorders.size() - 1;
    }
}
Monitor* getRecorder(int id) {
    if (id < recorders.size())
        return recorders[id];
    else
        return nullptr;
}
void removeRecorder(Monitor* recorder){
    for (unsigned int i=0; i<recorders.size(); i++){
        if(recorders[i] == recorder){
            recorders[i] = nullptr;
            break;
        }
    }
}

void singleStep(); // Function prototype

// Simulate the network for the given number of steps,
// called from python
void run(int nbSteps) {
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Perform simulation for " << nbSteps << " steps." << std::endl;
#endif

    for(int i=0; i<nbSteps; i++) {
        singleStep();
    }

}

// Simulate the network for a single steps,
// called from python
void step() {

    singleStep();

}

int run_until(int steps, std::vector<int> populations, bool or_and)
{


    run(steps);
    return steps;


}

// Initialize the internal data and the random numbers generator
void initialize(double _dt) {


    // Internal variables
    dt = _dt;
    t = (long int)(0);

    // Populations
    // Initialize populations
    pop0.init_population();
    pop1.init_population();
    pop2.init_population();
    pop3.init_population();
    pop4.init_population();
    pop5.init_population();
    pop6.init_population();
    pop7.init_population();
    pop8.init_population();
    pop9.init_population();


    // Projections
    // Initialize projections
    proj0.init_projection();
    proj1.init_projection();
    proj2.init_projection();
    proj3.init_projection();
    proj4.init_projection();
    proj5.init_projection();
    proj6.init_projection();
    proj7.init_projection();
    proj8.init_projection();
    proj9.init_projection();
    proj10.init_projection();
    proj11.init_projection();
    proj12.init_projection();
    proj13.init_projection();
    proj14.init_projection();
    proj15.init_projection();
    proj16.init_projection();
    proj17.init_projection();
    proj18.init_projection();
    proj19.init_projection();
    proj20.init_projection();
    proj21.init_projection();
    proj22.init_projection();
    proj23.init_projection();
    proj24.init_projection();
    proj25.init_projection();
    proj26.init_projection();
    proj27.init_projection();
    proj28.init_projection();


    // Custom constants

        tau_MSN = 0.0;
        tau_FSI = 0.0;
        tau_STN = 0.0;
        tau_GPe = 0.0;
        tau_GPiSNr = 0.0;
        sigmap = 0.0;
        Smax_MSN = 0.0;
        Smax_STN = 0.0;
        Smax_GPe = 0.0;
        Smax_GPiSNr = 0.0;
        Smax_FSI = 0.0;
        theta_MSN = 0.0;
        theta_FSI = 0.0;
        theta_STN = 0.0;
        theta_GPe = 0.0;
        theta_GPiSNr = 0.0;

}

// Initialize the random distribution objects
void init_rng_dist() {
pop0.init_rng_dist();
pop1.init_rng_dist();
pop2.init_rng_dist();
pop3.init_rng_dist();
pop4.init_rng_dist();
pop5.init_rng_dist();
pop6.init_rng_dist();
pop7.init_rng_dist();
pop8.init_rng_dist();
pop9.init_rng_dist();

}

// Change the seed of the RNG
void setSeed(long int seed, int num_sources, bool use_seed_seq){
    rng.clear();

    rng.push_back(std::mt19937(seed));

    rng.shrink_to_fit();
}

// Step method. Generated by ANNarchy.
void singleStep()
{


    ////////////////////////////////
    // Presynaptic events
    ////////////////////////////////


    // pop5: FSI
    if (pop5._active)
        memset( pop5._sum_exc.data(), 0.0, pop5._sum_exc.size() * sizeof(double));

    // pop5: FSI
    if (pop5._active)
        memset( pop5._sum_inh.data(), 0.0, pop5._sum_inh.size() * sizeof(double));

    // pop6: MSN
    if (pop6._active)
        memset( pop6._sum_exc.data(), 0.0, pop6._sum_exc.size() * sizeof(double));

    // pop6: MSN
    if (pop6._active)
        memset( pop6._sum_inh.data(), 0.0, pop6._sum_inh.size() * sizeof(double));

    // pop7: GPe
    if (pop7._active)
        memset( pop7._sum_exc.data(), 0.0, pop7._sum_exc.size() * sizeof(double));

    // pop7: GPe
    if (pop7._active)
        memset( pop7._sum_inh.data(), 0.0, pop7._sum_inh.size() * sizeof(double));

    // pop8: GPiSNr
    if (pop8._active)
        memset( pop8._sum_exc.data(), 0.0, pop8._sum_exc.size() * sizeof(double));

    // pop8: GPiSNr
    if (pop8._active)
        memset( pop8._sum_inh.data(), 0.0, pop8._sum_inh.size() * sizeof(double));

    // pop9: STN
    if (pop9._active)
        memset( pop9._sum_exc.data(), 0.0, pop9._sum_exc.size() * sizeof(double));

    // pop9: STN
    if (pop9._active)
        memset( pop9._sum_inh.data(), 0.0, pop9._sum_inh.size() * sizeof(double));

#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Update psp/conductances ..." << std::endl;
#endif
    proj0.compute_psp();
    proj1.compute_psp();
    proj2.compute_psp();
    proj3.compute_psp();
    proj4.compute_psp();
    proj5.compute_psp();
    proj6.compute_psp();
    proj7.compute_psp();
    proj8.compute_psp();
    proj9.compute_psp();
    proj10.compute_psp();
    proj11.compute_psp();
    proj12.compute_psp();
    proj13.compute_psp();
    proj14.compute_psp();
    proj15.compute_psp();
    proj16.compute_psp();
    proj17.compute_psp();
    proj18.compute_psp();
    proj19.compute_psp();
    proj20.compute_psp();
    proj21.compute_psp();
    proj22.compute_psp();
    proj23.compute_psp();
    proj24.compute_psp();
    proj25.compute_psp();
    proj26.compute_psp();
    proj27.compute_psp();
    proj28.compute_psp();



    ////////////////////////////////
    // Recording target variables
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Record psp/conductances ..." << std::endl;
#endif
    for (unsigned int i=0; i < recorders.size(); i++){
        recorders[i]->record_targets();
    }

    ////////////////////////////////
    // Update random distributions
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Draw required random numbers ..." << std::endl;
#endif




    ////////////////////////////////
    // Update neural variables
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Evaluate neural ODEs ..." << std::endl;
#endif

    pop5.update(); pop5.spike_gather(); 
    pop6.update(); pop6.spike_gather(); 
    pop7.update(); pop7.spike_gather(); 
    pop8.update(); pop8.spike_gather(); 
    pop9.update(); pop9.spike_gather(); 



    ////////////////////////////////
    // Delay outputs
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Update delay queues ..." << std::endl;
#endif
    pop0.update_delay();
    pop1.update_delay();
    pop2.update_delay();
    pop3.update_delay();
    pop6.update_delay();
    pop7.update_delay();
    pop9.update_delay();


    ////////////////////////////////
    // Global operations (min/max/mean)
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Update global operations ..." << std::endl;
#endif




    ////////////////////////////////
    // Update synaptic variables
    ////////////////////////////////
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "Evaluate synaptic ODEs ..." << std::endl;
#endif




    ////////////////////////////////
    // Postsynaptic events
    ////////////////////////////////


    ////////////////////////////////
    // Structural plasticity
    ////////////////////////////////


    ////////////////////////////////
    // Recording neural / synaptic variables
    ////////////////////////////////

    for (unsigned int i=0; i < recorders.size(); i++){
        recorders[i]->record();
    }


    ////////////////////////////////
    // Increase internal time
    ////////////////////////////////
    t++;


}


/*
 * Access to time and dt
 *
*/
long int getTime() {return t;}
void setTime(long int t_) { t=t_;}
double getDt() { return dt;}
void setDt(double dt_) { dt=dt_;}

/*
 * Number of threads
 *
*/
void setNumberThreads(int threads, std::vector<int> core_list)
{
    std::cerr << "WARNING: a call of setNumberThreads() is without effect on single thread simulation code." << std::endl;
}
