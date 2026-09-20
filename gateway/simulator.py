import time
import datetime
import requests
import random

API_URL = "http://127.0.0.1:8000/api/internal/telemetry"

def simulate_node(node_id: int, seq: int):
    # Phase 5: Simulator Repair (NO direct DB writes)
    ts_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    msg = {
        "node": node_id,
        "seq": seq,
        "probes_c": [31.4 + random.uniform(-0.5, 0.5), 31.0, 30.5, 30.0, None],
        "ambient_c": 28.0 + random.uniform(-1, 1),
        "rh_pct": 55.0 + random.uniform(-2, 2),
        "co2_ppm": 1100 + int(random.uniform(-50, 50)),
        "mass_g": 12450,
        "rssi": -72 + int(random.uniform(-5, 5)),
        "faults": 0,
        "ts": ts_str
    }
    try:
        r = requests.post(API_URL, json=msg)
        print(f"[*] Node {node_id} seq {seq} -> {r.status_code} {r.text}")
    except Exception as e:
        print(f"[!] Node {node_id} failed: {e}")

if __name__ == '__main__':
    print("[*] Starting Simulator...")
    seq = 1000
    while True:
        seq += 1
        simulate_node(101, seq)
        simulate_node(202, seq)
        time.sleep(5)
