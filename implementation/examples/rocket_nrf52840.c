/* * * complex rocket trajectory ... */

#include "ode_solver.h"
#include "rocket_complex.h"
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

/* hardware stubs... */
#define OUTPUT_CAPACITY 32

/* arm dwt->cyccnt for timing... */
#define DWT_CYCCNT (*(volatile uint32_t *)0xE0001004)
static uint32_t t_start = 0;
static uint32_t t_accum = 0;
#define hw_timer_start() do { t_start = DWT_CYCCNT; } while(0)
#define hw_timer_accumulate() do { t_accum += DWT_CYCCNT - t_start; } while(0)

/* nrf_uarte0 registers for tx... */
static inline void hw_serial_tx(const uint8_t* buf, size_t len) {
    volatile uint32_t* nrf_uarte0_txd = (volatile uint32_t*)0x40028000;
    for (size_t i = 0; i < len; i++) {
        *nrf_uarte0_txd = buf[i];
    }
}

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
    
    typedef struct { float t; float v; } OutPoint;
    OutPoint output_buffer[OUTPUT_CAPACITY];
    int buffered_points = 0;
    
    int step_idx = 0;
    while (t <= t_max) {
        hw_timer_start();
        
        if (step_idx % 100 == 0) {
            output_buffer[buffered_points].t = t;
            output_buffer[buffered_points].v = y[0];
            buffered_points++;
            if (buffered_points >= OUTPUT_CAPACITY) {
                hw_serial_tx((const uint8_t*)output_buffer, buffered_points * sizeof(OutPoint));
                buffered_points = 0;
            }
        }
        
        ode_rk4(t, y, h_step, 1, rocket_ode, &params);
        
        hw_timer_accumulate();
        
        t += h_step;
        step_idx++;
    }
    
    if (buffered_points > 0) {
        hw_serial_tx((const uint8_t*)output_buffer, buffered_points * sizeof(OutPoint));
        buffered_points = 0;
    }

    return 0;
}
