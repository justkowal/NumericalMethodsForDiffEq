#![no_std]
#![no_main]

use cortex_m_rt::entry;

use rocket_rs_stm32::runtime;

extern crate panic_halt;

#[entry]
fn main() -> ! {
    runtime::run::<false, false>()
}
