#pragma once

#include <string>
#include <vector>
#include <algorithm>
#include <map>
#include <deque>
#include <queue>
#include <iostream>
#include <sstream>
#include <fstream>
#include <cstdlib>
#include <stdlib.h>
#include <string.h>
#include <cmath>
#include <random>
#include <cassert>


/*
 * Built-in functions
 *
 */

#define positive(x) (x>0.0? x : 0.0)
#define negative(x) (x<0.0? x : 0.0)
#define clip(x, a, b) (x<a? a : (x>b? b :x))
#define modulo(a, b) long(a) % long(b)
#define ite(a, b, c) (a?b:c)

// power function for integer exponent
inline double power(double x, unsigned int a){
    double res=x;
    for (unsigned int i=0; i< a-1; i++){
        res *= x;
    }
    return res;
};


/*
 * Custom constants
 *
 */

extern double tau_MSN;
void set_tau_MSN(double value);
extern double tau_FSI;
void set_tau_FSI(double value);
extern double tau_STN;
void set_tau_STN(double value);
extern double tau_GPe;
void set_tau_GPe(double value);
extern double tau_GPiSNr;
void set_tau_GPiSNr(double value);
extern double sigmap;
void set_sigmap(double value);
extern double Smax_MSN;
void set_Smax_MSN(double value);
extern double Smax_STN;
void set_Smax_STN(double value);
extern double Smax_GPe;
void set_Smax_GPe(double value);
extern double Smax_GPiSNr;
void set_Smax_GPiSNr(double value);
extern double Smax_FSI;
void set_Smax_FSI(double value);
extern double theta_MSN;
void set_theta_MSN(double value);
extern double theta_FSI;
void set_theta_FSI(double value);
extern double theta_STN;
void set_theta_STN(double value);
extern double theta_GPe;
void set_theta_GPe(double value);
extern double theta_GPiSNr;
void set_theta_GPiSNr(double value);

/*
 * Custom functions
 *
 */


/*
 * Structures for the populations
 *
 */
#include "pop0.hpp"
#include "pop1.hpp"
#include "pop2.hpp"
#include "pop3.hpp"
#include "pop4.hpp"
#include "pop5.hpp"
#include "pop6.hpp"
#include "pop7.hpp"
#include "pop8.hpp"
#include "pop9.hpp"

/*
 * Structures for the projections
 *
 */
#include "proj0.hpp"
#include "proj1.hpp"
#include "proj2.hpp"
#include "proj3.hpp"
#include "proj4.hpp"
#include "proj5.hpp"
#include "proj6.hpp"
#include "proj7.hpp"
#include "proj8.hpp"
#include "proj9.hpp"
#include "proj10.hpp"
#include "proj11.hpp"
#include "proj12.hpp"
#include "proj13.hpp"
#include "proj14.hpp"
#include "proj15.hpp"
#include "proj16.hpp"
#include "proj17.hpp"
#include "proj18.hpp"
#include "proj19.hpp"
#include "proj20.hpp"
#include "proj21.hpp"
#include "proj22.hpp"
#include "proj23.hpp"
#include "proj24.hpp"
#include "proj25.hpp"
#include "proj26.hpp"
#include "proj27.hpp"
#include "proj28.hpp"



/*
 * Internal data
 *
*/
extern double dt;
extern long int t;
extern std::vector<std::mt19937> rng;


/*
 * Declaration of the populations
 *
 */
extern PopStruct0 pop0;
extern PopStruct1 pop1;
extern PopStruct2 pop2;
extern PopStruct3 pop3;
extern PopStruct4 pop4;
extern PopStruct5 pop5;
extern PopStruct6 pop6;
extern PopStruct7 pop7;
extern PopStruct8 pop8;
extern PopStruct9 pop9;


/*
 * Declaration of the projections
 *
 */
extern ProjStruct0 proj0;
extern ProjStruct1 proj1;
extern ProjStruct2 proj2;
extern ProjStruct3 proj3;
extern ProjStruct4 proj4;
extern ProjStruct5 proj5;
extern ProjStruct6 proj6;
extern ProjStruct7 proj7;
extern ProjStruct8 proj8;
extern ProjStruct9 proj9;
extern ProjStruct10 proj10;
extern ProjStruct11 proj11;
extern ProjStruct12 proj12;
extern ProjStruct13 proj13;
extern ProjStruct14 proj14;
extern ProjStruct15 proj15;
extern ProjStruct16 proj16;
extern ProjStruct17 proj17;
extern ProjStruct18 proj18;
extern ProjStruct19 proj19;
extern ProjStruct20 proj20;
extern ProjStruct21 proj21;
extern ProjStruct22 proj22;
extern ProjStruct23 proj23;
extern ProjStruct24 proj24;
extern ProjStruct25 proj25;
extern ProjStruct26 proj26;
extern ProjStruct27 proj27;
extern ProjStruct28 proj28;


/*
 * Recorders
 *
 */
#include "Recorder.h"

extern std::vector<Monitor*> recorders;
int addRecorder(Monitor* recorder);
Monitor* getRecorder(int id);
void removeRecorder(Monitor* recorder);

/*
 * Simulation methods
 *
*/

void initialize(double _dt) ;

void init_rng_dist();

void run(int nbSteps);

int run_until(int steps, std::vector<int> populations, bool or_and);

void step();


/*
 * Time export
 *
*/
long int getTime() ;
void setTime(long int t_) ;

double getDt() ;
void setDt(double dt_);

/*
 * Number of threads
 *
*/
void setNumberThreads(int threads, std::vector<int> core_list);

/*
 * Seed for the RNG
 *
*/
void setSeed(long int seed, int num_sources, bool use_seed_seq);

