# Vermikendra Application Flow

## 1. Node Telemetry Cycle
- **BOOT:** Load config, self-test.
- **SLEEP:** Radio asleep, `3V3_S` off. Armed on timer (5 min) or LIS3DH tilt interrupt.
- **SAMPLE:** Turn on `3V3_S`. Read DS18B20, SCD41, Moisture.
- **EVALUATE:** Check edge failsafe rules (e.g., if temp > 33°C, actuate misting pump).
- **TX:** Power SX1262, transmit binary payload, open 2s receive window for ACK/commands.

## 2. Respiration Cycle
- **RESP_FLUSH:** Turn on 40mm fan for 120s to flush headspace.
- **RESP_MEASURE:** Turn off fan. Run SCD41 for 600s.
- **CALCULATE:** Fit linear slope of CO2 (ppm/min). Transmit Type 0x02 packet.

## 3. Gateway Data Pipeline
- `vk-radio` decodes LoRa payload and publishes to `vk/{site}/{node}/up`.
- `vk-ingest` writes the reading to the `readings` SQLite table.
- `vk-engine` calculates heat forecasts, wetness index, and respiration normalized indices.

## 4. UI Dashboard Flow
- Operator connects phone to CM4 Hotspot.
- Next.js PWA loads over HTTP.
- WebSocket `/ws/live` streams readings. UI updates thermal gradient heatmap and readiness gauge.
