/* * * runge-kutta 4th order meth... */

#include "ode_solver.h"

int ode_rk4(
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
    
    /* temporary buffers for intermed... */
    static float k1_buffer[ODE_MAX_STATES];
    static float k2_buffer[ODE_MAX_STATES];
    static float k3_buffer[ODE_MAX_STATES];
    static float k4_buffer[ODE_MAX_STATES];
    static float y_temp_buffer[ODE_MAX_STATES];
    
    float* k1 = k1_buffer;
    float* k2 = k2_buffer;
    float* k3 = k3_buffer;
    float* k4 = k4_buffer;
    float* y_temp = y_temp_buffer;
    
    float h_half = h * 0.5f;
    float h_sixth = h / 6.0f;
    int result;
    
    /* k1 = f(t, y)... */
    result = dydt_fn(t, y, n, k1, params);
    if (result != 0) {
        return result;
    }
    
    /* k2 = f(t + h/2, y + h/2 * k1)... */
    for (size_t i = 0; i < n; i++) {
        y_temp[i] = y[i] + h_half * k1[i];
    }
    result = dydt_fn(t + h_half, y_temp, n, k2, params);
    if (result != 0) {
        return result;
    }
    
    /* k3 = f(t + h/2, y + h/2 * k2)... */
    for (size_t i = 0; i < n; i++) {
        y_temp[i] = y[i] + h_half * k2[i];
    }
    result = dydt_fn(t + h_half, y_temp, n, k3, params);
    if (result != 0) {
        return result;
    }
    
    /* k4 = f(t + h, y + h * k3)... */
    for (size_t i = 0; i < n; i++) {
        y_temp[i] = y[i] + h * k3[i];
    }
    result = dydt_fn(t + h, y_temp, n, k4, params);
    if (result != 0) {
        return result;
    }
    
    /* update: y = y + (h/6) * (k1 + ... */
    for (size_t i = 0; i < n; i++) {
        y[i] = y[i] + h_sixth * (k1[i] + 2.0f * k2[i] + 2.0f * k3[i] + k4[i]);
    }
    
    return 0;
}
