import serial
import struct
import sqlite3
import datetime
import json
import paho.mqtt.client as mqtt

# ---------------------------------------------------------
# CONSTANTS & CONTRACTS
# ---------------------------------------------------------
DB_PATH = 'vermikendra.db'
SERIAL_PORT = '/dev/serial0' # Assuming UART connection to Waveshare HAT
BAUD_RATE = 115200

SENSOR_FAULT_INT16 = 0x8000
SENSOR_FAULT_UINT16 = 0xFFFF

# 44-byte binary unpack string matching firmware/src/config.h
# B=uint8, H=uint16, h=int16, I=uint32, i=int32, b=int8, 4s=bytes[4]
PAYLOAD_FORMAT = '<B H H B H H h h h h h h H H I H i H B b 4s'
PAYLOAD_SIZE = struct.calcsize(PAYLOAD_FORMAT)

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect(DB_PATH, isolation_level=None) # autocommit
conn.execute('PRAGMA journal_mode=WAL;')

mqttc = mqtt.Client()
mqttc.connect("127.0.0.1", 1883, 60)
mqttc.loop_start()

# ---------------------------------------------------------
# UTILS
# ---------------------------------------------------------
def safe_int16(val):
    return None if val == -32768 else val / 100.0  # -32768 is 0x8000 signed

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
            # For demonstration without hardware, block
            import time; time.sleep(1); continue

        if len(raw_data) == PAYLOAD_SIZE:
            # 1. Unpack Binary Frame
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

            # Calculate actual timestamp
            ts_now = datetime.datetime.utcnow()
            ts_actual = ts_now - datetime.timedelta(seconds=age_s)
            ts_str = ts_actual.isoformat()

            # 2. Translate to safe Python types (Data Contract Enforcement)
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

            # 3. Store to SQLite WAL
            try:
                conn.execute("""
                    INSERT INTO readings 
                    (node_id, ts, seq, probe_1, probe_2, probe_3, probe_4, probe_5, 
                     ambient, rh, pressure, gas_ohm, moisture_raw, mass_g, co2_ppm, 
                     battery_mv, rssi, flags, faults)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (node_id, ts_str, seq, probe_1, probe_2, probe_3, probe_4, probe_5,
                      ambient, rel_hum, pressure, gas_res, moisture, mass, co2_ppm,
                      batt_mv, rssi, flags, faults))
                
                conn.execute("UPDATE nodes SET last_seen=?, battery_mv=? WHERE id=?", 
                             (ts_str, batt_mv, node_id))
            except sqlite3.IntegrityError:
                print(f"[!] Duplicate packet dropped: Node={node_id} Seq={seq}")

            # 4. Publish to local MQTT for vk-engine analytics
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
            # Assuming bin mapping is site-level, defaulting to 1 for MVP
            mqttc.publish(f"vk/site1/node{node_id}/up", json.dumps(msg))

if __name__ == '__main__':
    main()
