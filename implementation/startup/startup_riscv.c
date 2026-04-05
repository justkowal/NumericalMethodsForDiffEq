#include <stdint.h>

extern uint32_t _etext;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t _estack;

extern int main(void);

__attribute__((section(".text.reset"), naked))
void Reset_Handler(void) {
    // set stack pointer
    __asm__ volatile ("la sp, _estack");

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
