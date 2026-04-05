#include <Arduino.h>

extern "C" {
#include "ode_solver.h"
#include "rocket_complex.h"
void rtt_write(const void* data, unsigned int len);
}

void rtt_print(const char* str) {
    rtt_write(str, strlen(str));
    delay(2); // Small delay to let probe-rs read the buffer before it fills up
}

void my_ftoa(float n, char* res, int afterpoint) {
    int ipart = (int)n;
    float fpart = n - (float)ipart;
    if (fpart < 0) fpart = -fpart;
    if (n < 0 && ipart == 0) {
        *res++ = '-';
        ipart = 0;
    }
    itoa(ipart, res, 10);
    int p = strlen(res);
    if (afterpoint != 0) {
        res[p] = '.';
        for (int i=0; i<afterpoint; i++) {
           fpart = fpart * 10;
        }
        itoa((int)(fpart + 0.5f), res + p + 1, 10);
    }
}

#ifdef SLOW_MODE
uint32_t original_cfgr;
float clock_speed_hz = 31250.0f; // 16MHz HSI / 512

void go_slow() {
    // Enable HSI16
    RCC->CR |= RCC_CR_HSION;
    while(!(RCC->CR & RCC_CR_HSIRDY));
    
    original_cfgr = RCC->CFGR;
    uint32_t cfgr = original_cfgr;
    
    // Switch SYSCLK to HSI16 and set AHB prescaler to 512
    cfgr &= ~(RCC_CFGR_SW_Msk | RCC_CFGR_HPRE_Msk);
    cfgr |= RCC_CFGR_SW_HSI | RCC_CFGR_HPRE_DIV512;
    
    RCC->CFGR = cfgr;
    // Wait until switch is done
    while((RCC->CFGR & RCC_CFGR_SWS_Msk) != RCC_CFGR_SWS_HSI);
}

void go_fast() {
    RCC->CFGR = original_cfgr;
    // Wait until switch is done back to whatever it was (usually PLL)
    while((RCC->CFGR & RCC_CFGR_SWS_Msk) != (original_cfgr & RCC_CFGR_SWS_Msk));
}
#else
#define go_slow() {}
#define go_fast() {}
#define clock_speed_hz ((float)SystemCoreClock)
#endif

// Cortex-M3 Data Watchpoint and Trace (DWT) cycle counter registers automatically provided by CMSIS
void setup() {
  rtt_print("Starting computation...\n");
  rtt_print("ExecutionTime(us),SimulationTime(s),Velocity(m/s)\n");

  // Enable DWT Cycle Counter
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  DWT->CYCCNT = 0;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;

  RocketParams params = {
      100.0f,    // m_dry
      500.0f,    // m_fuel_0
      10.0f,     // burn_rate
      500.0f / 10.0f, // t_burn
      2500.0f,   // v_e
      0.5f,      // A
      0.4f       // C_d
  };

  float y[1] = {0.0f};
  float t = 0.0f;
  float h_step = 0.1f;
  float t_max = 250.0f;

  int step_idx = 0;

  float total_exec_time_us = 0.0f;

  while (t <= t_max) {
      go_slow();
      uint32_t step_start = DWT->CYCCNT;
#ifdef USE_EULER
      ode_euler_forward(t, y, h_step, 1, rocket_ode, &params);
#else
      ode_rk4(t, y, h_step, 1, rocket_ode, &params);
#endif
      uint32_t step_end = DWT->CYCCNT;
      go_fast();
      
      uint32_t current_cycles = step_end - step_start;
      total_exec_time_us += (float)current_cycles / (clock_speed_hz / 1000000.0f);

      // Print out over RTT via abstraction
      if (step_idx % 10 == 0) {
          char buf_time[20] = {0};
          char buf_t[20] = {0};
          char buf_y[20] = {0};
          my_ftoa(total_exec_time_us, buf_time, 3);
          my_ftoa(t, buf_t, 2);
          my_ftoa(y[0], buf_y, 4);
          rtt_print(buf_time);
          rtt_print(",");
          rtt_print(buf_t);
          rtt_print(",");
          rtt_print(buf_y);
          rtt_print("\n");
      }
      
      t += h_step;
      step_idx++;
  }

  rtt_print("DONE\n");
  
  while (true) {
    delay(100);
  }
}

void loop() {
}
