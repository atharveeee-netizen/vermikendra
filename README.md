# Vermikendra 🪱

**Vermikendra** is an autonomous, completely offline, scientific vermicompost monitoring system. It replaces guesswork with deterministic biology and classical mathematics.

This repository was designed and engineered entirely from scratch by **SYZYGY** based on an initial Technical Requirements Document. It prioritizes "Engineering Truth"—meaning no cloud dependencies, no AI black boxes without real data, and hardware-aware fail-safes.

## The Architecture

The system consists of three distinct layers operating completely off-grid:

1. **The Edge Node (`firmware/`)**
   - **Hardware:** RAK4631 (nRF52 + SX1262 LoRa).
   - **Sensors:** 5x DS18B20 1-Wire Thermal Array, SCD41 (CO2), Capacitive Moisture.
   - **Role:** Wakes up, powers the sensors, reads them, packs a strict 44-byte binary frame, transmits via LoRa, and returns to a 2.0µA deep sleep. If it detects a thermal cascade ($\ge 33^\circ C$), it bypasses the Gateway and directly triggers a local misting pump.
   - **Code:** C++ / PlatformIO.

2. **The Gateway Intelligence (`gateway/` & `analytics/`)**
   - **Hardware:** Raspberry Pi CM4 + Waveshare LoRa HAT.
   - **Role:** Receives raw LoRa frames via UART. `vk_ingest.py` mathematically unpacks the 44-byte payload and stores it in an immutable SQLite WAL database. `vk_engine.py` consumes the stream via MQTT and runs SciPy Ordinary Least Squares (OLS) linear regression on the CO2 data to calculate the respiration slope ($R^2 \ge 0.90$).
   - **Code:** Python 3 (scipy, pyserial, paho-mqtt, sqlite3).

3. **The Offline Dashboard (`dashboard/`)**
   - **Hardware:** Any rural operator's smartphone connected to the Pi's local Wi-Fi hotspot (`vermikendra.local`).
   - **Role:** An aggressively cached Next.js Progressive Web App (PWA). Displays the current thermal gradient and the mathematical compost readiness (CO2 slope) in high-contrast (`vk-good`, `vk-warning`, `vk-critical`) tailored for direct sunlight.
   - **Code:** Next.js / Tailwind CSS / React.

## Getting Started

Because Vermikendra is designed for offline deployment, there is no "Cloud Setup". 

1. **Firmware:** Open `firmware/` in PlatformIO and flash to the RAK4631.
2. **Gateway:** Run `python3 gateway/vk_ingest.py` and `python3 analytics/vk_engine.py` as `systemd` services on the Raspberry Pi.
3. **Dashboard:** Run `npm run build && npm start` in `dashboard/` to serve the Next.js UI over the Pi's local network.

## Documentation
*   [Data Contract](docs/DATA_CONTRACT.md): The strict schema and fault logic.
*   [Hardware Pinout](hardware/pinout/RAK4631_PINOUT.md): The physical `WB_` pin mappings.
*   [Failure Modes (FMEA)](docs/FAILURE_MODES.md): How the system survives physical decay.
*   [Security Audit](docs/SECURITY_AUDIT.md): The threat model of an open Wi-Fi hotspot in an agricultural field.

---
*Engineered by Syzygy for the Vermikendra Project.*
