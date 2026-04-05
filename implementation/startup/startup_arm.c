#include <stdint.h>

extern uint32_t _etext;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t _estack;

extern int main(void);

void Reset_Handler(void) {
    uint32_t *src, *dest;

    // copy .data section f
    src = &_etext;
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

    // infinite loop in cas
    while (1);
}

// minimal vector table
__attribute__((section(".isr_vector")))
void (* const g_pfnVectors[])(void) = {
    (void (*)(void))(&_estack),
    Reset_Handler
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
