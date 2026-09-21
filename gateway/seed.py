import os
import sqlite3
import json
from db import bootstrap_database, get_connection

DB_PATH = os.getenv('VK_DB_PATH', 'vermikendra.db')

def seed():
    # Remove existing db if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[*] Removed existing {DB_PATH}")

    # Bootstrap the new schema
    bootstrap_database(DB_PATH)
    
    conn = get_connection(DB_PATH)
    
    # Insert Site
    conn.execute("INSERT INTO sites (id, name, location) VALUES (?, ?, ?)", 
                 ('site-1', 'Main Farm', 'Maharashtra, India'))
    
    # Insert Fields with Boundaries (GeoJSON Polygon)
    field_a_boundary = json.dumps({
        "type": "Polygon",
        "coordinates": [[[73.856, 18.520], [73.858, 18.520], [73.858, 18.522], [73.856, 18.522], [73.856, 18.520]]]
    })
    field_b_boundary = json.dumps({
        "type": "Polygon",
        "coordinates": [[[73.859, 18.520], [73.861, 18.520], [73.861, 18.522], [73.859, 18.522], [73.859, 18.520]]]
    })
    
    conn.execute("INSERT INTO fields (id, site_id, name, boundary) VALUES (?, ?, ?, ?)",
                 ('field-a', 'site-1', 'Field A', field_a_boundary))
    conn.execute("INSERT INTO fields (id, site_id, name, boundary) VALUES (?, ?, ?, ?)",
                 ('field-b', 'site-1', 'Field B', field_b_boundary))

    # Insert Bins with Lat/Lon
    # Field A beds
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-01', 'site-1', 'field-a', 'Bed 01', 18.521, 73.857))
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-02', 'site-1', 'field-a', 'Bed 02', 18.5215, 73.8575))
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-03', 'site-1', 'field-a', 'Bed 03', 18.5205, 73.8565))

    # Field B beds
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-04', 'site-1', 'field-b', 'Bed 04', 18.521, 73.860))
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-05', 'site-1', 'field-b', 'Bed 05', 18.5215, 73.8605))

    # Bed without GPS (to test fallback)
    conn.execute("INSERT INTO bins (id, site_id, field_id, name, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                 ('bed-06', 'site-1', 'field-b', 'Bed 06 (No GPS)', None, None))

    # Insert Nodes
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (101, 'bed-01', 'AA:BB:CC:DD:EE:01'))
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (102, 'bed-02', 'AA:BB:CC:DD:EE:02'))
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (103, 'bed-03', 'AA:BB:CC:DD:EE:03'))
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (104, 'bed-04', 'AA:BB:CC:DD:EE:04'))
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (105, 'bed-05', 'AA:BB:CC:DD:EE:05'))
    conn.execute("INSERT INTO nodes (id, bin_id, mac_address) VALUES (?, ?, ?)", (106, 'bed-06', 'AA:BB:CC:DD:EE:06'))

    conn.commit()
    print("[*] Database seeded successfully with Farm -> Field -> Bed spatial hierarchy.")
    conn.close()

if __name__ == '__main__':
    seed()
