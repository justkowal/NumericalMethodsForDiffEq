#include <Arduino.h>

extern "C" {
#include "ode_solver.h"
#include "rocket_complex.h"
}

// Cortex-M4 Data Watchpoint and Trace (DWT) cycle counter registers
#define DEMCR       (*(volatile uint32_t *)0xE000EDFC)
#define DWT_CTRL    (*(volatile uint32_t *)0xE0001000)
#define DWT_CYCCNT  (*(volatile uint32_t *)0xE0001004)

void setup() {
  Serial.begin(115200);
  
  // Wait for the USB CDC connection to open (native USB)
  while(!Serial) {
     delay(10);
  }

  Serial.println("Starting computation...");
  Serial.println("ExecutionTime(us),SimulationTime(s),Velocity(m/s)");

  // Enable DWT Cycle Counter on Cortex-M4
  DEMCR |= 0x01000000;
  DWT_CYCCNT = 0;
  DWT_CTRL |= 1;

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

  while (t <= t_max) {
      // 1. Snapshot hardware cycles right before solving
      uint32_t step_start = DWT_CYCCNT;
      
      ode_rk4(t, y, h_step, 1, rocket_ode, &params);
      
      // 2. Snapshot hardware cycles exactly after solving
      uint32_t step_end = DWT_CYCCNT;
      
      // 3. nRF52840 runs at exactly 64 MHz, meaning 1us = 64 cycles.
      // This measurement is natively tracked without API/OS overhead.
      uint32_t exec_cycles = step_end - step_start;
      float exec_time_us = (float)exec_cycles / 64.0f;

      // Print out over Native USB CDC via abstraction
      if (step_idx % 10 == 0) {
          Serial.print(exec_time_us, 3);
          Serial.print(",");
          Serial.print(t, 2);
          Serial.print(",");
          Serial.println(y[0], 4);
      }
      
      t += h_step;
      step_idx++;
  }

  Serial.println("DONE");
}

void loop() {
    delay(1000);
}
