# Forensic Audit Report (Phase 0)

Date: 2026-09-20
Auditor: Syzygy Engineering Loop

## Methodology
A repository-wide scan was conducted for forbidden patterns indicating technical debt, fabricated execution, and unverified assumptions (`mock`, `fake`, `hardcoded`, `127.0.0.1`, `bin_id = 1`, etc.).

## Findings

### Category B: Configuration Default
*   `analytics/vk_engine.py:12`: `MQTT_BROKER = '127.0.0.1'`
*   `gateway/vk_ingest.py:30`: `mqttc.connect("127.0.0.1", 1883, 60)`
*   **Resolution Plan:** Move to external configuration file / environment variable.

### Category D: Test Fixture
*   `hardware/test-procedures/LORA_INTEROPERABILITY.md:21`: `hardcoded byte array: [0x01, 0xAA...]`
*   **Resolution Plan:** Acceptable in documentation context.

### Category F & H: Accidental Hardcode & Placeholder Math
*   `analytics/vk_engine.py:96-97`: `index_value = slope * 0.5 # placeholder`
*   `analytics/vk_engine.py:135-136`: `bin_id = 1`
*   `gateway/vk_ingest.py:126`: `f"vk/site1/node{node_id}/up"`
*   `firmware/src/main.cpp:42`: `payload.node_id = 1;`
*   **Resolution Plan:** Must be ruthlessly stripped. Bin ID and Site ID must be determined via database relationships and canonical configuration files.

### Category G: Fake Production Telemetry
*   `firmware/src/main.cpp:44`: `payload.batt_mv = 3900; // Mock until ADC wired`
*   `dashboard/src/app/page.tsx:3`: `const mockProbes = [26.1, 28.5, 31.2, 33.4, 29.8];`
*   **Resolution Plan:** Absolutely forbidden. The firmware must return `0xFFFF` for missing ADC. The dashboard must render "Offline" or empty states if no data exists. No fake data on the screen.

## Conclusion
The repository contains critical violations of the Engineering Truth doctrine. Immediate remediation required.
