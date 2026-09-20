import time
import struct
import random
import paho.mqtt.client as mqtt
import json

# Simulator for Vermikendra Edge Node
# Outputs deterministic JSON telemetry directly to MQTT to test E2E WebSocket and DB pipelines without Virtual Serial.

NODE_ID = 101
SITE_ID = "site_hq"
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

print(f"[*] Starting Vermikendra Node Simulator (Node {NODE_ID}) via MQTT")

mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
mqttc.loop_start()

seq = 0
base_temp = 25.0

while True:
    seq += 1
    base_temp += random.uniform(-0.1, 0.2)
    
    t1 = round(base_temp, 2)
    t2 = round(base_temp - 0.5, 2)
    t3 = round(base_temp - 1.0, 2)
    t4 = round(base_temp - 1.5, 2)
    
    msg = {
        "node": NODE_ID,
        "seq": seq,
        "probes_c": [t1, t2, t3, t4, None],
        "ambient_c": 24.0,
        "rh_pct": 60.0,
        "co2_ppm": int(800 + (seq * 2)),
        "moisture_raw": 500,
        "mass_g": 15000,
        "rssi": -65,
        "faults": 0
    }
    
    topic = f"vk/{SITE_ID}/node{NODE_ID}/up"
    mqttc.publish(topic, json.dumps(msg))
    
    print(f"PUBLISHED -> {topic} : T1={t1}C CO2={msg['co2_ppm']}ppm")
    time.sleep(5)
