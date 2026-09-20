#include <Arduino.h>
#include <RadioLib.h>
#include "config.h"
#include "sensors.h"

// SX1262 setup on RAK4631
SX1262 radio = new Module(PIN_LORA_NSS, PIN_LORA_DIO_1, PIN_LORA_RESET, PIN_LORA_BUSY);

RTC_DATA_ATTR uint16_t seq_num = 0; // Persists in deep sleep

void setup() {
    Serial.begin(115200);
    
    // Initialize Hardware
    sensors_init();
    pinMode(PIN_FAN_CTRL, OUTPUT);
    pinMode(PIN_PUMP_CTRL, OUTPUT);
    digitalWrite(PIN_FAN_CTRL, LOW);
    digitalWrite(PIN_PUMP_CTRL, LOW);

    // Initialize Radio
    Serial.print(F("[SX1262] Initializing ... "));
    int state = radio.begin(LORA_FREQ, LORA_BW, LORA_SF, LORA_CR, LORA_SYNC_WORD, LORA_TX_POWER);
    if (state == RADIOLIB_ERR_NONE) {
        Serial.println(F("success!"));
    } else {
        Serial.print(F("failed, code "));
        Serial.println(state);
        while (true);
    }
}

void loop() {
    // ---------------------------------------------------------
    // STATE: SAMPLE
    // ---------------------------------------------------------
    Serial.println("STATE: SAMPLE");
    sensors_power_on();
    delay(5000); // Allow SCD41 to spin up (simulate blocking wait for real firmware)
    
    PayloadType0x01 payload = {};
#ifdef VK_NODE_ID
    payload.node_id = VK_NODE_ID;
#else
    payload.node_id = 0xFFFF; // Explicit unconfigured fault state
#endif
    payload.seq = seq_num++;
    payload.batt_mv = SENSOR_FAULT_UINT16; // Explicit fault until physical ADC is wired
    
    sensors_read_all(&payload);
    sensors_power_off();

    // ---------------------------------------------------------
    // STATE: EVALUATE (Failsafe Rules)
    // ---------------------------------------------------------
    Serial.println("STATE: EVALUATE");
    bool critical_heat = false;
    for (int i=0; i<5; i++) {
        if (payload.t_probe[i] != SENSOR_FAULT_INT16 && payload.t_probe[i] >= 3300) {
            critical_heat = true;
        }
    }
    if (critical_heat) {
        Serial.println("FAILSAFE: Triggering Misting Pump!");
        digitalWrite(PIN_PUMP_CTRL, HIGH);
        delay(2000); // Mist for 2s
        digitalWrite(PIN_PUMP_CTRL, LOW);
    }

    // ---------------------------------------------------------
    // STATE: TX
    // ---------------------------------------------------------
    Serial.println("STATE: TX");
    int state = radio.transmit((uint8_t*)&payload, sizeof(payload));
    if (state == RADIOLIB_ERR_NONE) {
        Serial.println(F("TX success!"));
    }

    // ---------------------------------------------------------
    // STATE: SLEEP
    // ---------------------------------------------------------
    Serial.println("STATE: SLEEP");
    radio.sleep();
    
    // Simulate deep sleep delay
    delay(60000); 
}
