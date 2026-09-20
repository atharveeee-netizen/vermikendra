import sqlite3
import json
import datetime
import requests

DB_PATH = "vermikendra.db"

def inject():
    print("[*] Simulating Single Bin (Phase 6 & 7)")
    
    node_id = 999
    site_id = "SIM-SITE-01"
    bin_id = "SIM-BIN-01"
    
    conn = sqlite3.connect(DB_PATH)
    
    # Auto-provision
    conn.execute("INSERT OR IGNORE INTO sites (id, name, location) VALUES (?, ?, ?)", (site_id, "Simulated Site", "Test Bed"))
    conn.execute("INSERT OR IGNORE INTO bins (id, site_id, name) VALUES (?, ?, ?)", (bin_id, site_id, "Simulated Bin"))
    conn.execute("INSERT OR IGNORE INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (node_id, bin_id, "00:00:00:00:00:SIM"))
    
    ts_str = "2026-09-20T12:00:00Z"
    
    # Inject telemetry
    conn.execute("""
        INSERT INTO telemetry 
        (node_id, ts, ambient_c, probe_1, probe_2, probe_3, probe_4, probe_5, 
         moisture_raw, co2_ppm, mass_g, battery_mv, faults)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (node_id, ts_str, 28.0, 31.4, 31.0, 30.5, 30.0, None, 48, 1100, 12450, 3800, 0))
    
    conn.commit()
    conn.close()
    
    print(f"[*] Successfully injected exact telemetry to DB for {node_id}")
    
    # Trigger WebSocket
    msg = {
        "node": node_id,
        "seq": 1001,
        "probes_c": [31.4, 31.0, 30.5, 30.0, None],
        "ambient_c": 28.0,
        "rh_pct": 55.0,
        "co2_ppm": 1100,
        "mass_g": 12450,
        "rssi": -72,
        "faults": 0,
        "ts": ts_str
    }
    requests.post("http://127.0.0.1:8000/api/internal/telemetry", json=msg)
    print(f"[*] Pushed to WS bridge")

if __name__ == '__main__':
    inject()
