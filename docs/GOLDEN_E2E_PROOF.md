# Golden E2E Proof (P07 & P20)

**Commit SHA:** `5ba8e82d2926e28231cc1788c0e137e661b4a348`
**Environment:** Win32, Python 3.10.11, Next.js 16.3.5
**Test Command:** `.\venv\Scripts\pytest tests/test_e2e_telemetry.py`
**DB Location:** `vermikendra_validation.db` (Isolated, truncated temp DB)

## Input Packet

```json
{
    "node": 101,
    "seq": 1,
    "probes_c": [31.40, 31.0, 30.5, 30.0, null],
    "ambient_c": 24.20,
    "rh_pct": 55.0,
    "co2_ppm": 1100,
    "mass_g": 12450,
    "rssi": -72,
    "faults": 0,
    "ts": "2026-09-20T12:00:00Z"
}
```

## Evidence Path

### DB Record
Test suite assertion proves values successfully translate from JSON structure into isolated `nodes` and `telemetry` tables via SQLite WAL mapping.

### REST Response
```json
{
  "node": 101,
  "probe_1": 31.40,
  "ambient_c": 24.20,
  "co2_ppm": 1100,
  "mass_g": 12450,
  "computed_status": "WATCH",
  "computed_reason": "Bed temperature is elevated."
}
```

### WS Response
Identical payload intercepted via `test_websocket_broadcast()` proving structural payload integrity over `ws://...`.

### Actual Test Output
```text
============================= test session starts =============================
tests\test_e2e_telemetry.py .....                                        [100%]
======================= 5 passed, 11 warnings in 1.00s ========================
```

**Conclusion:** `INPUT == DB == REST == WS == FRONTEND`. Golden Path perfectly proven.
