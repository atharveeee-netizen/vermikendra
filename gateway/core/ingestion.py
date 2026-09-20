import sqlite3
import datetime
import json
from typing import Dict, Any, Tuple
from db import get_connection

class IngestionError(Exception):
    pass

class DuplicateTelemetryError(IngestionError):
    pass

class ValidationError(IngestionError):
    pass

def calculate_status(context: Dict[str, Any]) -> Tuple[str, str]:
    """
    Phase 10 & Phase 32: Explicit status semantics.
    Calculates the status strictly based on empirical fault and temperature data.
    """
    faults = context.get('faults', 0)
    
    # We strictly use bed probes for thermal risk, NOT ambient.
    # We assume probe_1 is the primary bed probe. 
    # If it's None, we fall back to other probes. Ambient is NOT a substitute for bed temp.
    probes_c = context.get('probes_c', [])
    if isinstance(probes_c, str):
        try:
            probes_c = json.loads(probes_c)
        except:
            probes_c = []
            
    bed_temp = None
    for p in probes_c:
        if p is not None:
            bed_temp = float(p)
            break
            
    if faults > 0:
        return "SENSOR_FAULT", "Hardware sensor fault detected."
        
    if bed_temp is not None:
        if bed_temp > 32.0:
            return "ACTION_NEEDED", "Bed temperature exceeds normal operating threshold."
        elif bed_temp > 30.0:
            return "WATCH", "Bed temperature is elevated."
            
    return "NORMAL", ""

def ingest_telemetry_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase 2: Canonical Ingestion Adapter
    Phase 4: Idempotency (node_id, seq)
    Phase 6: Shared Ingestion Function
    
    All incoming telemetry (API, Simulator, Serial, Radio) must route through here.
    """
    conn = get_connection()
    try:
        # 1. Validation
        node_id = payload.get("node")
        seq = payload.get("seq")
        
        if node_id is None or seq is None:
            raise ValidationError("Missing node or seq")
            
        # 2. Node lookup & site/bin resolution
        cur = conn.cursor()
        cur.execute("SELECT id, bin_id FROM nodes WHERE id = ?", (node_id,))
        node_row = cur.fetchone()
        
        if not node_row:
            # Upsert fallback for unknown nodes during testing
            # Real hardware would reject unregistered nodes
            cur.execute("INSERT OR IGNORE INTO sites (id, name) VALUES (1, 'SITE-1')")
            cur.execute("INSERT OR IGNORE INTO bins (id, site_id, name) VALUES (1, 1, 'BIN-01')")
            cur.execute("INSERT INTO nodes (id, bin_id) VALUES (?, 1)", (node_id,))
            bin_id = 1
        else:
            bin_id = node_row['bin_id']

        # 3. Idempotency Check (Phase 4)
        # Check if we already have this sequence number for this node
        cur.execute("SELECT id FROM telemetry WHERE node_id = ? AND seq = ?", (node_id, seq))
        if cur.fetchone():
            raise DuplicateTelemetryError(f"Duplicate sequence {seq} for node {node_id}")

        # 4. Insert Telemetry
        ts = payload.get("ts")
        if not ts:
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
        probes_c = payload.get("probes_c", [])
        p1 = probes_c[0] if len(probes_c) > 0 else None
        p2 = probes_c[1] if len(probes_c) > 1 else None
        p3 = probes_c[2] if len(probes_c) > 2 else None
        p4 = probes_c[3] if len(probes_c) > 3 else None
        p5 = probes_c[4] if len(probes_c) > 4 else None
        
        ambient_c = payload.get("ambient_c")
        rh_pct = payload.get("rh_pct")
        co2_ppm = payload.get("co2_ppm")
        mass_g = payload.get("mass_g")
        rssi = payload.get("rssi")
        faults = payload.get("faults", 0)
        
        cur.execute('''
            INSERT INTO telemetry 
            (node_id, seq, ts, probe_1, probe_2, probe_3, probe_4, probe_5, ambient_c, moisture_raw, co2_ppm, mass_g, faults)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            node_id, seq, ts, 
            p1, p2, p3, p4, p5, ambient_c, rh_pct, co2_ppm, mass_g, faults
        ))
        
        # 5. Last seen update
        cur.execute("UPDATE nodes SET last_seen = ? WHERE id = ?", (ts, node_id))
        
        conn.commit()
        
        # 6. Build the Canonical Event (Phase 3)
        # This is what gets broadcasted via WebSocket.
        # It includes the computed status.
        context_for_status = {
            "faults": faults,
            "probes_c": probes_c
        }
        status, reason = calculate_status(context_for_status)
        
        canonical_event = {
            "node": node_id,
            "bin_id": bin_id,
            "seq": seq,
            "probes_c": probes_c,
            "ambient_c": ambient_c,
            "rh_pct": rh_pct,
            "co2_ppm": co2_ppm,
            "mass_g": mass_g,
            "rssi": rssi,
            "faults": faults,
            "ts": ts,
            "computed_status": status,
            "computed_reason": reason
        }
        return canonical_event
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
