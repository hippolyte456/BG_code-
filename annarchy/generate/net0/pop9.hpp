/*
 *  ANNarchy-version: 4.7.0
 */
#pragma once
#include "ANNarchy.h"
#include <random>


extern double dt;
extern long int t;
extern std::vector<std::mt19937> rng;


///////////////////////////////////////////////////////////////
// Main Structure for the population of id 9 (STN)
///////////////////////////////////////////////////////////////
struct PopStruct9{

    int size; // Number of neurons
    bool _active; // Allows to shut down the whole population
    int max_delay; // Maximum number of steps to store for delayed synaptic transmission

    // Access functions used by cython wrapper
    int get_size() { return size; }
    void set_size(int s) { size  = s; }
    int get_max_delay() { return max_delay; }
    void set_max_delay(int d) { max_delay  = d; }
    bool is_active() { return _active; }
    void set_active(bool val) { _active = val; }



    // Neuron specific parameters and variables

    // Local parameter tau
    std::vector< double > tau;

    // Local variable mp
    std::vector< double > mp;

    // Local variable r
    std::vector< double > r;

    // Local psp _sum_exc
    std::vector< double > _sum_exc;

    // Local psp _sum_inh
    std::vector< double > _sum_inh;

    // Random numbers

    // Local functions
    double f_activateSTN (double x) {return Smax_STN/(exp((theta_STN - x)/sigmap) + 1.0) ;};



    // Delayed variables
    std::deque< std::vector< double > > _delayed_r;



    // Access methods to the parameters and variables

    std::vector<double> get_local_attribute_all_double(std::string name) {

        // Local parameter tau
        if ( name.compare("tau") == 0 ) {
            return tau;
        }

        // Local variable mp
        if ( name.compare("mp") == 0 ) {
            return mp;
        }

        // Local variable r
        if ( name.compare("r") == 0 ) {
            return r;
        }

        // Local psp _sum_exc
        if ( name.compare("_sum_exc") == 0 ) {
            return _sum_exc;
        }

        // Local psp _sum_inh
        if ( name.compare("_sum_inh") == 0 ) {
            return _sum_inh;
        }


        // should not happen
        std::cerr << "PopStruct9::get_local_attribute_all_double: " << name << " not found" << std::endl;
        return std::vector<double>();
    }

    double get_local_attribute_double(std::string name, int rk) {
        assert( (rk < size) );

        // Local parameter tau
        if ( name.compare("tau") == 0 ) {
            return tau[rk];
        }

        // Local variable mp
        if ( name.compare("mp") == 0 ) {
            return mp[rk];
        }

        // Local variable r
        if ( name.compare("r") == 0 ) {
            return r[rk];
        }

        // Local psp _sum_exc
        if ( name.compare("_sum_exc") == 0 ) {
            return _sum_exc[rk];
        }

        // Local psp _sum_inh
        if ( name.compare("_sum_inh") == 0 ) {
            return _sum_inh[rk];
        }


        // should not happen
        std::cerr << "PopStruct9::get_local_attribute_double: " << name << " not found" << std::endl;
        return static_cast<double>(0.0);
    }

    void set_local_attribute_all_double(std::string name, std::vector<double> value) {
        assert( (value.size() == size) );

        // Local parameter tau
        if ( name.compare("tau") == 0 ) {
            tau = value;
            return;
        }

        // Local variable mp
        if ( name.compare("mp") == 0 ) {
            mp = value;
            return;
        }

        // Local variable r
        if ( name.compare("r") == 0 ) {
            r = value;
            return;
        }

        // Local psp _sum_exc
        if ( name.compare("_sum_exc") == 0 ) {
            _sum_exc = value;
            return;
        }

        // Local psp _sum_inh
        if ( name.compare("_sum_inh") == 0 ) {
            _sum_inh = value;
            return;
        }


        // should not happen
        std::cerr << "PopStruct9::set_local_attribute_all_double: " << name << " not found" << std::endl;
    }

