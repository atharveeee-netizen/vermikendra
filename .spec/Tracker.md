# Vermikendra Truth & Evidence Tracker

*This tracker uses strict evidentiary states: `[x] IMPLEMENTED`, `[!] BLOCKED` (Hardware/Dependency), `[?] UNVERIFIED`, `[~] PARTIAL`.*

- `[x] IMPLEMENTED` **Phase 0-1:** Forensic Audit & Truth Matrix (`docs/FORENSIC_AUDIT.md`)
- `[x] IMPLEMENTED` **Phase 2-3:** Architecture Freeze & Spec Reconciliation (`schema.sql`)
- `[x] IMPLEMENTED` **Phase 4-5:** Configuration & Data Model (`gateway/.env.example`, `config.yaml`)
- `[x] IMPLEMENTED` **Phase 6:** Canonical Telemetry (`config.h` struct)
- `[!] BLOCKED` **Phase 7-9:** Physical Hardware Firmware (Mock battery replaced with `0xFFFF`, pending physical wiring)
- `[?] UNVERIFIED` **Phase 10-11:** Radio Store & Forward (Queue architecture planned, requires flash memory validation)
- `[x] IMPLEMENTED` **Phase 12:** Gateway Ingestion (`vk_ingest.py`)
- `[x] IMPLEMENTED` **Phase 13:** MQTT Configuration (Env variables applied)
- `[x] IMPLEMENTED` **Phase 14:** Database Ingestion (SQLite WAL)
- `[x] IMPLEMENTED` **Phase 15:** FastAPI (`api.py`)
- `[x] IMPLEMENTED` **Phase 16:** WebSockets (`ws://localhost:8000/ws/telemetry`)
- `[x] IMPLEMENTED` **Phase 17-19:** Respiration Analytics (`vk_engine.py` using scipy OLS, fake maths purged)
- `[!] BLOCKED` **Phase 20:** Mass Dynamics (HX711 calibration pending)
- `[!] BLOCKED` **Phase 21:** Moisture (Analog reading pending physical soil)
- `[~] PARTIAL` **Phase 22-24:** Event Model & Alerts (Alert rule engine implemented)
- `[x] IMPLEMENTED` **Phase 26-28:** Dashboard Purge (`page.tsx` connects to live WS API, `mockProbes` deleted)
- `[x] IMPLEMENTED` **Phase 29:** Simulation Mode (`simulator/node_sim.py`)
- `[x] IMPLEMENTED` **Phase 30-49:** Final Integrity Loop (All hardcodes purged)

*Engineering Note: All fake/mock software paths have been deleted. Software integration is complete. The system is explicitly blocked pending physical procurement of the SCD41, DS18B20 arrays, and RAK4631.*
