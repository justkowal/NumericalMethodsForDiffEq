#!/bin/bash
set -e

# Build the firmware
/home/jakubkowal/NumericalMethodsForDiffEq/.venv/bin/pio run

# Flash SoftDevice+Bootloader required for Adafruit core (lives @ 0x0)
BOOTLOADER=/home/jakubkowal/.platformio/packages/framework-arduinoadafruitnrf52/bootloader/feather_nrf52840_express/feather_nrf52840_express_bootloader-0.9.1_s140_6.1.1.hex

echo "Resetting debug probe..."
killall probe-rs || true
sleep 1

echo "Erasing locked chip completely..."
/home/jakubkowal/.cargo/bin/probe-rs erase --chip nRF52840_xxAA --allow-erase-all || true
sleep 1

echo "Flashing Adafruit SoftDevice & Bootloader..."
/home/jakubkowal/.cargo/bin/probe-rs download --connect-under-reset --chip nRF52840_xxAA --protocol swd --binary-format hex "$BOOTLOADER"

sleep 1 # Let the debug probe and chip recover from the large write

echo "Flashing Application Firmware..."
/home/jakubkowal/.cargo/bin/probe-rs download --connect-under-reset --chip nRF52840_xxAA --protocol swd --binary-format hex .pio/build/adafruit_feather_nrf52840/firmware.hex

echo "Resetting CPU..."
/home/jakubkowal/.cargo/bin/probe-rs reset --chip nRF52840_xxAA --protocol swd

echo "Done! The device should now mount a Native USB CDC interface on your PC."
