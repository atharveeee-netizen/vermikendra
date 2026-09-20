import os
import serial
import struct
import sqlite3
import datetime
import json
import time
import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------
# CONSTANTS & CONTRACTS
# ---------------------------------------------------------
DB_PATH = os.getenv('VK_DB_PATH', 'vermikendra.db')
SERIAL_PORT = os.getenv('VK_SERIAL_PORT', '/dev/serial0')
BAUD_RATE = int(os.getenv('VK_BAUD_RATE', '115200'))
API_URL = "http://127.0.0.1:8000/api/internal/telemetry"

SENSOR_FAULT_INT16 = 0x8000
SENSOR_FAULT_UINT16 = 0xFFFF

PAYLOAD_FORMAT = '<B H H B H H h h h h h h H H I H i H B b 4s'
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FORMAT)

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect(DB_PATH, isolation_level=None)
conn.execute('PRAGMA journal_mode=WAL;')

# Removed MQTT Connection Logic

# ---------------------------------------------------------
# UTILS
# ---------------------------------------------------------
def safe_int16(val):
    return None if val == -32768 else val / 100.0

def safe_uint16(val):
    return None if val == SENSOR_FAULT_UINT16 else val

# ---------------------------------------------------------
# MAIN INGEST LOOP
# ---------------------------------------------------------
def main():
    print(f"[*] Starting vk-ingest on {SERIAL_PORT}")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"[!] Serial Error: {e}. Running in dry-mode for testing.")
        ser = None

    while True:
        if ser and ser.in_waiting >= PAYLOAD_SIZE:
            raw_data = ser.read(PAYLOAD_SIZE)
        else:
            time.sleep(1)
            continue

        if len(raw_data) == PAYLOAD_SIZE:
            try:
                unpacked = struct.unpack(PAYLOAD_FORMAT, raw_data)
            except struct.error:
                print("[!] Frame unpacking failed")
                continue

            (version, node_id, seq, flags, age_s, batt_mv,
             t1, t2, t3, t4, t5, t_amb, rh, pres,
             gas_res, moisture, mass, co2,
             faults, rssi, hmac_tag) = unpacked

            if version != 0x01:
                print(f"[!] Unknown payload version: {version}")
                continue

            ts_now = datetime.datetime.utcnow()
            ts_actual = ts_now - datetime.timedelta(seconds=age_s)
            ts_str = ts_actual.isoformat()

            probe_1 = safe_int16(t1)
            probe_2 = safe_int16(t2)
            probe_3 = safe_int16(t3)
            probe_4 = safe_int16(t4)
            probe_5 = safe_int16(t5)
            ambient = safe_int16(t_amb)
            rel_hum = safe_uint16(rh) / 100.0 if safe_uint16(rh) else None
            pressure = safe_uint16(pres)
            co2_ppm = safe_uint16(co2)

            print(f"[*] Rx Node={node_id} Seq={seq} T1={probe_1} CO2={co2_ppm} RSSI={rssi}")

            try:
                conn.execute("""
                    INSERT INTO telemetry 
                    (node_id, ts, ambient_c, probe_1, probe_2, probe_3, probe_4, probe_5, 
                     moisture_raw, co2_ppm, mass_g, battery_mv, faults)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (node_id, ts_str, ambient, probe_1, probe_2, probe_3, probe_4, probe_5,
                      moisture, co2_ppm, mass, batt_mv, faults))
                
                conn.execute("UPDATE nodes SET last_seen=? WHERE id=?", 
                             (ts_str, node_id))
            except sqlite3.IntegrityError:
                print(f"[!] Duplicate packet dropped: Node={node_id} Seq={seq}")

            msg = {
                "node": node_id,
                "ts": ts_str,
                "seq": seq,
                "probes_c": [probe_1, probe_2, probe_3, probe_4, probe_5],
                "ambient_c": ambient,
                "rh_pct": rel_hum,
                "co2_ppm": co2_ppm,
                "mass_g": mass,
                "rssi": rssi,
                "faults": faults
            }
            try:
                requests.post(API_URL, json=msg, timeout=2)
            except Exception as e:
                print(f"[!] Failed to push to API: {e}")

if __name__ == '__main__':
    main()
