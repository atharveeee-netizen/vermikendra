import os
import sqlite3
from typing import Optional

DB_PATH = os.getenv('VK_DB_PATH', 'vermikendra.db')

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode for concurrency
    conn.execute('PRAGMA journal_mode=WAL;')
    # Enable foreign keys
    conn.execute('PRAGMA foreign_keys=ON;')
    return conn

def bootstrap_database(db_path: Optional[str] = None):
    """Deterministic Database Bootstrap (Phase 10)"""
    path = db_path or DB_PATH
    schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    if not os.path.exists(schema_file):
        raise RuntimeError(f"Schema file not found at {schema_file}")

    with open(schema_file, 'r') as f:
        schema_sql = f.read()

    conn = get_connection(path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"[*] Database bootstrapped successfully at {path}")
    except Exception as e:
        print(f"[!] Database bootstrap failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    bootstrap_database()
