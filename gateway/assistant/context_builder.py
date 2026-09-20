from typing import Optional, Dict, Any
import sqlite3

def build_node_context(conn: sqlite3.Connection, node_id: int) -> Optional[Dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM telemetry WHERE node_id = ? ORDER BY ts DESC LIMIT 1', (node_id,))
    row = cursor.fetchone()
    if not row:
        return None
        
    return dict(row)
