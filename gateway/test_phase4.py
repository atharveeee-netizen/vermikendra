import sqlite3
import os

DB_PATH = 'vermikendra.db'

def run_test():
    print("--- Phase 4: Zero-State Database Verification ---")
    
    if not os.path.exists(DB_PATH):
        import db
        db.bootstrap_database()
        
    import db
    conn = db.get_connection()
    
    # Check WAL
    cur = conn.execute("PRAGMA journal_mode;")
    wal = cur.fetchone()[0]
    print(f"WAL Enabled: {wal.upper() == 'WAL'}")
    
    # Check Foreign Keys
    cur = conn.execute("PRAGMA foreign_keys;")
    fk = cur.fetchone()[0]
    print(f"Foreign Keys Enabled: {bool(fk)}")
    
    # Check tables
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    print(f"Tables exist: {tables}")
    
    # Check emptiness
    for t in tables:
        if t != "sqlite_sequence":
            cur = conn.execute(f"SELECT COUNT(*) FROM {t};")
            count = cur.fetchone()[0]
            print(f"Table {t} row count: {count}")
            
    conn.close()

if __name__ == '__main__':
    run_test()
