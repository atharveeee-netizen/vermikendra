# VERMIKENDRA TRACKER

## COMPLETED
- `[x]` **Hardware Node Integration:** Defined 44-byte struct formats, ingestion unpacking, and DB writing (`vk_ingest.py`).
- `[x]` **Database Bootstrap:** SQLite WAL enabled, schema defined, migrations scripted (`db.py`, `schema.sql`).
- `[x]` **API Gateway:** FastAPI initialized. Added endpoints for Site/Bin/Node Discovery and Latest Telemetry.
- `[x]` **Status Engine:** Computes ACTION_NEEDED, WATCH, NORMAL deterministically on the backend to avoid UI calculation drift.
- `[x]` **WebSocket Broadcast:** Live streaming of MQTT payloads to active PWA clients with exponential backoff on reconnect.
- `[x]` **Voice Assistant Architecture:**
    - STT configured for multi-lingual input (hi-IN, gu-IN, en-IN).
    - Extracted Context Builder to pull from active DB telemetry.
    - Extracted Intent Router for hardcoded, safe routing to bypass LLMs.
    - TTS Abstracted (Sarvam working, HuggingFace stubbed for future).
- `[x]` **Frontend:**
    - Zero-UI Density Farmer-first design. No gradients, large text, big status blocks.
    - Deeply modularized (`/hooks`, `/services`, `/types`).
    - PWA configuration established.
    - Purged ALL hardcoded values (IDs, farmer names, localhost domains). Driven purely by `NEXT_PUBLIC_API_BASE_URL`.

## PENDING / UNVERIFIED
- `[ ]` **HuggingFace Local Fallback:** Needs physical hardware testing (Raspberry Pi/Low-end Android) to verify inference speed. Currently marked `[?] UNVERIFIED`.
- `[ ]` **LoRaWAN Range Test:** The system logic works, but actual RF distances in dense canopy need field testing.
- `[ ]` **PWA Offline Service Worker Deep Test:** Next-PWA is active, but offline cache invalidation behavior with telemetry WebSockets needs auditing on real mobile browsers.
