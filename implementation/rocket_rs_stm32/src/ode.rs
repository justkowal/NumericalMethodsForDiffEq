pub const ODE_MAX_STATES: usize = 64;

pub fn ode_euler_forward<F>(t: f32, y: &mut [f32], h: f32, mut dydt_fn: F) -> Result<(), i32>
where
    F: FnMut(f32, &[f32], &mut [f32]) -> Result<(), i32>,
{
    if y.is_empty() || y.len() > ODE_MAX_STATES {
        return Err(-1);
    }

    let n = y.len();
    let mut dydt = [0.0_f32; ODE_MAX_STATES];
    dydt_fn(t, y, &mut dydt[..n])?;

    for i in 0..n {
        y[i] += h * dydt[i];
    }

    Ok(())
}

pub fn ode_rk4<F>(t: f32, y: &mut [f32], h: f32, mut dydt_fn: F) -> Result<(), i32>
where
    F: FnMut(f32, &[f32], &mut [f32]) -> Result<(), i32>,
{
    if y.is_empty() || y.len() > ODE_MAX_STATES {
        return Err(-1);
    }

    let n = y.len();
    let mut k1 = [0.0_f32; ODE_MAX_STATES];
    let mut k2 = [0.0_f32; ODE_MAX_STATES];
    let mut k3 = [0.0_f32; ODE_MAX_STATES];
    let mut k4 = [0.0_f32; ODE_MAX_STATES];
    let mut y_temp = [0.0_f32; ODE_MAX_STATES];

    let h_half = h * 0.5;
    let h_sixth = h / 6.0;

    dydt_fn(t, y, &mut k1[..n])?;

    for i in 0..n {
        y_temp[i] = y[i] + h_half * k1[i];
    }
    dydt_fn(t + h_half, &y_temp[..n], &mut k2[..n])?;

    for i in 0..n {
        y_temp[i] = y[i] + h_half * k2[i];
    }
    dydt_fn(t + h_half, &y_temp[..n], &mut k3[..n])?;

    for i in 0..n {
        y_temp[i] = y[i] + h * k3[i];
    }
    dydt_fn(t + h, &y_temp[..n], &mut k4[..n])?;

    for i in 0..n {
        y[i] += h_sixth * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]);
    }

    Ok(())
}
