-- Phase 4 & Phase 10: Canonical Schema & Initialization

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sites (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
);

CREATE TABLE IF NOT EXISTS bins (
    id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY,
    bin_id TEXT NOT NULL,
    mac_address TEXT UNIQUE,
    fw_version TEXT,
    last_seen TIMESTAMP,
    FOREIGN KEY(bin_id) REFERENCES bins(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER NOT NULL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ambient_c REAL,
    probe_1 REAL,
    probe_2 REAL,
    probe_3 REAL,
    probe_4 REAL,
    probe_5 REAL,
    moisture_raw INTEGER,
    co2_ppm INTEGER,
    mass_g REAL,
    battery_mv INTEGER,
    faults INTEGER DEFAULT 0,
    quality TEXT DEFAULT 'VALID', -- VALID, STALE, FAULT, MISSING
    FOREIGN KEY(node_id) REFERENCES nodes(id) ON DELETE CASCADE
);

-- Basic Seed Data if empty (simulating discovery)
INSERT OR IGNORE INTO sites (id, name, location) VALUES ('site_hq', 'Vermikendra HQ', 'Indore, India');
INSERT OR IGNORE INTO bins (id, site_id, name) VALUES ('bin_01', 'site_hq', 'Primary Compost Bin');
INSERT OR IGNORE INTO nodes (id, bin_id, mac_address) VALUES (101, 'bin_01', 'AA:BB:CC:DD:EE:FF');
