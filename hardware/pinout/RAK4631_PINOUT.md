# RAK4631 WisBlock Edge Node Pinout

This document defines the strict physical pin mappings for the Vermikendra edge node. The C++ firmware (Phase 6) MUST use these exact macro definitions.

## 1. I2C Bus (Sensors)
The primary `Wire` bus connects the digital sensors.
- **SDA:** `WB_I2C1_SDA`
- **SCL:** `WB_I2C1_SCL`
- **Devices on Bus:**
  - `0x62`: SCD41 (CO2)
  - `0x77`: BME688 (Temp/Humidity/Gas)
  - `0x48`: TMP117 (High-Precision Reference Temp)
  - `0x28`: HX711 via M5Stack I2C wrapper (Mass)

## 2. 1-Wire Bus (Thermal Gradient)
The DS18B20 probes use the 1-Wire protocol, requiring a pull-up resistor.
- **DQ (Data):** `WB_IO1`
- **Power:** Connect the VDD line of all 5 probes to `3V3_S` (the software-controlled 3.3V power domain). Do not use parasitic power.
- **Pull-up:** Connect a physical 4.7kΩ resistor between `WB_IO1` and `3V3_S`.

## 3. GPIO Interrupts
To wake the nRF52840 from deep sleep without polling.
- **Lid Tilt Interrupt:** `WB_IO3`. The LIS3DH INT1 pin connects here. Triggered when the lid tilts > 30°.

## 4. Analog Inputs
- **Capacitive Moisture Sensor:** `WB_A1`. Analog voltage must not exceed the ADC reference limit (typically VDD/Internal Ref).

## 5. Software Power Control
The WisBlock base board features a software-controllable power rail (`3V3_S`) to completely kill power to sensors during deep sleep.
- **Control Pin:** `WB_IO2`. Write `HIGH` to power sensors, `LOW` to kill power.

## 6. Actuators
- **5V Flush Fan Relay / MOSFET:** `WB_IO4`. The firmware toggles this pin during the `RESP_FLUSH` cycle.
- **Misting Pump Relay / MOSFET:** `WB_IO5`.

---
*Note: Any changes to these pin assignments must be propagated to `firmware/src/config.h`.*
