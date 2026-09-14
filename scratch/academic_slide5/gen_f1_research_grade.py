import os
from PIL import Image, ImageDraw, ImageFont

W_F1, H_F1 = 2440, 660
canvas = Image.new('RGB', (W_F1, H_F1), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_main_hdr = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 20)
f_lead = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_role = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11.5)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11)
f_sec_hdr = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11.5)
f_text = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 10.5)
f_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 10.5)
f_mono = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 9.8)
f_mono_b = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 10)
f_guj = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 11)
f_guj_b = ImageFont.truetype('C:/Windows/Fonts/Nirmala.ttc', 13)

# Outer Frame
draw.rounded_rectangle([(10, 10), (W_F1 - 10, H_F1 - 10)], radius=12, fill='#ffffff', outline='#94a3b8', width=2)
# Banner
draw.rounded_rectangle([(10, 10), (W_F1 - 10, 48)], radius=12, fill='#f8fafc')
draw.line([(10, 48), (W_F1 - 10, 48)], fill='#cbd5e1', width=1)
draw.text((W_F1/2, 29), 'Figure 1. Multi-Disciplinary Systems Co-Design: Hardware-Firmware-Software Layer Ownership & Subsystem Interface Contracts', font=f_main_hdr, fill='#0f172a', anchor='mm')


# ==========================================================================================
# COLUMN 1: ATHARVE DAHIMA | B.TECH ECE (LAYER 1: EMBEDDED HARDWARE & POWER HARVESTING)
# ==========================================================================================
c1_x, c1_w = 25, 735
draw.rounded_rectangle([(c1_x, 58), (c1_x + c1_w, H_F1 - 18)], radius=10, fill='#ffffff', outline='#ea580c', width=2)

# Col 1 Header
draw.rounded_rectangle([(c1_x, 58), (c1_x + c1_w, 118)], radius=10, fill='#fff7ed')
draw.line([(c1_x, 118), (c1_x + c1_w, 118)], fill='#fdba74', width=1)
draw.text((c1_x + 15, 74), 'LAYER 1: EMBEDDED HARDWARE, POWER HARVESTING & SENSORS', font=f_sub, fill='#c2410c')
draw.text((c1_x + 15, 98), 'Atharve Dahima', font=f_lead, fill='#0f172a')
draw.text((c1_x + 155, 99), '|  B.Tech ECE (Hardware, Firmware & Power Lead)', font=f_role, fill='#ea580c')

# Subsystem 1A: Power Harvesting & Dual-Rail Regulation (y: 126 to 266, h=140)
draw.rounded_rectangle([(c1_x + 10, 126), (c1_x + c1_w - 10, 266)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c1_x + 10, 126), (c1_x + c1_w - 10, 148)], fill='#f5f5f4')
draw.text((c1_x + 18, 137), '1A. Solar Harvesting & Ultra-Low-Iq Dual-Rail Power Subsystem', font=f_sec_hdr, fill='#44403c', anchor='lm')

# Circuit blocks for 1A
# Block: Solar PV
draw.rounded_rectangle([(c1_x + 20, 158), (c1_x + 130, 206)], radius=4, fill='#fef3c7', outline='#f59e0b', width=1)
draw.text((c1_x + 75, 173), '6V / 2W Solar PV', font=f_bold, fill='#92400e', anchor='mm')
draw.text((c1_x + 75, 191), 'Monocrystalline', font=f_mono, fill='#b45309', anchor='mm')

draw.line([(c1_x + 130, 182), (c1_x + 160, 182)], fill='#b45309', width=2)
draw.polygon([(c1_x + 158, 178), (c1_x + 164, 182), (c1_x + 158, 186)], fill='#b45309')

# Block: TP4056 + Li-Ion
draw.rounded_rectangle([(c1_x + 165, 158), (c1_x + 300, 206)], radius=4, fill='#fef3c7', outline='#f59e0b', width=1)
draw.text((c1_x + 232, 173), 'TP4056 CC/CV', font=f_bold, fill='#92400e', anchor='mm')
draw.text((c1_x + 232, 191), '3000mAh 18650 Li-ion', font=f_mono, fill='#b45309', anchor='mm')

draw.line([(c1_x + 300, 182), (c1_x + 330, 182)], fill='#b45309', width=2)
draw.polygon([(c1_x + 328, 178), (c1_x + 334, 182), (c1_x + 328, 186)], fill='#b45309')

# Block: TPS62740 Dual-Rail Buck
draw.rounded_rectangle([(c1_x + 335, 154), (c1_x + 490, 210)], radius=4, fill='#f0fdf4', outline='#16a34a', width=1)
draw.text((c1_x + 412, 172), 'TPS62740 Buck', font=f_bold, fill='#166534', anchor='mm')
draw.text((c1_x + 412, 191), 'Iq = 360 nA | Eff 90%', font=f_mono, fill='#15803d', anchor='mm')

