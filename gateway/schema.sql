-- Vermikendra Offline Gateway Schema
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    village TEXT,
    district TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE IF NOT EXISTS bins (
    id INTEGER PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    name TEXT NOT NULL,
    volume_l REAL,
    bed_depth_cm REAL,
    headspace_l REAL,
    tare_kg REAL,
    status TEXT DEFAULT 'Good'
);

CREATE TABLE IF NOT EXISTS nodes (
    id INTEGER PRIMARY KEY,
    bin_id INTEGER REFERENCES bins(id),
    key_id TEXT,
    firmware_version TEXT,
    last_seen DATETIME,
    battery_mv INTEGER
);

-- Readings Table (Strict adherence to Data Contract)
CREATE TABLE IF NOT EXISTS readings (
    node_id INTEGER REFERENCES nodes(id),
    ts DATETIME NOT NULL,
    seq INTEGER NOT NULL,
    probe_1 REAL,
    probe_2 REAL,
    probe_3 REAL,
    probe_4 REAL,
    probe_5 REAL,
    ambient REAL,
    rh REAL,
    pressure REAL,
    gas_ohm INTEGER,
    moisture_raw INTEGER,
    moisture_pct REAL,
    mass_g INTEGER,
    co2_ppm INTEGER,
    battery_mv INTEGER,
    rssi INTEGER,
    snr REAL,
    flags INTEGER,
    faults INTEGER,
    PRIMARY KEY (node_id, ts)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bin_id INTEGER REFERENCES bins(id),
    ts DATETIME NOT NULL,
    type TEXT NOT NULL,
    mass_before_g INTEGER,
    mass_after_g INTEGER,
    delta_g INTEGER,
    source TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bin_id INTEGER REFERENCES bins(id),
    ts_open DATETIME NOT NULL,
    ts_clear DATETIME,
    rule_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    value REAL,
    message_key TEXT NOT NULL,
    ack_user TEXT,
    ack_ts DATETIME
);

CREATE TABLE IF NOT EXISTS respiration_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bin_id INTEGER REFERENCES bins(id),
    ts_start DATETIME NOT NULL,
    slope_ppm_min REAL,
    r2 REAL,
    n_points INTEGER,
    index_value REAL,
    bed_temp_c REAL,
    valid BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER REFERENCES nodes(id),
    ts DATETIME NOT NULL,
    type TEXT NOT NULL,
    argument INTEGER,
    status TEXT DEFAULT 'QUEUED'
);

CREATE TABLE IF NOT EXISTS calibrations (
    node_id INTEGER REFERENCES nodes(id),
    sensor TEXT NOT NULL,
    parameters TEXT NOT NULL, -- Stored as JSON string
    valid_from DATETIME NOT NULL,
    PRIMARY KEY (node_id, sensor)
);
