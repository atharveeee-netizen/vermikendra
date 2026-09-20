# Vermikendra Architecture Decision Log

| Date | Decision | Rationale | State |
| :--- | :--- | :--- | :--- |
| 2026-09-20 | Offline-First Architecture | Rural compost environments lack stable internet. All processing (analytics, dashboard, LoRa ingestion) must occur on the local CM4 gateway. | Approved |
| 2026-09-20 | SQLite WAL Mode | Simultaneous write (LoRa packet ingestion) and read (PWA WebSocket stream) required. | Approved |
| 2026-09-20 | No Deep Learning for V1 | Respiration rate slope and thermal gradient are deterministically computable using classical statistics. ML is blocked until real sensor data is collected. | Approved |
| 2026-09-20 | Dedicated Vermikendra Repository | Previous attempts to map onto Beevil Knievel (`sih`) caused confusion and mixed artifacts. Cloned dedicated repo to ensure clean engineering truth. | Approved |