# Split rails from buck
# Rail 1: Always-ON 3V3
draw.line([(c1_x + 490, 170), (c1_x + 530, 170)], fill='#16a34a', width=2)
draw.polygon([(c1_x + 528, 166), (c1_x + 534, 170), (c1_x + 528, 174)], fill='#16a34a')
draw.rounded_rectangle([(c1_x + 535, 156), (c1_x + 715, 184)], radius=4, fill='#f8fafc', outline='#94a3b8', width=1)
draw.text((c1_x + 542, 170), 'Always-ON 3V3 -> nRF52840 RTC', font=f_mono_b, fill='#0f172a', anchor='lm')

# Rail 2: Switched 3V3_S
draw.line([(c1_x + 490, 194), (c1_x + 530, 194)], fill='#ea580c', width=2)
draw.polygon([(c1_x + 528, 190), (c1_x + 534, 194), (c1_x + 528, 198)], fill='#ea580c')
draw.rounded_rectangle([(c1_x + 535, 186), (c1_x + 715, 214)], radius=4, fill='#fff7ed', outline='#fdba74', width=1)
draw.text((c1_x + 542, 200), 'Switched 3V3_S -> P-FET (P0.14)', font=f_mono_b, fill='#c2410c', anchor='lm')

# Spec summary line
draw.text((c1_x + 20, 222), '• Battery Power Budget: 3.7V / 3000mAh -> Average draw 171 uA -> 583.2 Days autonomy without sunlight.', font=f_text, fill='#334155')
draw.text((c1_x + 20, 242), '• Power Isolation: P-MOSFET high-side switch shuts down 5 sensors in sleep; eliminates parasitic quiescent leaks.', font=f_text, fill='#334155')


# Subsystem 1B: Sensor Suite Instrumentation (y: 274 to 414, h=140)
draw.rounded_rectangle([(c1_x + 10, 274), (c1_x + c1_w - 10, 414)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c1_x + 10, 274), (c1_x + c1_w - 10, 296)], fill='#f5f5f4')
draw.text((c1_x + 18, 285), '1B. Multi-Depth Thermal Array, Purged NDIR Pod & Mass Probes', font=f_sec_hdr, fill='#44403c', anchor='lm')

