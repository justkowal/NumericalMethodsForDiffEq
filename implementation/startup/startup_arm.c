#include <stdint.h>

extern uint32_t _sidata;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t _estack;

extern int main(void);

void Reset_Handler(void) {
    uint32_t *src, *dest;

    // Hardware already initialized SP from vector table entry 0.
    
    // copy .data section
    src = &_sidata;
    dest = &_sdata;
    while (dest < &_edata) {
        *dest++ = *src++;
    }

    // zero .bss section
    dest = &_sbss;
    while (dest < &_ebss) {
        *dest++ = 0;
    }

    // call main
    main();

    // Signal successful exit to probe-rs or loop
    // But first, spin briefly if RTT hasn't drained? Actually, infinite loop is safer for testing.
    while (1);
}

void HardFault_Handler(void) {
    while (1);
}

// minimal vector table
__attribute__((section(".isr_vector"), used))
void (* const g_pfnVectors[64])(void) = {
    (void (*)(void))(&_estack), // 0: SP
    Reset_Handler,              // 1: Reset
    HardFault_Handler,          // 2: NMI
    HardFault_Handler,          // 3: HardFault
    HardFault_Handler,          // 4: MemManage
    HardFault_Handler,          // 5: BusFault
    HardFault_Handler           // 6: UsageFault
};

void *memcpy(void *dest, const void *src, uint32_t n) {
    char *dp = dest;
    const char *sp = src;
    while (n--) *dp++ = *sp++;
    return dest;
}

void *memset(void *s, int c, uint32_t n) {
    char *p = s;
    while (n--) *p++ = c;
    return s;
}

void _start(void) { Reset_Handler(); }
