#pragma once
#ifdef _OPENMP
    #include <omp.h>
#endif

#include "sparse_matrix.hpp"

#include "pop3.hpp"
#include "pop6.hpp"



extern PopStruct3 pop3;
extern PopStruct6 pop6;

extern std::vector<std::mt19937> rng;

/////////////////////////////////////////////////////////////////////////////
// proj7: PTNstim -> MSN with target exc
/////////////////////////////////////////////////////////////////////////////
struct ProjStruct7 : LILMatrix<int, int> {
    ProjStruct7() : LILMatrix<int, int>( 3, 1) {
    }


    void init_from_lil( std::vector<int> &row_indices,
                        std::vector< std::vector<int> > &column_indices,
                        std::vector< std::vector<double> > &values,
                        std::vector< std::vector<int> > &delays) {
        static_cast<LILMatrix<int, int>*>(this)->init_matrix_from_lil(row_indices, column_indices);

        w = values[0][0];

    delay = delays[0][0];


    #ifdef _DEBUG_CONN
        static_cast<LILMatrix<int, int>*>(this)->print_data_representation();
    #endif
    }





    // Transmission and plasticity flags
    bool _transmission, _plasticity, _update;
    int _update_period;
    long int _update_offset;


    // Uniform delay
    int delay ;



    // Local parameter alpha
    std::vector< std::vector<double > > alpha;

    // Global parameter w
    double  w ;




    // Method called to initialize the projection
    void init_projection() {
    #ifdef _DEBUG
        std::cout << "ProjStruct7::init_projection() - this = " << this << std::endl;
    #endif

        _transmission = true;
        _update = true;
        _plasticity = true;
        _update_period = 1;
        _update_offset = 0L;



        // Local parameter alpha
        alpha = init_matrix_variable<double>(static_cast<double>(0.0));




    }

    // Spiking networks: reset the ring buffer when non-uniform
    void reset_ring_buffer() {

    }

    // Spiking networks: update maximum delay when non-uniform
    void update_max_delay(int d){

    }

    // Computes the weighted sum of inputs or updates the conductances
    void compute_psp() {
    #ifdef _TRACE_SIMULATION_STEPS
        std::cout << "    ProjStruct7::compute_psp()" << std::endl;
    #endif
        double sum;

        if (_transmission && pop6._active){

            std::vector<double> _pre_r = pop3._delayed_r[delay-1];

            for (int i = 0; i < post_rank.size(); i++) {

                sum = 0.0;
                for (int j = 0; j < pre_rank[i].size(); j++) {
                    sum +=  _pre_r[pre_rank[i][j]]*w ;
                }
                pop6._sum_exc[post_rank[i]] += sum;
            }

        } // active

    }

    // Draws random numbers
    void update_rng() {

    }

    // Updates synaptic variables
    void update_synapse() {
    #ifdef _TRACE_SIMULATION_STEPS
        std::cout << "    ProjStruct7::update_synapse()" << std::endl;
    #endif


    }

    // Post-synaptic events
    void post_event() {


    }

    // Variable/Parameter access methods

    std::vector<std::vector<double>> get_local_attribute_all_double(std::string name) {

        if ( name.compare("alpha") == 0 ) {

            return get_matrix_variable_all<double>(alpha);
        }


        // should not happen
        std::cerr << "ProjStruct7::get_local_attribute_all_double: " << name << " not found" << std::endl;
        return std::vector<std::vector<double>>();
    }

    std::vector<double> get_local_attribute_row_double(std::string name, int rk_post) {

        if ( name.compare("alpha") == 0 ) {

            return get_matrix_variable_row<double>(alpha, rk_post);
        }


        // should not happen
        std::cerr << "ProjStruct7::get_local_attribute_row_double: " << name << " not found" << std::endl;
        return std::vector<double>();
    }

    double get_local_attribute_double(std::string name, int rk_post, int rk_pre) {

        if ( name.compare("alpha") == 0 ) {

            return get_matrix_variable<double>(alpha, rk_post, rk_pre);
        }


        // should not happen
        std::cerr << "ProjStruct7::get_local_attribute: " << name << " not found" << std::endl;
        return 0.0;
    }

    void set_local_attribute_all_double(std::string name, std::vector<std::vector<double>> value) {

        if ( name.compare("alpha") == 0 ) {
            update_matrix_variable_all<double>(alpha, value);

            return;
        }

    }

    void set_local_attribute_row_double(std::string name, int rk_post, std::vector<double> value) {

        if ( name.compare("alpha") == 0 ) {
            update_matrix_variable_row<double>(alpha, rk_post, value);

            return;
        }

    }

    void set_local_attribute_double(std::string name, int rk_post, int rk_pre, double value) {

        if ( name.compare("alpha") == 0 ) {
            update_matrix_variable<double>(alpha, rk_post, rk_pre, value);

            return;
        }

    }

    double get_global_attribute_double(std::string name) {

        if ( name.compare("w") == 0 ) {
            return w;
        }


        // should not happen
        std::cerr << "ProjStruct7::get_global_attribute_double: " << name << " not found" << std::endl;
        return 0.0;
    }

    void set_global_attribute_double(std::string name, double value) {

        if ( name.compare("w") == 0 ) {
            w = value;

            return;
        }

    }


    // Access additional


    // Memory management
    long int size_in_bytes() {
        long int size_in_bytes = 0;

        // connectivity
        size_in_bytes += static_cast<LILMatrix<int, int>*>(this)->size_in_bytes();

        // Local parameter alpha
        size_in_bytes += sizeof(std::vector<std::vector<double>>);
        size_in_bytes += sizeof(std::vector<double>) * alpha.capacity();
        for(auto it = alpha.cbegin(); it != alpha.cend(); it++)
            size_in_bytes += (it->capacity()) * sizeof(double);

        // Global parameter w
        size_in_bytes += sizeof(double);

        return size_in_bytes;
    }

    // Structural plasticity



    void clear() {
    #ifdef _DEBUG
        std::cout << "ProjStruct7::clear() - this = " << this << std::endl;
    #endif

        // Connectivity
        static_cast<LILMatrix<int, int>*>(this)->clear();

        // alpha
        for (auto it = alpha.begin(); it != alpha.end(); it++) {
            it->clear();
            it->shrink_to_fit();
        };
        alpha.clear();
        alpha.shrink_to_fit();

    }
};

