# Vermikendra Core

> Low-Cost, Multi-Parameter Vermicomposting IoT Node & Offline Gateway for Self-Help Groups (SHGs) and Rural Enterprises.

## Overview
Vermikendra is an off-grid IoT telemetry and decision-support system designed to eliminate silent worm colony collapse, track organic matter degradation kinetics, and guarantee verified compost readiness.

## System Architecture
- **Sensor Node Hardware**: Nordic nRF52840 + Semtech SX1262 LoRa module (RAK4631), 5-point DS18B20 depth temperature array, Sensirion SCD41 photoacoustic NDIR CO2 sensor, Bosch BME688 environmental sensor, 4x 50kg load cells with HX711 ADC.
- **Power Subsystem**: 6V/2W monocrystalline solar panel, TP4056 charge management, 3.7V 3000mAh 18650 Li-ion cell. Ultralow 18 uA sleep current, >7 days zero-sun autonomy.
- **Radio Protocol**: LoRa P2P @ 865.0625 MHz (India license-exempt band), SF9, 125 kHz bandwidth, HMAC-SHA256 authenticated 44-byte binary telemetry frames.
- **Edge Gateway**: Raspberry Pi Compute Module 4 (CM4) with SX1262 LoRa HAT, Mosquitto MQTT broker, FastAPI asynchronous ingestion service, SQLite3 (WAL mode) time-series storage.
- **Offline Operator Dashboard**: React/Vite Progressive Web App (PWA) served over the gateway's standalone 802.11 b/g/n WiFi hotspot (192.168.4.1), localized in Gujarati, Hindi, and English.

## Extent of AI Tools Usage
- **AI-Assisted (30%)**: Documentation formatting, visual graphic artifacts, and mathematical modeling (1D thermal diffusion PDE, Gompertz respiration curve fitting).
- **Teammate-Engineered (70%)**: C++ firmware architecture, hardware schematic design, circuit assembly, LoRa daemon, SQLite persistence schema, and offline PWA frontend.

## License
MIT License - Team Vermikendra
