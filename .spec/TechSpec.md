# Vermikendra Technical Specification (TechSpec)

## 1. Hardware Stack (Edge Node)
- **MCU & Radio:** RAK4631 WisBlock Core (nRF52840 + SX1262 LoRa, IN865).
- **Sensors:** 
  - 5x DS18B20 (Waterproof thermal gradient).
  - DFRobot Gravity SCD41 (CO2 for respiration).
  - BME688 (Headspace environmental).
  - LIS3DH (Lid tilt wake interrupt).
  - Capacitive soil moisture.
  - HX711 (M5Stack Weight I2C Unit).
- **Power:** 6V 100mA solar panel, 134N3P charger, 1S Li-Ion cell.
- **Enclosure:** IP65 box with ePTFE breathable vent patch to block liquid water.

## 2. Gateway Stack (Central Hub)
- **Compute:** Raspberry Pi CM4 (2GB RAM, 32GB eMMC).
- **Radio Receiver:** Waveshare SX1262 868M LoRa HAT (UART over USB).
- **Software Daemon:** Python 3.11 offline services (vk-radio, vk-ingest, vk-engine, vk-api).
- **Database:** SQLite (WAL mode).
- **Messaging:** Mosquitto MQTT.

## 3. Frontend Stack (Dashboard)
- **Framework:** Next.js / React (Offline PWA).
- **API:** FastAPI + WebSocket.
- **Network:** CM4 acts as a Wi-Fi Hotspot (`vermikendra.local`, `10.42.0.1`).