    void set_local_attribute_double(std::string name, int rk, double value) {
        assert( (rk < size) );

        // Local parameter tau
        if ( name.compare("tau") == 0 ) {
            tau[rk] = value;
            return;
        }

        // Local variable mp
        if ( name.compare("mp") == 0 ) {
            mp[rk] = value;
            return;
        }

        // Local variable r
        if ( name.compare("r") == 0 ) {
            r[rk] = value;
            return;
        }

        // Local psp _sum_exc
        if ( name.compare("_sum_exc") == 0 ) {
            _sum_exc[rk] = value;
            return;
        }

        // Local psp _sum_inh
        if ( name.compare("_sum_inh") == 0 ) {
            _sum_inh[rk] = value;
            return;
        }


        // should not happen
        std::cerr << "PopStruct9::set_local_attribute_double: " << name << " not found" << std::endl;
    }



    // Method called to initialize the data structures
    void init_population() {
    #ifdef _DEBUG
        std::cout << "PopStruct9::init_population() - this = " << this << std::endl;
    #endif
        _active = true;

        // Local parameter tau
        tau = std::vector<double>(size, 0.0);

        // Local variable mp
        mp = std::vector<double>(size, 0.0);

        // Local variable r
        r = std::vector<double>(size, 0.0);

        // Local psp _sum_exc
        _sum_exc = std::vector<double>(size, 0.0);

        // Local psp _sum_inh
        _sum_inh = std::vector<double>(size, 0.0);



        // Delayed variables
        _delayed_r = std::deque< std::vector< double > >(max_delay, std::vector< double >(size, 0.0));



    }

    // Method called to reset the population
    void reset() {


        for ( int i = 0; i < _delayed_r.size(); i++ ) {
            _delayed_r[i] = r;
        }


    }

    // Init rng dist
    void init_rng_dist() {

    }

    // Method to draw new random numbers
    void update_rng() {
#ifdef _TRACE_SIMULATION_STEPS
    std::cout << "    PopStruct9::update_rng()" << std::endl;
#endif

    }

    // Method to update global operations on the population (min/max/mean...)
    void update_global_ops() {

    }

    // Method to enqueue output variables in case outgoing projections have non-zero delay
    void update_delay() {

        if ( _active ) {

        _delayed_r.push_front(r);
        _delayed_r.pop_back();

        }
    }

    // Method to dynamically change the size of the queue for delayed variables
    void update_max_delay(int value) {

        if(value <= max_delay){ // nothing to do
            return;
        }
        max_delay = value;

    _delayed_r.resize(max_delay, std::vector< double >(size, 0.0));

    }

    // Main method to update neural variables
    void update() {

        if( _active ) {
        #ifdef _TRACE_SIMULATION_STEPS
            std::cout << "    PopStruct9::update()" << std::endl;
        #endif

            // Updating the local variables
            #pragma omp simd
            for(int i = 0; i < size; i++){

                // tau * dmp/dt  + mp = sum(exc) - sum(inh)
                double _mp = (_sum_exc[i] - _sum_inh[i] - mp[i])/tau[i];

                // tau * dmp/dt  + mp = sum(exc) - sum(inh)
                mp[i] += dt*_mp ;


                // r = f_activateSTN(mp)
                r[i] = f_activateSTN(mp[i]);


            }
        } // active

    }

    void spike_gather() {

    }



    // Memory management: track the memory consumption
    long int size_in_bytes() {
        long int size_in_bytes = 0;
        // Parameters
        size_in_bytes += sizeof(double) * tau.capacity();	// tau
        // Variables
        size_in_bytes += sizeof(double) * mp.capacity();	// mp
        size_in_bytes += sizeof(double) * r.capacity();	// r

        return size_in_bytes;
    }

    // Memory management: destroy all the C++ data
    void clear() {
#ifdef _DEBUG
    std::cout << "PopStruct9::clear() - this = " << this << std::endl;
#endif
        // Variables
        mp.clear();
        mp.shrink_to_fit();
        r.clear();
        r.shrink_to_fit();

    }
};

