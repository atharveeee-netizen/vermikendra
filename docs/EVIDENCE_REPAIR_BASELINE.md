# Vermikendra Evidence Repair Baseline

**Date**: 2026-09-21
**Commit**: 115b30e chore: remove venv from tracking
**Branch**: main
**Python Version**: 3.10
**Node Version**: v20+ (assumed via project usage)

## State of the Repository
The previous loop structurally decoupled the frontend from hardcoded fallbacks and replaced MQTT with an internal HTTP telemetry ingest. 
However, the `api.py` HTTP ingest still only broadcasts over WebSockets and does NOT persist to the database. Simulator bypasses the database. This breaks canonical tracking.

## Known Failures (Phase 0 Audit)
1. `/api/internal/telemetry` does not persist telemetry to SQLite.
2. `vk_ingest.py` reads from Serial but does not implement sequence/duplicate handling correctly.
3. Tests rely on explicitly manipulating SQLite to bypass `vk_ingest`.
4. `test_phase7_inject.py` fakes E2E integration by dual-writing.
5. Missing unified ingestion logic.

All 49 Truth Reconciliation phases will be executed to correct this.
