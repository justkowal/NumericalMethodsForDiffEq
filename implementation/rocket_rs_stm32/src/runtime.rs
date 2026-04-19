use core::hint::spin_loop;

use cortex_m::peripheral::{DWT, Peripherals};
use rtt_target::{rprintln, rtt_init_print};

use crate::ode::{ode_euler_forward, ode_rk4};
use crate::rocket::{rocket_ode, RocketParams};

include!(concat!(env!("OUT_DIR"), "/step_size.rs"));

const RCC_BASE: usize = 0x4002_1000;
const RCC_CR_OFFSET: usize = 0x00;
const RCC_CFGR_OFFSET: usize = 0x08;

const RCC_CR_HSION: u32 = 1 << 8;
const RCC_CR_HSIRDY: u32 = 1 << 10;

const RCC_CFGR_SW_MASK: u32 = 0b11;
const RCC_CFGR_SW_HSI: u32 = 0b01;
const RCC_CFGR_SWS_MASK: u32 = 0b11 << 2;
const RCC_CFGR_SWS_HSI: u32 = 0b01 << 2;
const RCC_CFGR_HPRE_MASK: u32 = 0b1111 << 4;
const RCC_CFGR_HPRE_DIV512: u32 = 0b1111 << 4;

const FAST_CLOCK_HZ: f32 = 170_000_000.0;
const SLOW_CLOCK_HZ: f32 = 31_250.0;

fn read_reg(addr: usize) -> u32 {
    unsafe { core::ptr::read_volatile(addr as *const u32) }
}

fn write_reg(addr: usize, value: u32) {
    unsafe { core::ptr::write_volatile(addr as *mut u32, value) }
}

fn delay_cycles(iterations: u32) {
    for _ in 0..iterations {
        spin_loop();
    }
}

fn switch_to_slow_clock() -> u32 {
    let cr = RCC_BASE + RCC_CR_OFFSET;
    let cfgr = RCC_BASE + RCC_CFGR_OFFSET;

    let mut cr_val = read_reg(cr);
    cr_val |= RCC_CR_HSION;
    write_reg(cr, cr_val);

    while (read_reg(cr) & RCC_CR_HSIRDY) == 0 {}

    let original_cfgr = read_reg(cfgr);
    let mut new_cfgr = original_cfgr;
    new_cfgr &= !(RCC_CFGR_SW_MASK | RCC_CFGR_HPRE_MASK);
    new_cfgr |= RCC_CFGR_SW_HSI | RCC_CFGR_HPRE_DIV512;
    write_reg(cfgr, new_cfgr);

    while (read_reg(cfgr) & RCC_CFGR_SWS_MASK) != RCC_CFGR_SWS_HSI {}

    original_cfgr
}

fn restore_clock(original_cfgr: u32) {
    let cfgr = RCC_BASE + RCC_CFGR_OFFSET;
    write_reg(cfgr, original_cfgr);

    while (read_reg(cfgr) & RCC_CFGR_SWS_MASK) != (original_cfgr & RCC_CFGR_SWS_MASK) {}
}

pub fn run<const SLOW_MODE: bool, const USE_EULER: bool>() -> ! {
    rtt_init_print!();
    rprintln!("Starting computation...");
    rprintln!("ExecutionTime(us),SimulationTime(s),Velocity(m/s)");

    let mut cp = match Peripherals::take() {
        Some(p) => p,
        None => loop {
            spin_loop();
        },
    };

    cp.DCB.enable_trace();
    cp.DWT.enable_cycle_counter();

    let params = RocketParams::default_profile();

    let mut y = [0.0_f32; 1];
    let mut t = 0.0_f32;
    let h_step = STEP_SIZE;
    let t_max = 250.0_f32;
    let mut step_idx: u32 = 0;
    let mut total_exec_time_us = 0.0_f32;

    while t <= t_max {
        let original_cfgr = if SLOW_MODE { switch_to_slow_clock() } else { 0 };

        let step_start = DWT::cycle_count();

        let result = if USE_EULER {
            ode_euler_forward(t, &mut y, h_step, |tt, yy, dydt| {
                rocket_ode(tt, yy, dydt, &params)
            })
        } else {
            ode_rk4(t, &mut y, h_step, |tt, yy, dydt| rocket_ode(tt, yy, dydt, &params))
        };

        let step_end = DWT::cycle_count();

        if SLOW_MODE {
            restore_clock(original_cfgr);
        }

        if result.is_err() {
            rprintln!("Solver error at t={:.2}", t);
            loop {
                delay_cycles(100_000);
            }
        }

        let current_cycles = step_end.wrapping_sub(step_start);
        let clock_hz = if SLOW_MODE { SLOW_CLOCK_HZ } else { FAST_CLOCK_HZ };
        total_exec_time_us += (current_cycles as f32) / (clock_hz / 1_000_000.0);

        if step_idx % 10 == 0 {
            rprintln!("{:.3},{:.2},{:.4}", total_exec_time_us, t, y[0]);
            delay_cycles(12_000);
        }

        t += h_step;
        step_idx = step_idx.wrapping_add(1);
    }

    rprintln!("DONE");

    loop {
        delay_cycles(1_000_000);
    }
}
