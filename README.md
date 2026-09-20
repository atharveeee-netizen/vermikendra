# Vermikendra 

A scientific vermicompost telemetry and agricultural monitoring system designed explicitly for zero-literacy usability, off-grid resilience, and deterministic ground-truth sensing.

## The Principle

*   **No "AI Slop":** The system never attempts to sound "smart". It delivers binary state data (e.g., "The bed is too hot") using deterministic rule engines.
*   **Zero UI Density:** The farmer sees *only* the state of the active bed, with large typography, bold colors, and an ambient voice interface. No graphs, no dashboards, no complex menus.
*   **Hardware Ground-Truth:** The frontend is completely stateless and dumb. It only renders exactly what the SQLite database proves was received from a physical LoRaWAN/Serial node.

## Status & Validation

> [!IMPORTANT]
> The claims in this repository are strictly audited. Claims without empirical proof are marked `UNVERIFIED` or `PLANNED`.

### Hardware & Firmware
*   [UNVERIFIED] **Firmware:** C++ based bare-metal edge nodes (RAK4631/nRF52). 
*   [UNVERIFIED] **RF Range:** LoRaWAN field transmission. (Blocked pending physical field test).
*   [UNVERIFIED] **Power:** 18-month battery life. 
*   [IMPLEMENTED] **Ingestion Contract:** Binary frame format (44 bytes) mapped in `vk_ingest.py`.

### Gateway & Backend
*   [VALIDATED] **Database:** SQLite WAL mode with strict foreign keys.
*   [VALIDATED] **API:** FastAPI REST and WebSocket bridge for local edge operation.
*   [VALIDATED] **Offline Mode:** The Gateway functions without internet, serving localized DB state.
*   [VALIDATED] **Voice STT:** Safe fallback when Sarvam API is unavailable.
*   [UNVERIFIED] **Voice TTS:** HuggingFace on-device TTS. (Blocked pending Raspberry Pi CM4 benchmark).

### Frontend (PWA)
*   [VALIDATED] **Farmer-First UX:** 1-tap multilingual voice invocation, no dense menus.
*   [VALIDATED] **Zero-State Resilience:** Explicitly handles empty databases without faking metrics.
*   [VALIDATED] **Offline Reconnection:** Exponential backoff for WebSockets.

## Local Simulator Setup

1. Run the Gateway:
   ```bash
   cd gateway
   python -m venv venv
   source venv/bin/activate # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python api.py         # Starts FastAPI on port 8000
   ```
2. Run the Dashboard:
   ```bash
   cd dashboard
   npm install
   npm run dev           # Starts Next.js on port 3000
   ```
3. Run the Simulator (to inject deterministc telemetry directly into the DB):
   ```bash
   cd gateway
   python test_phase7_inject.py
   ```
