#!/bin/bash
set -e

ENV_NAME=${1:-fast_rk4}
if [ "$ENV_NAME" != "slow_rk4" ] && [ "$ENV_NAME" != "fast_rk4" ] && [ "$ENV_NAME" != "slow_fwd_euler" ] && [ "$ENV_NAME" != "fast_fwd_euler" ]; then
    echo "Usage: ./upload.sh [fast_rk4|slow_rk4|fast_fwd_euler|slow_fwd_euler]"
    exit 1
fi

echo "Building environment: $ENV_NAME"
# Build the firmware
/home/jakubkowal/NumericalMethodsForDiffEq/.venv/bin/pio run -e $ENV_NAME

echo "Resetting debug probe..."
killall probe-rs || true
sleep 1

echo "Flashing Application Firmware to STM32..."
/home/jakubkowal/.cargo/bin/probe-rs run --chip STM32G474CE .pio/build/$ENV_NAME/firmware.elf

echo "Done! The data should have printed out in this terminal window via RTT."
