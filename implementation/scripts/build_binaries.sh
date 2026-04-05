#!/bin/bash
set -e

mkdir -p obj build

echo "Compiling ARM..."
arm-none-eabi-gcc -c startup/startup_arm.c -o obj/startup_arm.o -mcpu=cortex-m4 -mthumb -O3
arm-none-eabi-gcc -c src/rk4.c -o obj/rk4_arm.o -mcpu=cortex-m4 -mthumb -O3 -Iinclude
arm-none-eabi-gcc -c src/mini_rtt.c -o obj/mini_rtt.o -mcpu=cortex-m4 -mthumb -O3 -Iinclude
arm-none-eabi-gcc -c examples/rocket_nrf52840.c -o obj/rocket_nrf52840_arm.o -mcpu=cortex-m4 -mthumb -O3 -Iinclude
arm-none-eabi-gcc -c examples/rocket_stm32_fast.c -o obj/rocket_stm32_fast_arm.o -mcpu=cortex-m4 -mthumb -O3 -Iinclude
arm-none-eabi-gcc -c examples/rocket_stm32_slow.c -o obj/rocket_stm32_slow_arm.o -mcpu=cortex-m4 -mthumb -O3 -Iinclude

echo "Linking ARM..."
arm-none-eabi-gcc obj/startup_arm.o obj/rocket_nrf52840_arm.o obj/rk4_arm.o obj/mini_rtt.o -o build/rocket_nrf52840.elf -T linker/linker_nrf52840.ld -mcpu=cortex-m4 -mthumb -nostdlib -lgcc -Xlinker --gc-sections
arm-none-eabi-objcopy -O binary build/rocket_nrf52840.elf build/nrf52840.bin

arm-none-eabi-gcc obj/startup_arm.o obj/rocket_stm32_fast_arm.o obj/rk4_arm.o -o build/rocket_stm32_fast.elf -T linker/linker_stm32.ld -mcpu=cortex-m4 -mthumb -nostdlib -lgcc -Xlinker --gc-sections
arm-none-eabi-objcopy -O binary build/rocket_stm32_fast.elf build/stm32_fast.bin

arm-none-eabi-gcc obj/startup_arm.o obj/rocket_stm32_slow_arm.o obj/rk4_arm.o -o build/rocket_stm32_slow.elf -T linker/linker_stm32.ld -mcpu=cortex-m4 -mthumb -nostdlib -lgcc -Xlinker --gc-sections
arm-none-eabi-objcopy -O binary build/rocket_stm32_slow.elf build/stm32_slow.bin


echo "Compiling RISC-V..."
riscv64-unknown-elf-gcc -c startup/startup_riscv.c -o obj/startup_riscv.o -march=rv32imczicsr -mabi=ilp32 -O3
riscv64-unknown-elf-gcc -c src/rk4.c -o obj/rk4_riscv.o -march=rv32imczicsr -mabi=ilp32 -O3 -Iinclude
riscv64-unknown-elf-gcc -c examples/rocket_esp32c3.c -o obj/rocket_esp32c3_riscv.o -march=rv32imczicsr -mabi=ilp32 -O3 -Iinclude

echo "Linking RISC-V..."
riscv64-unknown-elf-gcc obj/startup_riscv.o obj/rocket_esp32c3_riscv.o obj/rk4_riscv.o -o build/rocket_esp32c3.elf -T linker/linker_esp32c3.ld -march=rv32imczicsr -mabi=ilp32 -nostdlib -lgcc -Xlinker --gc-sections
riscv64-unknown-elf-objcopy -O binary build/rocket_esp32c3.elf build/esp32c3.bin

echo "Done!"
