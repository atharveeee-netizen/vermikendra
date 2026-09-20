import time
import struct
import serial
import random

# Simulator for Vermikendra Edge Node
# Outputs deterministic, 44-byte binary packets identical to C++ firmware.

PORT = 'COM1' # Use virtual serial port for windows, or /dev/ttyV0 for linux
NODE_ID = 101

PAYLOAD_FORMAT = '<B H H B H H h h h h h h H H I H i H B b 4s'

seq = 0
base_temp = 25.0

print(f"[*] Starting Vermikendra Node Simulator (Node {NODE_ID})")

while True:
    # Deterministic biological simulation
    seq += 1
    
    # Slight upward drift
    base_temp += random.uniform(-0.1, 0.2)
    
    t1 = int((base_temp) * 100)
    t2 = int((base_temp - 0.5) * 100)
    t3 = int((base_temp - 1.0) * 100)
    t4 = int((base_temp - 1.5) * 100)
    t5 = 0x8000 # Simulate a broken probe 5
    
    t_amb = int((24.0) * 100)
    rh = 6000
    pres = 1013
    gas_res = 50000
    moisture = 500
    mass = 15000
    co2 = 800 + (seq * 2) # Simulate respiration slope
    
    version = 0x01
    flags = 0
    age_s = 0
    batt_mv = 3800
    faults = 0
    rssi = -65
    hmac_tag = b'ABCD'

    try:
        packet = struct.pack(PAYLOAD_FORMAT,
            version, NODE_ID, seq, flags, age_s, batt_mv,
            t1, t2, t3, t4, t5, t_amb, rh, pres,
            gas_res, moisture, mass, co2,
            faults, rssi, hmac_tag
        )
        
        # NOTE: For local testing without a virtual serial port loopback,
        # you can pipe this directly to a file, or modify vk_ingest to read from stdin/socket.
        print(f"PACKET: Node={NODE_ID} Seq={seq} T1={base_temp:.1f}C CO2={co2}ppm")
    except Exception as e:
        print(e)
        
    time.sleep(5)
