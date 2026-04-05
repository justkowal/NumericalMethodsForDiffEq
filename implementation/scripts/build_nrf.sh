#!/bin/bash
set -e
mkdir -p obj build
arm-none-eabi-gcc -c startup/startup_arm.c -o obj/startup_arm.o -mcpu=cortex-m4 -mthumb -O3
arm-none-eabi-gcc -c src/rk4.c -Iinclude -o obj/rk4.o -mcpu=cortex-m4 -mthumb -O3 -ffreestanding
arm-none-eabi-gcc -c examples/rocket_nrf52840.c -Iinclude -o obj/rocket_nrf52840.o -mcpu=cortex-m4 -mthumb -O3 -ffreestanding
arm-none-eabi-gcc obj/startup_arm.o obj/rk4.o obj/rocket_nrf52840.o -o build/rocket_nrf52840.elf -T test_link.ld -mcpu=cortex-m4 -mthumb -nostdlib -lgcc -lgcc -lm -Xlinker --gc-sections
echo "Build complete."
