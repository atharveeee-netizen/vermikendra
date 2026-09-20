import os
import sqlite3
import traceback

os.environ['VK_DB_PATH'] = 'vermikendra_validation.db'

# Initialize Schema
with sqlite3.connect('vermikendra_validation.db') as conn:
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())

from core.ingestion import ingest_telemetry_payload

payload = {
    "node": 101,
    "seq": 1,
    "probes_c": [31.40, 31.0, 30.5, 30.0, None],
    "ambient_c": 24.20,
    "rh_pct": 55.0,
    "co2_ppm": 1100,
    "mass_g": 12450,
    "rssi": -72,
    "faults": 0,
    "ts": "2026-09-20T12:00:00Z"
}

try:
    res = ingest_telemetry_payload(payload)
    print("SUCCESS:", res)
except Exception as e:
    print("FAILED:", e)
    traceback.print_exc()
