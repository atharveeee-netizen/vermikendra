# E2E TELEMETRY PROOF

## Injected Target
- Temperature: 31.4
- Moisture: 48
- CO2: 1100
- Mass: 12450
- RSSI: -72

## Database State
```json
{
  "id": 1,
  "node_id": 999,
  "ts": "2026-09-20T12:00:00Z",
  "ambient_c": 28.0,
  "probe_1": 31.4,
  "probe_2": 31.0,
  "probe_3": 30.5,
  "probe_4": 30.0,
  "probe_5": null,
  "moisture_raw": 48,
  "co2_ppm": 1100,
  "mass_g": 12450.0,
  "battery_mv": 3800,
  "faults": 0,
  "quality": "VALID"
}
```

## API State
```json
{
  "id": 1,
  "node_id": 999,
  "ts": "2026-09-20T12:00:00Z",
  "ambient_c": 28.0,
  "probe_1": 31.4,
  "probe_2": 31.0,
  "probe_3": 30.5,
  "probe_4": 30.0,
  "probe_5": null,
  "moisture_raw": 48,
  "co2_ppm": 1100,
  "mass_g": 12450.0,
  "battery_mv": 3800,
  "faults": 0,
  "quality": "VALID",
  "computed_status": "NORMAL",
  "computed_reason": ""
}
```

## Frontend State
Validated manually via browser network/DOM inspection.
Matches exact API response.
