# RED TEAM VALIDATION

Previous implementation claims are UNVERIFIED until independently tested.

| Component           | Claimed | Proven | Evidence |
| ------------------- | ------- | ------ | -------- |
| Database bootstrap  | VERIFIED | PROVEN | WAL: True, FK: True, Tables: 5, Rows: 0. |
| Telemetry ingestion | VERIFIED | PROVEN | Simulator injection reached MQTT -> DB. |
| API                 | VERIFIED | PROVEN | API reflects exact injected simulation values. |
| WebSocket           | ?       | ?      |          |
| Frontend            | VERIFIED | PROVEN | Zero-state handles empty sites safely. |
| PWA                 | ?       | ?      |          |
| Voice STT           | VERIFIED | PROVEN | Safely returns STT_NOT_CONFIGURED when key absent. |
| Assistant context   | VERIFIED | PROVEN | Rejects unknown intents ("how to prepare for rain"). |
| TTS                 | UNVERIFIED | BLOCKED| Hardware benchmark required on Pi CM4. |
| Simulation          | VERIFIED | PROVEN | 'SIMULATION' badge appears for SIM-* nodes. |
| Hardware            | ?       | ?      |          |
