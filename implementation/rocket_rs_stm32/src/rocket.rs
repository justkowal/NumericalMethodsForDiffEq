pub const G: f32 = 9.81;
pub const RHO_0: f32 = 1.225;

#[derive(Copy, Clone)]
pub struct RocketParams {
    pub m_dry: f32,
    pub m_fuel_0: f32,
    pub burn_rate: f32,
    pub t_burn: f32,
    pub v_e: f32,
    pub area: f32,
    pub c_d: f32,
}

impl RocketParams {
    pub const fn default_profile() -> Self {
        Self {
            m_dry: 100.0,
            m_fuel_0: 500.0,
            burn_rate: 10.0,
            t_burn: 500.0 / 10.0,
            v_e: 2500.0,
            area: 0.5,
            c_d: 0.4,
        }
    }

    pub fn mass(&self, t: f32) -> f32 {
        if t < self.t_burn {
            let ratio = 1.0 - t / self.t_burn;
            self.m_dry + self.m_fuel_0 * (ratio * ratio)
        } else {
            self.m_dry
        }
    }

    pub fn dmdt(&self, t: f32) -> f32 {
        if t < self.t_burn {
            -2.0 * self.m_fuel_0 / self.t_burn * (1.0 - t / self.t_burn)
        } else {
            0.0
        }
    }
}

pub fn rocket_ode(t: f32, y: &[f32], dydt: &mut [f32], p: &RocketParams) -> Result<(), i32> {
    if y.is_empty() || dydt.is_empty() {
        return Err(-1);
    }

    let v = y[0];
    let m_t = p.mass(t);
    let dmdt = p.dmdt(t);

    let thrust_accel = if t < p.t_burn {
        -(dmdt / m_t) * p.v_e
    } else {
        0.0
    };

    let drag_force = 0.5 * RHO_0 * v * v.abs() * p.c_d * p.area;
    let drag_accel = drag_force / m_t;

    dydt[0] = thrust_accel - G - drag_accel;
    Ok(())
}
