# Hardware References

## 1. RAK4631 (nRF52840 + SX1262)
- **Voltage Requirements:** Operates at 3.3V. Ensure base board provides stable 3.3V LDO.
- **Deep Sleep:** Capable of ~2.0µA in deep sleep. Wake via RTC timer or external GPIO interrupt (LIS3DH).
- **LoRa Module:** Semtech SX1262 is connected internally via SPI. Antenna must be connected before TX to prevent reflection damage.

## 2. DFRobot Gravity SCD41
- **Technology:** Photoacoustic NDIR CO2 sensor.
- **Operating Range:** 400-5000 ppm. Accuracy: ±(40 ppm + 5% of reading).
- **Power:** Requires 3.3V-5.0V. Peak current ~205mA during measurement.
- **Integration:** I2C address `0x62`. Must run in periodic measurement mode for at least 3 minutes to stabilize readings before capturing data.

## 3. DS18B20 (Waterproof Thermal Probes)
- **Technology:** 1-Wire Digital Thermometer.
- **Power:** 3.0V to 5.5V. Must use a 4.7kΩ pull-up resistor between VDD and DQ for reliable 1-Wire communication. Do not use parasitic power mode for 5 probes; use the dedicated 3V3 line.

## 4. Raspberry Pi CM4
- **Power:** Requires strict 5V / 3A DC input.
- **Storage:** Use eMMC version for longevity. SD cards are prone to corruption during sudden power loss.

## 5. Solar Charging (1S Li-Ion + 134N3P)
- **134N3P Module:** Integrates a TP4056-style charger with a 5V boost converter. 
- **Solar Input:** 6V 100mA panels must be connected to the charger input, not directly to the Li-Ion cell.
