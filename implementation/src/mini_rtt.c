#include <stdint.h>
#include <stddef.h>

#define RTT_BUFFER_SIZE 1024

typedef struct {
    const char* name;
    char* buffer;
    uint32_t size;
    volatile uint32_t write_pos;
    volatile uint32_t read_pos;
    uint32_t flags;
} RTT_BUFFER;

typedef struct {
    char acID[16];
    uint32_t max_num_up_buffers;
    uint32_t max_num_down_buffers;
    RTT_BUFFER up_buffers[1];
} SEGGER_RTT_CB;

char rtt_up_buf[RTT_BUFFER_SIZE];

__attribute__((section(".data")))
SEGGER_RTT_CB _SEGGER_RTT = {
    "SEGGER RTT\0\0\0\0\0",
    1, 0,
    {
        { "Terminal", rtt_up_buf, RTT_BUFFER_SIZE, 0, 0, 2 }
    }
};

void rtt_write(const void* data, size_t len) {
    const uint8_t* d = (const uint8_t*)data;
    while(len--) {
        uint32_t wr = _SEGGER_RTT.up_buffers[0].write_pos;
        uint32_t rd = _SEGGER_RTT.up_buffers[0].read_pos;
        uint32_t next = (wr + 1) % RTT_BUFFER_SIZE;
        
        // Drop data if buffer is full instead of hanging
        if(next == rd) {
            return; 
        }
        
        rtt_up_buf[wr] = *d++;
        _SEGGER_RTT.up_buffers[0].write_pos = next;
    }
}
