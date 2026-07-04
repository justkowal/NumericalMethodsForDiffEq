#!/bin/bash

# Configuration
DEFAULT_STEP=0.04
QUAD_STEP=$(echo "scale=4; $DEFAULT_STEP / 4" | bc)
TARGET="thumbv7em-none-eabihf"
# Simulation takes about 25-30s real time to reach 250s sim time in slow mode.
# We increase the buffer to ensure we catch the "DONE" marker.
WAIT_TIME=60

echo "Starting data collection for rocket simulation..."

# --- Dependency Check ---
echo "Checking for Rust target: $TARGET"
if ! rustup target list --installed | grep -q "$TARGET"; then
    echo "Target $TARGET not found. Installing..."
    rustup target add "$TARGET"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install $TARGET. Please check your internet connection."
        exit 1
    fi
    echo "Target installed successfully."
fi

echo "Default Step Size: $DEFAULT_STEP"
echo "High-Res Step Size: $QUAD_STEP"

# Helper function to run simulation and clean output
# Strips leading timestamps like "19:05:10.588: "
run_sim() {
    local step=$1
    local bin=$2
    local output=$3
    
    echo "Collecting: $bin (h=$step)"
    ROCKET_STEP_SIZE=$step cargo $bin | sed 's/^[0-9:\.]* //g' > "$output" &
    local pid=$!
    
    # Wait for completion or timeout
    sleep $WAIT_TIME
    kill $pid 2>/dev/null
    
    # Short delay to allow the OS to release the USB debug probe interface
    sleep 2
    
    echo "Saved to $output"
}

echo "------------------------------------------------"
# 1. Collect Slow RK4 (Default Step)
run_sim $DEFAULT_STEP "slow_rk4" "rk4_slow_h_default.csv"

echo "------------------------------------------------"
# 2. Collect Slow Euler (Default Step)
run_sim $DEFAULT_STEP "slow_fwd_euler" "euler_slow_h_default.csv"

echo "------------------------------------------------"
# 3. Collect Slow Euler (4x More Steps)
run_sim $QUAD_STEP "slow_fwd_euler" "euler_slow_h_quad.csv"

echo "------------------------------------------------"
echo "Data collection complete."
echo "Files generated: rk4_slow_h_default.csv, euler_slow_h_default.csv, euler_slow_h_quad.csv"