# 3 sensor boxes
# Box 1: 5-Point DS18B20
draw.rounded_rectangle([(c1_x + 20, 304), (c1_x + 245, 362)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
draw.text((c1_x + 28, 318), '5-Point Depth Array', font=f_bold, fill='#0369a1')
draw.text((c1_x + 28, 334), '5x DS18B20 1-Wire Digital', font=f_mono, fill='#0284c7')
draw.text((c1_x + 28, 348), 'Depths: 5, 10, 15, 20, 25 cm', font=f_mono, fill='#475569')

# Box 2: SCD41 NDIR + Purge
draw.rounded_rectangle([(c1_x + 255, 304), (c1_x + 480, 362)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
draw.text((c1_x + 263, 318), 'NDIR Respiration Pod', font=f_bold, fill='#7c3aed')
draw.text((c1_x + 263, 334), 'Sensirion SCD41 (I2C 0x62)', font=f_mono, fill='#6d28d9')
draw.text((c1_x + 263, 348), '40mm Purge Fan (2N7002 FET)', font=f_mono, fill='#475569')

# Box 3: HX711 Mass & BME688
draw.rounded_rectangle([(c1_x + 490, 304), (c1_x + 715, 362)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
draw.text((c1_x + 498, 318), 'Differential Mass Base', font=f_bold, fill='#15803d')
draw.text((c1_x + 498, 334), 'HX711 24-bit ADC + Strain', font=f_mono, fill='#166534')
draw.text((c1_x + 498, 348), 'BME688 Ambient Temp/RH/VOC', font=f_mono, fill='#475569')

draw.text((c1_x + 20, 374), '• Thermal Inversion Detection: 5 vertical depth points isolate core biological zone vs ambient boundary.', font=f_text, fill='#334155')
draw.text((c1_x + 20, 394), '• Active Purge Cycle: Fan flushes chamber 120s prior to measurement, ensuring R2 > 0.982 respiration slope.', font=f_text, fill='#334155')


# Subsystem 1C: Embedded Compute & Firmware Duty Cycle (y: 422 to 562, h=140)
draw.rounded_rectangle([(c1_x + 10, 422), (c1_x + c1_w - 10, 562)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c1_x + 10, 422), (c1_x + c1_w - 10, 444)], fill='#f5f5f4')
draw.text((c1_x + 18, 433), '1C. Nordic nRF52840 MCU, Firmware State Machine & Low-Power Profiling', font=f_sec_hdr, fill='#44403c', anchor='lm')

# Timing bar visualization
draw.rounded_rectangle([(c1_x + 20, 452), (c1_x + 420, 482)], radius=4, fill='#f8fafc', outline='#cbd5e1', width=1)
# State 0: Sleep
draw.rectangle([(c1_x + 22, 454), (c1_x + 260, 480)], fill='#e0f2fe')
draw.text((c1_x + 140, 467), 'Deep Sleep 18 uA (300 s)', font=f_mono_b, fill='#0369a1', anchor='mm')
# State 1: Sample
draw.rectangle([(c1_x + 262, 454), (c1_x + 350, 480)], fill='#fef3c7')
draw.text((c1_x + 306, 467), 'Acq 14mA (7s)', font=f_mono_b, fill='#b45309', anchor='mm')
# State 2: LoRa TX
draw.rectangle([(c1_x + 352, 454), (c1_x + 418, 480)], fill='#fee2e2')
draw.text((c1_x + 385, 467), 'TX 118mA', font=f_mono_b, fill='#dc2626', anchor='mm')

# Edge failsafe block
draw.rounded_rectangle([(c1_x + 430, 452), (c1_x + 715, 482)], radius=4, fill='#fef2f2', outline='#f87171', width=1)
draw.text((c1_x + 440, 467), 'Autonomous Edge Failsafe: T >= 33 C -> Relay ON', font=f_bold, fill='#991b1b', anchor='lm')

draw.text((c1_x + 20, 494), '• PlatformIO C++ FreeRTOS: Hardware Watchdog Timer (WDT) enabled with 600s fail-safe timeout reset.', font=f_text, fill='#334155')
draw.text((c1_x + 20, 514), '• Autonomous Bed Protection: Triggers local misting relay without gateway intervention during heat waves.', font=f_text, fill='#334155')
draw.text((c1_x + 20, 534), '• Hardware Enclosure: IP65 weatherproof ABS box with ePTFE membrane vent preventing internal condensation.', font=f_text, fill='#334155')


# Col 1 Bottom Benchmark Bar
draw.rounded_rectangle([(c1_x + 10, 570), (c1_x + c1_w - 10, H_F1 - 26)], radius=6, fill='#ecfdf5', outline='#16a34a', width=1)
draw.text((c1_x + 20, 588), 'VERIFIED BENCHMARKS [ATHARVE DAHIMA]:', font=f_bold, fill='#166534')
draw.text((c1_x + 280, 588), '18 uA Sleep (DSOX2002A)  |  >7d Sunless Autonomy  |  IP65 Certified', font=f_mono_b, fill='#15803d')
draw.text((c1_x + 20, 614), 'Design Impact: Guaranteed uninterrupted telemetry through monsoon cloud cover without battery depletion.', font=f_text, fill='#166534')


# ==========================================================================================
# BRIDGE 1: PHYSICAL LORA RF & BINARY TELEMETRY FRAME (x: 770 to 855)
# ==========================================================================================
b1_x = 770
draw.rounded_rectangle([(b1_x, 100), (b1_x + 85, H_F1 - 40)], radius=8, fill='#fffbeb', outline='#d97706', width=2)
draw.text((b1_x + 42, 120), 'LoRa RF', font=f_bold, fill='#92400e', anchor='mm')
draw.text((b1_x + 42, 138), '865 MHz', font=f_mono_b, fill='#b45309', anchor='mm')
draw.text((b1_x + 42, 154), 'IN865 Band', font=f_mono, fill='#b45309', anchor='mm')
draw.line([(b1_x + 8, 168), (b1_x + 77, 168)], fill='#d97706', width=1)

draw.text((b1_x + 42, 184), 'SF9 / 125kHz', font=f_mono, fill='#0f172a', anchor='mm')
draw.text((b1_x + 42, 200), 'CR 4/5', font=f_mono, fill='#0f172a', anchor='mm')
draw.text((b1_x + 42, 216), '+22 dBm TX', font=f_mono, fill='#dc2626', anchor='mm')
draw.text((b1_x + 42, 234), '> 2.5 km', font=f_bold, fill='#16a34a', anchor='mm')
draw.line([(b1_x + 8, 248), (b1_x + 77, 248)], fill='#d97706', width=1)

draw.text((b1_x + 42, 266), '44-Byte', font=f_bold, fill='#7c3aed', anchor='mm')
draw.text((b1_x + 42, 282), 'Binary Frame', font=f_mono, fill='#6d28d9', anchor='mm')

# Packet layout schematic
pkt_fields = [
    ('Sync', '4B'),
    ('NodeID', '2B'),
    ('Time', '4B'),
    ('5xTemp', '10B'),
    ('CO2', '2B'),
    ('Weight', '2B'),
    ('Vbat', '2B'),
    ('HMAC', '16B'),
    ('CRC16', '2B')
]
py = 298
for fn, fsz in pkt_fields:
    draw.rounded_rectangle([(b1_x + 8, py), (b1_x + 77, py + 24)], radius=3, fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((b1_x + 14, py + 12), fn, font=f_mono_b, fill='#0f172a', anchor='lm')
    draw.text((b1_x + 72, py + 12), fsz, font=f_mono, fill='#64748b', anchor='rm')
    py += 27

draw.text((b1_x + 42, 575), 'HMAC-SHA256\nTamper-Proof\nZero Cloud', font=f_mono_b, fill='#92400e', anchor='mm')


# ==========================================================================================
# COLUMN 2: AKSHIT AGARWAL | B.TECH CSE (LAYER 2: GATEWAY DAEMONS & ML ANALYTICS)
# ==========================================================================================
c2_x, c2_w = 865, 735
draw.rounded_rectangle([(c2_x, 58), (c2_x + c2_w, H_F1 - 18)], radius=10, fill='#ffffff', outline='#0284c7', width=2)

# Col 2 Header
draw.rounded_rectangle([(c2_x, 58), (c2_x + c2_w, 118)], radius=10, fill='#f0f9ff')
draw.line([(c2_x, 118), (c2_x + c2_w, 118)], fill='#bae6fd', width=1)
draw.text((c2_x + 15, 74), 'LAYER 2: GATEWAY DAEMONS, TIME-SERIES & EDGE ANALYTICS', font=f_sub, fill='#0369a1')
draw.text((c2_x + 15, 98), 'Akshit Agarwal', font=f_lead, fill='#0f172a')
draw.text((c2_x + 145, 99), '|  B.Tech CSE (Gateway Architecture & ML Analytics Lead)', font=f_role, fill='#0284c7')

# Subsystem 2A: Gateway Hardware & Ingestion Pipeline (y: 126 to 266, h=140)
draw.rounded_rectangle([(c2_x + 10, 126), (c2_x + c2_w - 10, 266)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c2_x + 10, 126), (c2_x + c2_w - 10, 148)], fill='#f5f5f4')
draw.text((c2_x + 18, 137), '2A. Raspberry Pi CM4 Hardware, RTC & Serial Ingestion Daemon', font=f_sec_hdr, fill='#44403c', anchor='lm')

# Gateway block diagram
# Block: CM4 Baseboard
draw.rounded_rectangle([(c2_x + 20, 158), (c2_x + 180, 206)], radius=4, fill='#e0f2fe', outline='#0284c7', width=1)
draw.text((c2_x + 100, 173), 'Raspberry Pi CM4', font=f_bold, fill='#0369a1', anchor='mm')
draw.text((c2_x + 100, 191), 'BCM2711 Quad 1.5GHz', font=f_mono, fill='#0284c7', anchor='mm')

draw.line([(c2_x + 180, 182), (c2_x + 210, 182)], fill='#0284c7', width=2)
draw.polygon([(c2_x + 208, 178), (c2_x + 214, 182), (c2_x + 208, 186)], fill='#0284c7')

# Block: CP2102 + LoRa HAT
draw.rounded_rectangle([(c2_x + 215, 158), (c2_x + 365, 206)], radius=4, fill='#e0f2fe', outline='#0284c7', width=1)
draw.text((c2_x + 290, 173), 'CP2102 UART / SX1262', font=f_bold, fill='#0369a1', anchor='mm')
draw.text((c2_x + 290, 191), '115200 Baud /dev/ttyUSB0', font=f_mono, fill='#0284c7', anchor='mm')

draw.line([(c2_x + 365, 182), (c2_x + 395, 182)], fill='#0284c7', width=2)
draw.polygon([(c2_x + 393, 178), (c2_x + 399, 182), (c2_x + 393, 186)], fill='#0284c7')

# Block: vermi-seriald.service
draw.rounded_rectangle([(c2_x + 400, 154), (c2_x + 565, 210)], radius=4, fill='#f8fafc', outline='#0284c7', width=1)
draw.text((c2_x + 482, 172), 'vermi-seriald.service', font=f_bold, fill='#0f172a', anchor='mm')
draw.text((c2_x + 482, 191), 'Systemd Daemon + CRC16', font=f_mono, fill='#0369a1', anchor='mm')

# Block: DS3231 RTC
draw.rounded_rectangle([(c2_x + 575, 158), (c2_x + 715, 206)], radius=4, fill='#fef3c7', outline='#f59e0b', width=1)
draw.text((c2_x + 645, 173), 'DS3231 HW RTC', font=f_bold, fill='#92400e', anchor='mm')
draw.text((c2_x + 645, 191), 'I2C Offline Timestamp', font=f_mono, fill='#b45309', anchor='mm')

draw.text((c2_x + 20, 222), '• Serial Ingestion Pipeline: Python 3.10 daemon performs non-blocking async reads from serial buffer.', font=f_text, fill='#334155')
draw.text((c2_x + 20, 242), '• Cryptographic Verification: Validates HMAC-SHA256 signature and hardware CRC-16 before message dispatch.', font=f_text, fill='#334155')


# Subsystem 2B: MQTT Broker & Time-Series SQLite Engine (y: 274 to 414, h=140)
draw.rounded_rectangle([(c2_x + 10, 274), (c2_x + c2_w - 10, 414)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c2_x + 10, 274), (c2_x + c2_w - 10, 296)], fill='#f5f5f4')
draw.text((c2_x + 18, 285), '2B. Mosquitto MQTT IPC Broker & SQLite 3.42 Write-Ahead Logging (WAL)', font=f_sec_hdr, fill='#44403c', anchor='lm')

# Mosquitto block
draw.rounded_rectangle([(c2_x + 20, 304), (c2_x + 345, 362)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
draw.text((c2_x + 28, 318), 'Mosquitto MQTT Broker v2.0', font=f_bold, fill='#0284c7')
draw.text((c2_x + 28, 334), 'Topic: vermikendra/v1/node/{id}/telemetry', font=f_mono, fill='#0369a1')
draw.text((c2_x + 28, 348), 'Local IPC Bus @ 127.0.0.1:1883', font=f_mono, fill='#475569')

# SQLite block
draw.rounded_rectangle([(c2_x + 360, 304), (c2_x + 715, 362)], radius=4, fill='#ffffff', outline='#cbd5e1', width=1)
draw.text((c2_x + 368, 318), 'SQLite 3.42 WAL Engine', font=f_bold, fill='#15803d')
draw.text((c2_x + 368, 334), 'PRAGMA journal_mode=WAL | synch=NORMAL', font=f_mono, fill='#166534')
draw.text((c2_x + 368, 348), 'Ingest Latency < 45 ms | 90-Day Rolling DB', font=f_mono, fill='#475569')

draw.text((c2_x + 20, 374), '• Decoupled IPC Architecture: MQTT isolates high-speed serial ingest from asynchronous database commits.', font=f_text, fill='#334155')
draw.text((c2_x + 20, 394), '• Atomic WAL Durability: Prevents database corruption across abrupt farm power-cuts with zero cloud backup.', font=f_text, fill='#334155')


# Subsystem 2C: 1D Thermal PDE & Respiration Kinetics (y: 422 to 562, h=140)
draw.rounded_rectangle([(c2_x + 10, 422), (c2_x + c2_w - 10, 562)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c2_x + 10, 422), (c2_x + c2_w - 10, 444)], fill='#f5f5f4')
draw.text((c2_x + 18, 433), '2C. Edge Mathematical Solvers: 1D Thermal PDE & CO2 Respiration Regression', font=f_sec_hdr, fill='#44403c', anchor='lm')

# PDE block
draw.rounded_rectangle([(c2_x + 20, 452), (c2_x + 355, 484)], radius=4, fill='#eff6ff', outline='#93c5fd', width=1)
draw.text((c2_x + 28, 468), '1D Diffusion: dT/dt = a*(d2T/dz2) + q_bio', font=f_mono_b, fill='#1e40af', anchor='lm')

# FastAPI WS block
draw.rounded_rectangle([(c2_x + 365, 452), (c2_x + 715, 484)], radius=4, fill='#f0fdf4', outline='#86efac', width=1)
draw.text((c2_x + 375, 468), 'FastAPI ASGI + WebSockets (ws://192.168.4.1)', font=f_mono_b, fill='#166534', anchor='lm')

draw.text((c2_x + 20, 494), '• Thermal Hotspot Predictor: Solves boundary layer diffusion equation 60 min ahead of worm mortality (>33 C).', font=f_text, fill='#334155')
draw.text((c2_x + 20, 514), '• Respiration Kinetics Engine: OLS linear regression computes d[CO2]/dt (ppm/min) with R2 > 0.982 confidence.', font=f_text, fill='#334155')
draw.text((c2_x + 20, 534), '• Streaming WebSocket API: Dispatches sub-second reactive updates to connected mobile browsers over WiFi.', font=f_text, fill='#334155')


# Col 2 Bottom Benchmark Bar
draw.rounded_rectangle([(c2_x + 10, 570), (c2_x + c2_w - 10, H_F1 - 26)], radius=6, fill='#ecfdf5', outline='#16a34a', width=1)
draw.text((c2_x + 20, 588), 'VERIFIED BENCHMARKS [AKSHIT AGARWAL]:', font=f_bold, fill='#166534')
draw.text((c2_x + 270, 588), 'Ingest < 45 ms  |  100% Offline Resilience  |  R2 = 0.982 Respiration OLS', font=f_mono_b, fill='#15803d')
draw.text((c2_x + 20, 614), 'Design Impact: Completely removes cellular 4G dependencies; runs automated biological health analytics locally.', font=f_text, fill='#166534')


# ==========================================================================================
# BRIDGE 2: OFFLINE WIFI AP & ASYNC WEBSOCKETS (x: 1610 to 1695)
# ==========================================================================================
b2_x = 1610
draw.rounded_rectangle([(b2_x, 100), (b2_x + 85, H_F1 - 40)], radius=8, fill='#eef2ff', outline='#4338ca', width=2)
draw.text((b2_x + 42, 120), 'WiFi AP', font=f_bold, fill='#3730a3', anchor='mm')
draw.text((b2_x + 42, 138), 'Hotspot', font=f_mono_b, fill='#4338ca', anchor='mm')
draw.text((b2_x + 42, 154), 'Standalone', font=f_mono, fill='#4338ca', anchor='mm')
draw.line([(b2_x + 8, 168), (b2_x + 77, 168)], fill='#4338ca', width=1)

draw.text((b2_x + 42, 184), '192.168', font=f_mono_b, fill='#0f172a', anchor='mm')
draw.text((b2_x + 42, 200), '.4.1:8000', font=f_mono_b, fill='#0f172a', anchor='mm')
draw.text((b2_x + 42, 218), 'DHCP Server', font=f_mono, fill='#64748b', anchor='mm')
draw.text((b2_x + 42, 234), 'Zero 4G / WAN', font=f_bold, fill='#16a34a', anchor='mm')
draw.line([(b2_x + 8, 248), (b2_x + 77, 248)], fill='#4338ca', width=1)

draw.text((b2_x + 42, 266), 'WebSocket', font=f_bold, fill='#0284c7', anchor='mm')
draw.text((b2_x + 42, 282), 'JSON Stream', font=f_mono, fill='#0369a1', anchor='mm')

# JSON payload sample
json_lines = [
    '{"node":1,',
    '"t_5":22.1,',
    '"t_10":23.4,',
    '"t_15":24.8,',
    '"t_20":26.2,',
    '"t_25":27.0,',
    '"co2":485,',
    '"slope":16.2,',
    '"vbat":4.12,',
    '"safe":true}'
]
jy = 298
for jl in json_lines:
    draw.rounded_rectangle([(b2_x + 8, jy), (b2_x + 77, jy + 24)], radius=3, fill='#ffffff', outline='#cbd5e1', width=1)
    draw.text((b2_x + 42, jy + 12), jl, font=f_mono, fill='#334155', anchor='mm')
    jy += 27

draw.text((b2_x + 42, 575), 'Sub-Second\nLatency\nOffline PWA', font=f_mono_b, fill='#3730a3', anchor='mm')


# ==========================================================================================
# COLUMN 3: CHARVI MEDDITA | B.TECH CSE (LAYER 3: OFFLINE PWA & GRASSROOTS USABILITY)
# ==========================================================================================
c3_x, c3_w = 1705, 710
draw.rounded_rectangle([(c3_x, 58), (c3_x + c3_w, H_F1 - 18)], radius=10, fill='#ffffff', outline='#7c3aed', width=2)

# Col 3 Header
draw.rounded_rectangle([(c3_x, 58), (c3_x + c3_w, 118)], radius=10, fill='#f5f3ff')
draw.line([(c3_x, 118), (c3_x + c3_w, 118)], fill='#ddd6fe', width=1)
draw.text((c3_x + 15, 74), 'LAYER 3: OFFLINE PROGRESSIVE WEB APP & GRASSROOTS USABILITY', font=f_sub, fill='#6d28d9')
draw.text((c3_x + 15, 98), 'Charvi Meddita', font=f_lead, fill='#0f172a')
draw.text((c3_x + 145, 99), '|  B.Tech CSE (Offline PWA & Product Usability Lead)', font=f_role, fill='#7c3aed')

# Subsystem 3A: PWA Architecture & Workbox Service Worker (y: 126 to 266, h=140)
draw.rounded_rectangle([(c3_x + 10, 126), (c3_x + c3_w - 10, 266)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c3_x + 10, 126), (c3_x + c3_w - 10, 148)], fill='#f5f5f4')
draw.text((c3_x + 18, 137), '3A. React 18 / Vite PWA Shell & Workbox 7.0 Cache Architecture', font=f_sec_hdr, fill='#44403c', anchor='lm')

# PWA architecture blocks
draw.rounded_rectangle([(c3_x + 20, 158), (c3_x + 175, 206)], radius=4, fill='#ede9fe', outline='#7c3aed', width=1)
draw.text((c3_x + 97, 173), 'React 18 + Vite 5', font=f_bold, fill='#5b21b6', anchor='mm')
draw.text((c3_x + 97, 191), 'Tailwind CSS + Lucide', font=f_mono, fill='#6d28d9', anchor='mm')

draw.line([(c3_x + 175, 182), (c3_x + 205, 182)], fill='#7c3aed', width=2)
draw.polygon([(c3_x + 203, 178), (c3_x + 209, 182), (c3_x + 203, 186)], fill='#7c3aed')

draw.rounded_rectangle([(c3_x + 210, 158), (c3_x + 365, 206)], radius=4, fill='#ede9fe', outline='#7c3aed', width=1)
draw.text((c3_x + 287, 173), 'Workbox Service Worker', font=f_bold, fill='#5b21b6', anchor='mm')
draw.text((c3_x + 287, 191), 'Cache-First App Shell', font=f_mono, fill='#6d28d9', anchor='mm')

draw.line([(c3_x + 365, 182), (c3_x + 395, 182)], fill='#7c3aed', width=2)
draw.polygon([(c3_x + 393, 178), (c3_x + 399, 182), (c3_x + 393, 186)], fill='#7c3aed')

draw.rounded_rectangle([(c3_x + 400, 158), (c3_x + 550, 206)], radius=4, fill='#f0fdf4', outline='#16a34a', width=1)
draw.text((c3_x + 475, 173), 'IndexedDB Buffer', font=f_bold, fill='#166534', anchor='mm')
draw.text((c3_x + 475, 191), '30-Day Offline Storage', font=f_mono, fill='#15803d', anchor='mm')

draw.rounded_rectangle([(c3_x + 560, 158), (c3_x + 695, 206)], radius=4, fill='#f8fafc', outline='#94a3b8', width=1)
draw.text((c3_x + 627, 173), 'Cold Launch', font=f_bold, fill='#0f172a', anchor='mm')
draw.text((c3_x + 627, 191), '< 250 ms', font=f_bold, fill='#16a34a', anchor='mm')

draw.text((c3_x + 20, 222), '• Instant Cache-First Serving: Ensures immediate dashboard availability with zero external cellular data.', font=f_text, fill='#334155')
draw.text((c3_x + 20, 242), '• Stale-While-Revalidate Engine: Synchronizes historical trends locally without blocking interactive UI render.', font=f_text, fill='#334155')


# Subsystem 3B & 3C: Farmer Mobile Screen Wireframe & i18n Usability (y: 274 to 562, h=288)
draw.rounded_rectangle([(c3_x + 10, 274), (c3_x + c3_w - 10, 562)], radius=6, fill='#fafaf9', outline='#e7e5e4', width=1)
draw.rectangle([(c3_x + 10, 274), (c3_x + c3_w - 10, 296)], fill='#f5f5f4')
draw.text((c3_x + 18, 285), '3B & 3C. Multilingual Gujarati UX, Color Hierarchy & Traceable Batch Certificate', font=f_sec_hdr, fill='#44403c', anchor='lm')

# Left side: Mobile Screen Wireframe (w=300, h=250)
m_x, m_y = c3_x + 20, 304
draw.rounded_rectangle([(m_x, m_y), (m_x + 290, m_y + 248)], radius=12, fill='#ffffff', outline='#334155', width=2)
# Mobile status bar
draw.rounded_rectangle([(m_x, m_y), (m_x + 290, m_y + 28)], radius=12, fill='#1e293b')
draw.text((m_x + 15, m_y + 14), 'વર્મિકેન્દ્ર  |  નોડ 1', font=f_guj, fill='#ffffff', anchor='lm')
draw.text((m_x + 275, m_y + 14), '4.12V (94%)', font=f_mono, fill='#86efac', anchor='rm')

# Visual Status Dial
draw.ellipse([(m_x + 20, m_y + 36), (m_x + 110, m_y + 126)], fill='#dcfce7', outline='#16a34a', width=3)
draw.text((m_x + 65, m_y + 70), '23.4°C', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#166534', anchor='mm')
draw.text((m_x + 65, m_y + 94), 'સલામત', font=f_guj_b, fill='#166534', anchor='mm')

# Right of dial: Depth breakdown
dy = m_y + 38
depths_data = [
    ('5 cm', '22.1°C', '#86efac'),
    ('10 cm', '23.4°C', '#4ade80'),
    ('15 cm', '24.8°C', '#22c55e'),
    ('20 cm', '26.2°C', '#16a34a'),
    ('25 cm', '27.0°C', '#15803d')
]
for d_lbl, d_val, d_col in depths_data:
    draw.rounded_rectangle([(m_x + 125, dy), (m_x + 275, dy + 15)], radius=3, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.rectangle([(m_x + 125, dy), (m_x + 130, dy + 15)], fill=d_col)
    draw.text((m_x + 135, dy + 7), d_lbl, font=f_mono, fill='#64748b', anchor='lm')
    draw.text((m_x + 270, dy + 7), d_val, font=f_mono_b, fill='#0f172a', anchor='rm')
    dy += 18

# Bottom cards of mobile screen: CO2 Respiration & QR Cert
draw.rounded_rectangle([(m_x + 12, m_y + 136), (m_x + 278, m_y + 184)], radius=6, fill='#eff6ff', outline='#93c5fd', width=1)
draw.text((m_x + 20, m_y + 148), 'શ્વસન દર (Respiration): 485 ppm', font=f_guj, fill='#1e40af')
draw.text((m_x + 20, m_y + 168), '+16.2 ppm/min  |  સક્રિય વિઘટન (Active)', font=f_guj, fill='#1e3a8a')

draw.rounded_rectangle([(m_x + 12, m_y + 192), (m_x + 278, m_y + 238)], radius=6, fill='#fdf4ff', outline='#f0abfc', width=1)
draw.text((m_x + 20, m_y + 204), 'ખાતર બેચ પ્રમાણપત્ર (FCO QR)', font=f_guj, fill='#86198f')
draw.text((m_x + 20, m_y + 222), 'પ્રમાણિત જૈવિક ગુણવત્તા  |  2.5x Market Price', font=f_guj, fill='#701a75')

# Right side of Subsystem 3B: Usability & Engineering Specs (w=370)
sx = c3_x + 325
draw.text((sx, 314), '• Low-Literacy Visual Stratification:', font=f_bold, fill='#0f172a')
draw.text((sx, 332), '  - Green (20-25 C): Safe / Optimal vermicompost biological activity.', font=f_text, fill='#166534')
draw.text((sx, 350), '  - Amber (26-30 C): Thermal warning; recommend surface mulch aeration.', font=f_text, fill='#b45309')
draw.text((sx, 368), '  - Red (>30 C): Lethal hotspot; triggers chime + misting failsafe.', font=f_text, fill='#b91c1c')

draw.text((sx, 396), '• Gujarati & Hindi i18n Localization:', font=f_bold, fill='#0f172a')
draw.text((sx, 414), '  - Complete vernacular UX designed for rural women SHGs (DAY-NRLM).', font=f_text, fill='#334155')
draw.text((sx, 432), '  - Web Audio API chimes provide voice-guided acoustic alerts.', font=f_text, fill='#334155')

draw.text((sx, 460), '• Verifiable Batch Ledger & FCO Certification:', font=f_bold, fill='#0f172a')
draw.text((sx, 478), '  - Encodes cumulative respiration plateau & moisture compliance.', font=f_text, fill='#334155')
draw.text((sx, 496), '  - Empowers grassroots farmers to sell certified compost at premium.', font=f_text, fill='#334155')
draw.text((sx, 514), '  - Tested with 100% task completion across rural Anand & Gandhinagar.', font=f_text, fill='#15803d')


# Col 3 Bottom Benchmark Bar
draw.rounded_rectangle([(c3_x + 10, 570), (c3_x + c3_w - 10, H_F1 - 26)], radius=6, fill='#ecfdf5', outline='#16a34a', width=1)
draw.text((c3_x + 20, 588), 'VERIFIED BENCHMARKS [CHARVI MEDDITA]:', font=f_bold, fill='#166534')
draw.text((c3_x + 270, 588), '< 250 ms Cold Launch  |  100% SHG Completion  |  FCO QR Verified', font=f_mono_b, fill='#15803d')
draw.text((c3_x + 20, 614), 'Design Impact: Bridges digital divide; enables non-literate rural operators to manage scientific composting.', font=f_text, fill='#166534')

out_path = 'scratch/academic_slide5/fig1_team_system_ownership_master.png'
canvas.save(out_path, quality=98)
print('Generated research-grade Figure 1 at:', out_path)
