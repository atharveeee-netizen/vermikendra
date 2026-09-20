#pragma once
#include <Arduino.h>

// ---------------------------------------------------------
// HARDWARE PIN MAPPINGS (From Phase 5)
// ---------------------------------------------------------
#ifndef WB_IO1
  #define WB_IO1 1
  #define WB_IO2 2
  #define WB_IO3 3
  #define WB_IO4 4
  #define WB_IO5 5
  #define WB_A1  A1
  #define PIN_LORA_NSS 8
  #define PIN_LORA_DIO_1 9
  #define PIN_LORA_RESET 10
  #define PIN_LORA_BUSY 11
#endif
#define PIN_3V3_S       WB_IO2      // Power control for sensors
#define PIN_1WIRE       WB_IO1      // DS18B20 Array (Needs physical 4.7k pullup)
#define PIN_TILT_INT    WB_IO3      // LIS3DH Interrupt
#define PIN_FAN_CTRL    WB_IO4      // Flush Fan MOSFET
#define PIN_PUMP_CTRL   WB_IO5      // Misting Pump MOSFET
#define PIN_MOISTURE    WB_A1       // Capacitive Moisture ADC

// ---------------------------------------------------------
// DATA CONTRACT (From Phase 4)
// ---------------------------------------------------------
#define SENSOR_FAULT_INT16  0x8000
#define SENSOR_FAULT_UINT16 0xFFFF

// Type 0x01 Payload (44 Bytes exact, packed)
#pragma pack(push, 1)
struct PayloadType0x01 {
    uint8_t  version_type = 0x01;
    uint16_t node_id;
    uint16_t seq;
    uint8_t  flags;
    uint16_t age_s;
    uint16_t batt_mv;
    int16_t  t_probe[5];    // 0.01 C
    int16_t  t_ambient;     // 0.01 C
    uint16_t rh;
    uint16_t pressure;
    uint32_t gas_res;
    uint16_t moisture_raw;
    int32_t  mass;
    uint16_t co2_last;
    uint8_t  fault_bits;
    int8_t   rssi_last_ack;
    uint8_t  hmac_tag[4];
};
#pragma pack(pop)
