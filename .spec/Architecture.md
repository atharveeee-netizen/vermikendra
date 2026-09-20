# Vermikendra System Architecture

```mermaid
graph TD
    subgraph "Edge Node (RAK4631)"
        S[Sensors: 5xDS18B20, SCD41, Moisture] --> N(Node MCU)
        N -- "LoRa 865MHz P2P" --> G1
    end

    subgraph "Gateway (CM4)"
        G1(SX1262 LoRa HAT) -->|Serial| R[vk-radio]
        R -->|MQTT| I[vk-ingest]
        I --> DB[(SQLite WAL)]
        R -->|MQTT| E[vk-engine]
        E --> DB
        DB --> A[vk-api FastAPI]
        A -->|WebSocket/REST| PWA
    end

    subgraph "Operator"
        PWA[Offline Next.js PWA]
    end
```

## Contracts
- **Node-to-Gateway:** Custom binary payload over LoRa P2P (No LoRaWAN). 
- **Gateway Services:** Communicate purely via Mosquitto MQTT over `localhost`.
- **Database:** Strict SQLite schema (defined in `Schema.md`).
- **Dashboard:** Communicates via REST for historical data and WebSocket for real-time telemetry.
