#include "sensors.h"
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SensirionI2CScd4x.h>

OneWire oneWire(PIN_1WIRE);
DallasTemperature ds18b20(&oneWire);
SensirionI2CScd4x scd4x;

void sensors_init() {
    pinMode(PIN_3V3_S, OUTPUT);
    digitalWrite(PIN_3V3_S, LOW); // Off by default
}

void sensors_power_on() {
    digitalWrite(PIN_3V3_S, HIGH);
    delay(100); // Allow rails to stabilize
    Wire.begin();
    ds18b20.begin();
    scd4x.begin(Wire);
    
    // Attempt SCD41 initialization
    uint16_t error;
    char errorMessage[256];
    scd4x.stopPeriodicMeasurement();
    error = scd4x.startPeriodicMeasurement();
}

void sensors_power_off() {
    scd4x.stopPeriodicMeasurement();
    Wire.end();
    digitalWrite(PIN_3V3_S, LOW);
}

void sensors_read_all(PayloadType0x01* payload) {
    // 1. Read DS18B20 Array
    ds18b20.requestTemperatures();
    for (int i = 0; i < 5; i++) {
        float tempC = ds18b20.getTempCByIndex(i);
        if (tempC == DEVICE_DISCONNECTED_C || tempC == 85.0) {
            payload->t_probe[i] = SENSOR_FAULT_INT16;
            payload->fault_bits |= (1 << i);
        } else {
            payload->t_probe[i] = (int16_t)(tempC * 100);
        }
    }

    // 2. Read Moisture
    int raw_adc = analogRead(PIN_MOISTURE);
    payload->moisture_raw = raw_adc;

    // 3. Read SCD41 (Wait for data ready)
    uint16_t co2 = 0;
    float temp = 0.0f;
    float rh = 0.0f;
    bool dataReady = false;
    uint16_t error = scd4x.getDataReadyFlag(dataReady);
    
    if (!error && dataReady) {
        error = scd4x.readMeasurement(co2, temp, rh);
        if (!error) {
            payload->co2_last = co2;
            payload->t_ambient = (int16_t)(temp * 100);
            payload->rh = (uint16_t)(rh * 100);
        } else {
            payload->co2_last = SENSOR_FAULT_UINT16;
            payload->fault_bits |= (1 << 5);
        }
    } else {
        payload->co2_last = SENSOR_FAULT_UINT16;
        payload->fault_bits |= (1 << 5);
    }
}
