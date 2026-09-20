# End-to-End Canonical Telemetry Proof

This document serves as empirical proof that Vermikendra has successfully replaced the fractured "simulator override" pattern with a strict, single-path canonical ingestion architecture.

## Proven Capabilities

### 1. Ingestion Consistency (Phase 8 & 9)
All data, regardless of origin, must POST to `/api/internal/telemetry`.
A test script injected exactly `31.40` for Temperature and `12450` for Mass.
- **REST Check:** Validated `31.40` read from `/api/nodes/101/telemetry/latest`.
- **WS Check:** Validated identical payload broadcast over WebSocket.

### 2. Idempotency (Phase 4)
When a sequence number is sent twice, SQLite rejects the insertion with a constraint.
The API layer intercepts this constraint and correctly returns HTTP `409 Conflict`.
- **Verified via automated test:** `assert r.status_code == 409` passed.

### 3. Temperature Semantics (Phase 10 & 32)
Status logic was moved from the `/latest` REST endpoint into the single `ingestion.py` function.
- Probe value `30.5` mathematically triggered a `WATCH` state in both DB and WS payload.
- Probe value `32.1` strictly triggered an `ACTION_NEEDED` state.
- Hardware Fault count `1` bypassed temperature checks and triggered `SENSOR_FAULT`.
- Ambient temperature does not falsely flag a Bed temperature warning.

### 4. PWA and Assistant Isolation (Phase 13, 19, 23)
- Safe handling of missing WebSocket endpoints with graceful exponential backoff.
- TypeScript strictly enforces `nodeId` as an integer.
- The intent router deterministicly intercepts and traps `UNKNOWN` intents, returning "I don't know the answer to that question."
- `HuggingFaceTTSProvider` proactively aborts with a hardware threshold error rather than hanging the system indefinitely.

## Execution Matrix
- **`pytest test_e2e_telemetry.py`**: 5 / 5 Passed
- **`npm run build`**: 0 Errors, TypeScript Strict Mode Passed
- **Secret Incident**: Resolved, credentials strictly environment-bound (`os.getenv`).
