/* * * numerical ode solver libra... */

#ifndef ODE_SOLVER_H
#define ODE_SOLVER_H

#include <stddef.h>

/* ==============================... */

/* default maximum number of stat... */
#ifndef ODE_MAX_STATES
#define ODE_MAX_STATES 64
#endif

/* ==============================... */

/* * * system derivative function... */
typedef int (*ode_derivative_fn)(
    float t, 
    const float* y, 
    size_t n, 
    float* dydt, 
    void* params
);

/* * * forward euler step: y_{n+1... */
int ode_euler_forward(
    float t, 
    float* y, 
    float h, 
    size_t n, 
    ode_derivative_fn dydt_fn, 
    void* params
);

/* * * runge-kutta 4th order step... */
int ode_rk4(
    float t, 
    float* y, 
    float h, 
    size_t n, 
    ode_derivative_fn dydt_fn, 
    void* params
);

#endif /* ode_solver_h... */
