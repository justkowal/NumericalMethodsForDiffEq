/* * * complex rocket trajectory for x86 using printf * * */

#include "ode_solver.h"
#include "rocket_complex.h"
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

int main(int argc, char** argv) {
    (void)argc;
    (void)argv;

    /* rocket parameters... */
    RocketParams params = {
        .m_dry = 100.0f,           /* kg... */
        .m_fuel_0 = 500.0f,        /* kg... */
        .burn_rate = 10.0f,        /* kg/s... */
        .v_e = 2500.0f,            /* m/s... */
        .A = 0.5f,                 /* m^2... */
        .C_d = 0.4f                /* dimensionless... */
    };
    params.t_burn = params.m_fuel_0 / params.burn_rate;
    
    /* initial conditions: y[0]=v=0... */
    float y[1] = {0.0f};
    
    float t = 0.0f;
    float h_step = 0.1f;
    float t_max = 250.0f;     /* simulate up to 250 sec... */
    
    int step_idx = 0;
    printf("time,velocity\n");
    while (t <= t_max) {
        if (step_idx % 100 == 0) {
            printf("%f,%f\n", t, y[0]);
        }
        
        ode_rk4(t, y, h_step, 1, rocket_ode, &params);
        
        t += h_step;
        step_idx++;
    }

    return 0;
}
