# Implementation Truth Matrix (Phase 1)

**Absolute Rule:** We do not claim features are implemented unless physical/executable evidence exists.

| Component | Source | Specified | Implemented | Tested | Hardware Required | Evidence | Status | Remaining Work |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DS18B20 | `sensors.cpp` | Yes | Yes (Mocked) | No | Yes | Mock `getTempCByIndex` | **UNVERIFIED** | Strip hardcoded 85.0 failsafe, write actual read loop. |
| SCD41 | `sensors.cpp` | Yes | Yes | No | Yes | Basic read loop | **UNVERIFIED** | Implement true data-ready blocking. |
| BME688 / LIS3DH | `sensors.cpp` | Yes | No | No | Yes | None | **PLANNED** | Write physical driver implementation. |
| HX711 (Mass) | Firmware | Yes | No | No | Yes | None | **PLANNED** | Write physical driver. |
| Battery ADC | `main.cpp` | Yes | No (Fake) | No | Yes | `batt_mv = 3900` | **BLOCKED** | Strip fake data. Return `0xFFFF` fault. |
| LoRa (SX1262) | `main.cpp` | Yes | Yes | No | Yes | `RadioLib` import | **UNVERIFIED** | Awaiting interoperability Spike Test. |
| HMAC Authentication | `vk_ingest.py` | Yes | No | No | No | 44-byte struct | **PLANNED** | Implement SHA256/HMAC signature check. |
| SQLite WAL | `schema.sql` | Yes | Yes | Yes | No | `PRAGMA journal_mode=WAL` | **IMPLEMENTED** | Add dynamic Site/Bin relationships. |
| FastAPI | `api.py` | Yes | No | No | No | None | **PLANNED** | Build read-only REST interface. |
| WebSocket | `api.py` | Yes | No | No | No | None | **PLANNED** | Build MQTT->WS pipeline. |
| Respiration Analytics | `vk_engine.py` | Yes | Yes (Partial)| No | No | `scipy.stats.linregress` | **PARTIALLY_VALIDATED** | Strip `slope*0.5` placeholder. |
| Offline PWA | `dashboard/` | Yes | Yes (Mocked)| No | No | `page.tsx` fake UI | **PARTIALLY_VALIDATED** | Strip `mockProbes`. Connect to WebSocket. |
| Simulation | `simulator/` | Yes | No | No | No | None | **PLANNED** | Build deterministic node simulator. |

*This matrix drives the execution logic for the repair phases. Hardware-dependent items are explicitly marked UNVERIFIED/BLOCKED pending physical procurement.*
