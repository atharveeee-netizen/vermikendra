# POST-FARMER-UX BASELINE

## System State
*   **Commit:** `15953850772f19010972b88c58588f0ad92c06d8`
*   **Branch:** `main`
*   **Node.js:** `v24.14.1`
*   **npm:** `11.11.0`
*   **Python:** `3.10.11`

## Frontend Dependencies
*   **Next.js:** `16.3.5`
*   **React:** `19.2.8`
*   **TailwindCSS:** `4.3.3`
*   **next-pwa:** `5.6.0`

## Backend Dependencies
*   **FastAPI:** `0.141.1`
*   **uvicorn:** `0.49.0`
*   **websockets:** `16.1.1`
*   **paho-mqtt:** `2.1.0` (approx, handled by system)
*   **requests:** `2.34.2`

## Implementation Status
*   **IMPLEMENTED:** Farmer-first UX prototype, Sarvam STT/TTS API gateway structure.
*   **PARTIAL:** SQLite DB schema (exists but unmigrated/hardcoded querying), Voice state machine.
*   **UNVERIFIED:** Real telemetry pipeline through WebSocket in adverse conditions, PWA installability, HuggingFace TTS.
*   **BLOCKED:** Physical RAK4631 telemetry testing.
*   **PLANNED:** Multi-site entity routing, pure API-driven telemetry, Sarvam language contexts.
