# rocket_rs_stm32

no_std Rust port of the STM32 PlatformIO rocket simulation with the same 4 runtime variants:

1. `fast_rk4`
2. `slow_rk4`
3. `fast_fwd_euler`
4. `slow_fwd_euler`

## Target

- MCU family: STM32G4
- Board equivalent: NUCLEO-G474RE
- Rust target: `thumbv7em-none-eabihf`

## What was ported

- ODE solvers (`RK4`, `Forward Euler`) from C into safe Rust slice-based routines.
- Rocket 1D velocity model (mass curve, thrust, drag, gravity).
- RTT telemetry output with CSV-compatible lines:
  - `ExecutionTime(us),SimulationTime(s),Velocity(m/s)`

## Run

From this folder:

```bash
cargo fast_rk4
cargo slow_rk4
cargo fast_fwd_euler
cargo slow_fwd_euler
```

These aliases map to `cargo run --release --bin <variant>`.

## Compile-Time Step Size Flag

The integration step size is configured at compile time via `ROCKET_STEP_SIZE` (seconds).

Default:

```bash
cargo slow_fwd_euler
```

Custom step size (example: 0.05 s):

```bash
ROCKET_STEP_SIZE=0.05 cargo slow_fwd_euler
```

The value must be a positive floating-point number.

## Notes

- Slow mode reproduces the C implementation idea by switching to HSI with AHB `/512` divider around each integration step.
- Fast mode uses a compile-time clock constant (`170 MHz`) for cycle-to-microsecond conversion.
- RTT is provided via `rtt-target` and requires a connected debug probe (e.g., probe-rs).
