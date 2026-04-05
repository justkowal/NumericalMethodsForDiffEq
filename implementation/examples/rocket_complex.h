#ifndef ROCKET_PHYSICS_H
#define ROCKET_PHYSICS_H

#include "ode_solver.h"
#include <stddef.h>

static inline float rocket_fabsf(float x) { return x < 0.0f ? -x : x; }

/* constants based on problem.py ... */
#define G 9.81f              /* gravity (m/s^2)... */
#define RHO_0 1.225f         /* sea level air density (kg/m^3)... */

typedef struct {
    float m_dry;           /* dry mass of rocket... */
    float m_fuel_0;        /* initial fuel mass... */
    float burn_rate;       /* q = dm/dt (positive constant)... */
    float t_burn;          /* duration of burn: m_fuel_0 / q... */
    float v_e;             /* exhaust velocity... */
    float A;               /* cross-sectional area... */
    float C_d;             /* drag coefficient... */
} RocketParams;

/* mass function m(t)... */
static inline float get_mass(float t, const RocketParams* p) {
    if (t < p->t_burn) {
        float ratio = 1.0f - t/p->t_burn;
        return p->m_dry + p->m_fuel_0 * (ratio * ratio);
    }
    return p->m_dry;
}

/* mass derivative dm/dt... */
static inline float get_dmdt(float t, const RocketParams* p) {
    if (t < p->t_burn) {
        /* derivative of m_fuel_0 * (1 - ... */
        return -2.0f * p->m_fuel_0 / p->t_burn * (1.0f - t/p->t_burn);
    }
    return 0.0f;
}

/* ode system... */
static inline int rocket_ode(float t, const float* y, size_t n, float* dydt, void* params) {
    (void)n; /* we know it's a 1d system... */
    
    RocketParams* p = (RocketParams*)params;
    
    float v = y[0];
    
    float m_t = get_mass(t, p);
    float dmdt = get_dmdt(t, p);
    
    /* dynamics... */
    float thrust_accel = 0.0f;
    if (t < p->t_burn) {
        /* thrust = -v_e * dm/dt (note dm... */
        thrust_accel = -(dmdt / m_t) * p->v_e;
    }
    
    /* drag (assuming constant density... */
    float rho = RHO_0;
    float drag_force = 0.5f * rho * v * rocket_fabsf(v) * p->C_d * p->A;
    float drag_accel = drag_force / m_t;
    
    /* velocity derivative... */
    dydt[0] = thrust_accel - G - drag_accel;
    
    return 0;
}

#endif // ROCKET_PHYSICS_H
