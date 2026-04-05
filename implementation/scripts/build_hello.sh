#!/bin/bash
set -e
mkdir -p obj build
arm-none-eabi-gcc -c startup/startup_arm.c -o obj/startup_arm.o -mcpu=cortex-m4 -mthumb -O3
arm-none-eabi-gcc -c src/mini_rtt.c -o obj/mini_rtt.o -mcpu=cortex-m4 -mthumb -O3
arm-none-eabi-gcc -c examples/hello_nrf52840.c -o obj/hello_nrf52840.o -mcpu=cortex-m4 -mthumb -O3
arm-none-eabi-gcc obj/startup_arm.o obj/mini_rtt.o obj/hello_nrf52840.o -o build/hello_nrf52840.elf -T test_link.ld -mcpu=cortex-m4 -mthumb -nostdlib -lgcc -Xlinker --gc-sections
echo "Build complete."
