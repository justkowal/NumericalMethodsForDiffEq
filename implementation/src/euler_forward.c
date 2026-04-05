/* * * forward euler method imple... */

#include "ode_solver.h"

int ode_euler_forward(
    float t, 
    float* y, 
    float h, 
    size_t n, 
    ode_derivative_fn dydt_fn, 
    void* params)
{
    if (n == 0 || n > ODE_MAX_STATES) {
        return -1;  /* invalid system size... */
    }
    
    if (dydt_fn == NULL) {
        return -1;  /* no derivative function... */
    }
    
    /* temporary buffer for derivativ... */
    static float dydt_buffer[ODE_MAX_STATES];
    float* dydt = dydt_buffer;
    
    /* compute derivatives at current... */
    int result = dydt_fn(t, y, n, dydt, params);
    if (result != 0) {
        return result;
    }
    
    /* update each state: y += h * dy... */
    for (size_t i = 0; i < n; i++) {
        y[i] = y[i] + h * dydt[i];
    }
    
    return 0;
}
