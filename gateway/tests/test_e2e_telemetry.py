import os
import time
import json
import sqlite3
import pytest
from fastapi.testclient import TestClient

# 1. Setup isolated DB BEFORE importing API (Phase 7)
TEST_DB = "vermikendra_validation.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
os.environ['VK_DB_PATH'] = TEST_DB

import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# Initialize Schema
with sqlite3.connect(TEST_DB) as conn:
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
        
from api import app
from core.ingestion import IngestionError

client = TestClient(app)

def test_empty_state():
    """Phase 7 - Clean Database Test"""
    r = client.get("/api/sites")
    assert r.json() == []

def test_canonical_ingestion():
    """Phase 8 & 9 - True E2E Test & Exact Value Consistency"""
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

    # 1. Ingest via identical entrypoint
    r = client.post("/api/internal/telemetry", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "broadcasted"

    # 2. Verify REST API representation
    r = client.get("/api/nodes/101/telemetry/latest")
    assert r.status_code == 200
    data = r.json()
    assert data["probe_1"] == 31.40
    assert data["ambient_c"] == 24.20
    assert data["co2_ppm"] == 1100
    assert data["mass_g"] == 12450
    assert data["computed_status"] == "WATCH" # > 30.0

def test_idempotency():
    """Phase 4 - Idempotency"""
    payload = {
        "node": 101,
        "seq": 1, # Duplicate
        "probes_c": [31.40],
        "faults": 0
    }
    r = client.post("/api/internal/telemetry", json=payload)
    assert r.status_code == 409
    assert r.json()["status"] == "duplicate"

def test_temperature_semantics():
    """Phase 10 - Temperature Semantics"""
    # > 32.0 -> ACTION_NEEDED
    r = client.post("/api/internal/telemetry", json={
        "node": 101, "seq": 2, "probes_c": [32.1], "faults": 0
    })
    assert r.status_code == 200
    r2 = client.get("/api/nodes/101/telemetry/latest")
    assert r2.json()["computed_status"] == "ACTION_NEEDED"
    
    # Faults
    r = client.post("/api/internal/telemetry", json={
        "node": 101, "seq": 3, "probes_c": [28.0], "faults": 1
    })
    r2 = client.get("/api/nodes/101/telemetry/latest")
    assert r2.json()["computed_status"] == "SENSOR_FAULT"

def test_websocket_broadcast():
    """Phase 3 - Ensure WebSocket emits identical canonical payload"""
    # TestClient has websocket support
    with client.websocket_connect("/ws/telemetry") as websocket:
        payload = {
            "node": 101, "seq": 4, "probes_c": [29.5], "ambient_c": 28.0, "faults": 0
        }
        r = client.post("/api/internal/telemetry", json=payload)
        assert r.status_code == 200
        
        # Check WS
        data = websocket.receive_json()
        assert data["node"] == 101
        assert data["seq"] == 4
        assert data["probes_c"] == [29.5]
        assert data["computed_status"] == "NORMAL"
