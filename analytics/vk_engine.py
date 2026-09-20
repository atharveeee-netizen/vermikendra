import sqlite3
import datetime
import json
import paho.mqtt.client as mqtt
from scipy import stats
import numpy as np

# ---------------------------------------------------------
# CONSTANTS & CONFIG
# ---------------------------------------------------------
DB_PATH = '../gateway/vermikendra.db'
MQTT_BROKER = '127.0.0.1'

HEAT_CRITICAL_C = 33.0
HEAT_WARNING_C = 30.0

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect(DB_PATH, isolation_level=None) # autocommit
conn.execute('PRAGMA journal_mode=WAL;')

# ---------------------------------------------------------
# ANALYTICS FUNCTIONS
# ---------------------------------------------------------

def evaluate_heat_risk(node_id, bin_id, current_probes):
    """
    Evaluates current temperatures against hard thresholds.
    Future: Add rolling 30-min OLS slope forecast.
    """
    for idx, temp in enumerate(current_probes):
        if temp is None:
            continue
            
        if temp >= HEAT_CRITICAL_C:
            _trigger_alert(bin_id, 'CRITICAL', 'alert.heat.critical', temp, f'Probe {idx+1}')
        elif temp >= HEAT_WARNING_C:
            _trigger_alert(bin_id, 'WARNING', 'alert.heat.warning', temp, f'Probe {idx+1}')


def process_respiration_run(bin_id, node_id, ts_end):
    """
    Pulls the last 10 minutes (600s) of CO2 data, drops the first 60s,
    and runs SciPy linear regression.
    """
    ts_end_dt = datetime.datetime.fromisoformat(ts_end)
    ts_start_dt = ts_end_dt - datetime.timedelta(seconds=600)
    ts_effective_start_dt = ts_start_dt + datetime.timedelta(seconds=60) # drop first 60s
    
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ts, co2_ppm, mass_g, probe_1 
        FROM readings 
        WHERE node_id = ? AND ts >= ? AND ts <= ?
        ORDER BY ts ASC
    ''', (node_id, ts_effective_start_dt.isoformat(), ts_end_dt.isoformat()))
    
    rows = cursor.fetchall()
    if len(rows) < 20:
        print(f"[!] Respiration cycle invalid: Only {len(rows)} data points (Need >= 20)")
        return
        
    times = []
    co2_vals = []
    masses = []
    temps = []
    
    base_time = datetime.datetime.fromisoformat(rows[0][0])
    
    for row in rows:
        if row[1] is None or row[1] > 4800:
            continue # Drop faulty or maxed sensors
        current_time = datetime.datetime.fromisoformat(row[0])
        delta_min = (current_time - base_time).total_seconds() / 60.0
        
        times.append(delta_min)
        co2_vals.append(row[1])
        if row[2] is not None: masses.append(row[2])
        if row[3] is not None: temps.append(row[3])
        
    if len(times) < 20:
        print(f"[!] Respiration cycle invalid after QC filters.")
        return

    # OLS Regression via SciPy
    slope, intercept, r_value, p_value, std_err = stats.linregress(times, co2_vals)
    r2 = r_value ** 2
    
    avg_mass = np.mean(masses) if masses else 0
    avg_temp = np.mean(temps) if temps else 0
    
    # Validation Rule from TRD
    is_valid = 1 if r2 >= 0.90 else 0
    
    # Assuming Headspace and standard air mol params (mocked for V1)
    index_value = slope * 0.5 # Simplified normalizer placeholder
    
    print(f"[*] Respiration Run: Slope={slope:.2f} ppm/min, R2={r2:.4f}, Valid={is_valid}")
    
    conn.execute('''
        INSERT INTO respiration_runs 
        (bin_id, ts_start, slope_ppm_min, r2, n_points, index_value, bed_temp_c, valid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (bin_id, ts_start_dt.isoformat(), slope, r2, len(times), index_value, avg_temp, is_valid))


def _trigger_alert(bin_id, severity, msg_key, val, context):
    ts_now = datetime.datetime.utcnow().isoformat()
    # Very basic deduplication: check if already open
    cur = conn.cursor()
    cur.execute("SELECT id FROM alerts WHERE bin_id=? AND message_key=? AND ts_clear IS NULL", (bin_id, msg_key))
    if not cur.fetchone():
        print(f"[ALERT] {severity}: {msg_key} ({val})")
        conn.execute('''
            INSERT INTO alerts (bin_id, ts_open, rule_id, severity, value, message_key)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bin_id, ts_now, 'RULE_HEAT', severity, val, msg_key))

# ---------------------------------------------------------
# MQTT CALLBACKS
# ---------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print(f"[*] vk-engine connected to MQTT with code {rc}")
    client.subscribe("vk/+/+/up") # Listen to all sites and nodes

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        node_id = payload['node']
        ts = payload['ts']
        probes = payload.get('probes_c', [])
        
        # Hardcoded Bin ID mapping for MVP
        bin_id = 1 
        
        # 1. Evaluate instant heat risk
        evaluate_heat_risk(node_id, bin_id, probes)
        
        # 2. Respiration triggering logic (simplified: if this packet marks end of cycle)
        # In full system, this is driven by the state machine transitioning out of RESP_MEASURE
        
    except Exception as e:
        print(f"[!] Engine Error parsing MQTT: {e}")

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    print("[*] Starting vk-engine (Deterministic Analytics Layer)")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down vk-engine")

if __name__ == '__main__':
    main()
