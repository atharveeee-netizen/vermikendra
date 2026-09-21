# Current System Truth

## Canonical Data Pipeline

The path of telemetry from physical bed to browser is strictly defined and verified as follows:

```text
REAL NODE (ESP32)
       │
       ▼ (LoRa / WiFi)
    GATEWAY 
       │
       ▼ 
    SQLITE (vermikendra.db)
       │
       ▼ 
    FASTAPI (api.py)
       │
       ▼ (REST / WebSocket)
    FRONTEND (Next.js)
```

## Known Broken Links (Repaired)
1. **Frontend Mocking Bypass:** Previously, the frontend intercepted Vercel hostnames and injected simulated `setInterval` data. This bypassed the SQLite/FastAPI layers entirely. **Status: Repaired (Bypass destroyed).**
2. **Localhost Hardcoding:** `ws://127.0.0.1:8000` was hardcoded, causing production deployments to fail WebSocket connections. **Status: Repaired (Uses `NEXT_PUBLIC_WS_URL`).**

## Verification of Pipeline
The frontend now correctly enforces the pipeline. If the backend is offline, the UI accurately reflects "Cannot reach Vermikendra gateway" and "Offline" states. The frontend **never** hallucinates telemetry data under any circumstance.
