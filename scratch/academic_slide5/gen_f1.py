
import os
from PIL import Image, ImageDraw, ImageFont

W_F1, H_F1 = 2460, 600
f1_canvas = Image.new('RGB', (W_F1, H_F1), '#ffffff')
f1_draw = ImageDraw.Draw(f1_canvas)

# Fonts
f_hdr = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
f_lead = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_text = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)
f_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
f_mono = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 10.5)

# Outer Frame
f1_draw.rounded_rectangle([(10, 10), (W_F1 - 10, H_F1 - 10)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
f1_draw.rounded_rectangle([(10, 10), (W_F1 - 10, 50)], radius=16, fill='#f8fafc')
f1_draw.line([(10, 50), (W_F1 - 10, 50)], fill='#cbd5e1', width=2)
f1_draw.text((W_F1/2, 30), 'Fig. 1: Multi-Disciplinary System Layer Ownership & Architectural Interfaces', font=f_hdr, fill='#0f172a', anchor='mm')

# ----------------- COLUMN 1: ATHARVE DAHIMA (Hardware & Embedded Lead)
cx1, cw1 = 25, 750
f1_draw.rounded_rectangle([(cx1, 65), (cx1 + cw1, H_F1 - 20)], radius=12, fill='#f8fafc', outline='#0284c7', width=2)

f1_draw.rounded_rectangle([(cx1, 65), (cx1 + cw1, 135)], radius=12, fill='#e0f2fe')
f1_draw.line([(cx1, 135), (cx1 + cw1, 135)], fill='#0284c7', width=2)
f1_draw.text((cx1 + 20, 85), 'LAYER 1: EMBEDDED NODE & POWER HARVESTING', font=f_sub, fill='#0369a1')
f1_draw.text((cx1 + 20, 112), 'Atharve Dahima', font=f_lead, fill='#0f172a')
f1_draw.text((cx1 + 180, 114), '|  B.Tech ECE (Hardware & Firmware Lead)', font=f_text, fill='#0369a1')

subs1 = [
    ('Power Harvesting Subsystem:', '6V/2W Solar Panel -> TP4056 CC/CV Charger -> 3000mAh Li-ion Cell'),
    ('Dual-Rail Voltage Regulation:', 'TPS62740 Buck (360 nA Iq) -> Always-on 3V3 Rail & Switched 3V3_S Rail'),
    ('Embedded Firmware & Drivers:', 'Nordic nRF52840 (ARM Cortex-M4F) in C++/PlatformIO with Hardware WDT'),
    ('5-Point Depth Array Instrumentation:', '5x DS18B20 1-Wire Digital Probes at 5, 10, 15, 20, 25 cm (+/-0.5 C Precision)'),
    ('NDIR Respiration & Purge Pod:', 'Sensirion SCD41 Photoacoustic NDIR CO2 Cell + 40mm 5V Active Purge Fan'),
    ('Physical Enclosure & Mechanical:', 'IP65 ABS Weatherproof Enclosure CAD with ePTFE Hydrophobic Vent Membrane')
]
for i, (st, sd) in enumerate(subs1):
    sy = 150 + i * 48
    f1_draw.rounded_rectangle([(cx1 + 15, sy), (cx1 + cw1 - 15, sy + 42)], radius=6, fill='#ffffff', outline='#cbd5e1', width=1)
    f1_draw.text((cx1 + 25, sy + 12), st, font=f_bold, fill='#0369a1')
    f1_draw.text((cx1 + 25, sy + 27), sd, font=f_mono, fill='#334155')

f1_draw.rounded_rectangle([(cx1 + 15, 450), (cx1 + cw1 - 15, H_F1 - 30)], radius=8, fill='#f0fdf4', outline='#16a34a', width=1)
f1_draw.text((cx1 + cw1/2, 470), 'VERIFIED HARDWARE BENCHMARKS & ARTIFACTS', font=f_bold, fill='#166534', anchor='mm')
f1_draw.text((cx1 + 25, 492), '• Quiescent Deep Sleep Current: 18 uA (Oscilloscope Verified)', font=f_text, fill='#166534')
f1_draw.text((cx1 + 25, 512), '• Field Battery Autonomy: > 7 Days Zero-Sunlight Endurance (Monsoon Resilient)', font=f_text, fill='#166534')
f1_draw.text((cx1 + 25, 532), '• Autonomous Edge Failsafe: Triggers local misting relay when T >= 33 C without gateway', font=f_text, fill='#166534')


# ----------------- BRIDGE 1: LoRa RF PHY (x: 785 to 840)
bx1 = 785
f1_draw.rounded_rectangle([(bx1, 160), (bx1 + 55, 430)], radius=8, fill='#fffbeb', outline='#d97706', width=2)
f1_draw.text((bx1 + 27, 185), 'LoRa', font=f_bold, fill='#92400e', anchor='mm')
f1_draw.text((bx1 + 27, 205), '865 MHz', font=f_mono, fill='#b45309', anchor='mm')
f1_draw.text((bx1 + 27, 225), 'P2P PHY', font=f_mono, fill='#b45309', anchor='mm')
f1_draw.line([(bx1 + 10, 245), (bx1 + 45, 245)], fill='#d97706', width=1)
f1_draw.text((bx1 + 27, 275), '44-Byte\nBinary\nPacket', font=f_bold, fill='#0f172a', anchor='mm')
f1_draw.line([(bx1 + 10, 310), (bx1 + 45, 310)], fill='#d97706', width=1)
f1_draw.text((bx1 + 27, 345), 'HMAC\nSHA-256\nSigned', font=f_mono, fill='#7c3aed', anchor='mm')
f1_draw.line([(bx1 + 10, 385), (bx1 + 45, 385)], fill='#d97706', width=1)
f1_draw.text((bx1 + 27, 405), '> 2.5 km', font=f_bold, fill='#16a34a', anchor='mm')

f1_draw.line([(cx1 + cw1, 290), (bx1, 290)], fill='#0284c7', width=2)
f1_draw.polygon([(bx1 - 2, 287), (bx1 + 4, 290), (bx1 - 2, 293)], fill='#0284c7')

f1_draw.line([(bx1 + 55, 290), (850, 290)], fill='#d97706', width=2)
f1_draw.polygon([(848, 287), (854, 290), (848, 293)], fill='#d97706')


# ----------------- COLUMN 2: AKSHIT AGARWAL (Gateway & Analytics Lead)
cx2, cw2 = 850, 750
f1_draw.rounded_rectangle([(cx2, 65), (cx2 + cw2, H_F1 - 20)], radius=12, fill='#f8fafc', outline='#15803d', width=2)

f1_draw.rounded_rectangle([(cx2, 65), (cx2 + cw2, 135)], radius=12, fill='#ecfdf5')
f1_draw.line([(cx2, 135), (cx2 + cw2, 135)], fill='#15803d', width=2)
f1_draw.text((cx2 + 20, 85), 'LAYER 2: GATEWAY DAEMONS & ML ANALYTICS', font=f_sub, fill='#15803d')
f1_draw.text((cx2 + 20, 112), 'Akshit Agarwal', font=f_lead, fill='#0f172a')
f1_draw.text((cx2 + 180, 114), '|  B.Tech CSE (Gateway Architecture & ML Lead)', font=f_text, fill='#15803d')

subs2 = [
    ('Raspberry Pi CM4 Linux Environment:', 'Headless Debian Linux with systemd service daemons and watchdog timers'),
    ('Serial Ingest & Packet Parser:', 'Python CP2102 Serial UART driver decoding 44-byte binary frames @ 115200 baud'),
    ('Cryptographic Security Engine:', 'HMAC-SHA256 signature verification & CRC-16 hardware checksum validation'),
    ('Mosquitto MQTT Message Broker:', 'Asynchronous inter-process bus: topics v1/node/{id}/telemetry & /alerts'),
    ('FastAPI Core & WebSockets:', 'Asynchronous ASGI server streaming real-time metrics and historical REST JSON'),
    ('1D Thermal ODE & CO2 Regression:', 'Predictive heat diffusion PDE solver + Linear regression for biological maturity')
]
for i, (st, sd) in enumerate(subs2):
    sy = 150 + i * 48
    f1_draw.rounded_rectangle([(cx2 + 15, sy), (cx2 + cw2 - 15, sy + 42)], radius=6, fill='#ffffff', outline='#cbd5e1', width=1)
    f1_draw.text((cx2 + 25, sy + 12), st, font=f_bold, fill='#15803d')
    f1_draw.text((cx2 + 25, sy + 27), sd, font=f_mono, fill='#334155')

f1_draw.rounded_rectangle([(cx2 + 15, 450), (cx2 + cw2 - 15, H_F1 - 30)], radius=8, fill='#f0fdf4', outline='#16a34a', width=1)
f1_draw.text((cx2 + cw2/2, 470), 'VERIFIED SOFTWARE BENCHMARKS & ARTIFACTS', font=f_bold, fill='#166534', anchor='mm')
f1_draw.text((cx2 + 25, 492), '• 100% Offline Resilience: Zero internet or cellular 4G connectivity needed', font=f_text, fill='#166534')
f1_draw.text((cx2 + 25, 512), '• Ingestion Latency: < 45 ms packet arrival to SQLite WAL database commit', font=f_text, fill='#166534')
f1_draw.text((cx2 + 25, 532), '• Predictive Horizon: 60-minute advance forecast of thermal boundary layer breach', font=f_text, fill='#166534')


# ----------------- BRIDGE 2: Local WiFi / WS (x: 1610 to 1665)
bx2 = 1610
f1_draw.rounded_rectangle([(bx2, 160), (bx2 + 55, 430)], radius=8, fill='#eef2ff', outline='#4338ca', width=2)
f1_draw.text((bx2 + 27, 185), 'WiFi', font=f_bold, fill='#3730a3', anchor='mm')
f1_draw.text((bx2 + 27, 205), 'Hotspot', font=f_mono, fill='#4338ca', anchor='mm')
f1_draw.text((bx2 + 27, 225), 'AP Mode', font=f_mono, fill='#4338ca', anchor='mm')
f1_draw.line([(bx2 + 10, 245), (bx2 + 45, 245)], fill='#4338ca', width=1)
f1_draw.text((bx2 + 27, 275), '192.168\n.4.1\nLocal IP', font=f_bold, fill='#0f172a', anchor='mm')
f1_draw.line([(bx2 + 10, 310), (bx2 + 45, 310)], fill='#4338ca', width=1)
f1_draw.text((bx2 + 27, 345), 'JSON\nREST API\n& WS', font=f_mono, fill='#0284c7', anchor='mm')
f1_draw.line([(bx2 + 10, 385), (bx2 + 45, 385)], fill='#4338ca', width=1)
f1_draw.text((bx2 + 27, 405), 'Zero 4G', font=f_bold, fill='#16a34a', anchor='mm')

f1_draw.line([(cx2 + cw2, 290), (bx2, 290)], fill='#15803d', width=2)
f1_draw.polygon([(bx2 - 2, 287), (bx2 + 4, 290), (bx2 - 2, 293)], fill='#15803d')

f1_draw.line([(bx2 + 55, 290), (1675, 290)], fill='#4338ca', width=2)
f1_draw.polygon([(1673, 287), (1679, 290), (1673, 293)], fill='#4338ca')


# ----------------- COLUMN 3: CHARVI MEDDITA (Frontend & Product Lead)
cx3, cw3 = 1675, 750
f1_draw.rounded_rectangle([(cx3, 65), (cx3 + cw3, H_F1 - 20)], radius=12, fill='#f8fafc', outline='#7c3aed', width=2)

f1_draw.rounded_rectangle([(cx3, 65), (cx3 + cw3, 135)], radius=12, fill='#ede9fe')
f1_draw.line([(cx3, 135), (cx3 + cw3, 135)], fill='#7c3aed', width=2)
f1_draw.text((cx3 + 20, 85), 'LAYER 3: OFFLINE PWA & FARMER USABILITY', font=f_sub, fill='#7c3aed')
f1_draw.text((cx3 + 20, 112), 'Charvi Meddita', font=f_lead, fill='#0f172a')
f1_draw.text((cx3 + 175, 114), '|  B.Tech CSE (Offline PWA & Product Usability Lead)', font=f_text, fill='#7c3aed')

subs3 = [
    ('React 18 / Vite Progressive Web App:', 'Modern reactive single-page app bundled with Tailwind CSS & Lucide icons'),
    ('Service Worker Offline Engine:', 'Workbox offline caching ensuring immediate launch with zero internet connectivity'),
    ('Multilingual i18n Localization:', 'Native Gujarati, Hindi, and English UX specifically designed for grassroots farmers'),
    ('Low-Literacy Visual Dials:', 'Color-coded gauge dials (Green/Yellow/Red) and depth thermal contour maps'),
    ('Audio-Visual Alert Subsystem:', 'Browser Web Audio API sound chime and tactile vibration on >33 C hotspot breach'),
    ('Batch Audit Trail & QR Ledger:', 'Generates tamper-evident batch quality certificates for premium compost market pricing')
]
for i, (st, sd) in enumerate(subs3):
    sy = 150 + i * 48
    f1_draw.rounded_rectangle([(cx3 + 15, sy), (cx3 + cw3 - 15, sy + 42)], radius=6, fill='#ffffff', outline='#cbd5e1', width=1)
    f1_draw.text((cx3 + 25, sy + 12), st, font=f_bold, fill='#7c3aed')
    f1_draw.text((cx3 + 25, sy + 27), sd, font=f_mono, fill='#334155')

f1_draw.rounded_rectangle([(cx3 + 15, 450), (cx3 + cw3 - 15, H_F1 - 30)], radius=8, fill='#f0fdf4', outline='#16a34a', width=1)
f1_draw.text((cx3 + cw3/2, 470), 'VERIFIED FIELD USABILITY BENCHMARKS', font=f_bold, fill='#166534', anchor='mm')
f1_draw.text((cx3 + 25, 492), '• Cold App Launch Time: < 250 ms from local Gateway cache without WAN', font=f_text, fill='#166534')
f1_draw.text((cx3 + 25, 512), '• Usability Evaluation: 100% task completion rate among non-English rural self-help groups', font=f_text, fill='#166534')
f1_draw.text((cx3 + 25, 532), '• Field Audit Trail: Generates verifiable digital batch certificate for organic FCO pricing', font=f_text, fill='#166534')

f1_canvas.save('scratch/academic_slide5/fig1_team_system_ownership_master.png', quality=98)
print('Generated Figure 1 system ownership master!')
