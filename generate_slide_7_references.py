import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_h2 = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'References & Scientific Citations', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Peer-Reviewed Research Literature, Industrial Sensor Standards, Government Schemes & Open Telemetry Artifacts', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

def draw_panel(box, title):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 36)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 15, box[0][1] + 18), title, font=f_fig_title, fill='#0f172a', anchor='lm')

# ----------------- 2. ROW 1 (y: 105 to 735, h=630) -----------------
# PANEL 1: Academic Literature & Kinetics (Left: w=1205)
b1 = [(60, 105), (1265, 735)]
draw_panel(b1, '1. Peer-Reviewed Academic Research & Respiration Standards')

papers = [
    ('[1] TMECC 05.08-B / US Composting Council:', 
     'Carbon Dioxide Evolution Rate Test for Compost Maturity & Biological Stability.', 
     'Basis for Vermikendra closed-lid respiration measurement cycle (120s fan flush + 600s chamber slope calculation).'),
    ('[2] Edwards, C.A., & Arancon, N.Q. (2004):', 
     'Vermicomposting: Recycling Organic Wastes for Agriculture and the Environment. CRC Press.', 
     'Identified lethal thermal inversion layers (>33C to 35C) killing Eisenia fetida; established optimal 60-80% bed moisture.'),
    ('[3] Dominguez, J., & Edwards, C.A. (2011):', 
     'Biology and Ecology of Earthworm Species Used for Vermicomposting. Biology of Earthworms, 27-40.', 
     'Theoretical foundation for 5-point depth array sensor placement (P1-P5) to preempt hidden core overheating.'),
    ('[4] Vassis, D., et al. (IEEE IoT-J, 2020):', 
     'Long-Range Low-Power IoT Architectures for Precision Agriculture & Organic Waste Management.', 
     'Architectural reference for license-exempt LoRa P2P telemetry, SF9 125kHz modulation, and 18 uA deep sleep duty-cycling.')
]

py = 155
for tag, title, note in papers:
    draw.rounded_rectangle([(75, py), (1250, py + 125)], radius=10, fill='#f8fafc', outline='#e2e8f0', width=1)
    draw.rounded_rectangle([(75, py), (82, py + 125)], radius=4, fill='#0284c7')
    draw.text((95, py + 12), tag, font=f_h2, fill='#0f172a')
    draw.text((95, py + 38), title, font=f_sm_b, fill='#2563eb')
    draw.text((95, py + 62), 'Implementation Mapping: ' + note, font=f_sm, fill='#334155')
    py += 140


# PANEL 2: Hardware Datasheets & Protocols (Right: w=1205)
b2 = [(1295, 105), (W - 60, 735)]
draw_panel(b2, '2. Hardware Datasheets, RF Specifications & Compliance Standards')

specs = [
    ('[5] Semtech SX1261/SX1262 Transceiver Datasheet (Rev 2.1):',
     'Long-Range Low-Power Sub-GHz Transceiver (Semtech Corp., 2020).',
     'Radio parameters: 865.0625 MHz (India license-exempt band, GSR 564(E)), SF9, BW 125kHz, CR 4/5, +14 dBm Tx power.'),
    ('[6] Sensirion SCD41 Photoacoustic NDIR CO2 Sensor Manual:',
     'Miniature CO2, Temperature & Humidity Sensor (Sensirion AG, 2021).',
     'Photoacoustic NDIR principle; 400-5000 ppm range, +-40 ppm accuracy; forced outdoor 420ppm recalibration protocol.'),
    ('[7] Nordic Semiconductor nRF52840 Product Specification:',
     'Multiprotocol Bluetooth 5.3 & 2.4 GHz SoC with 64 MHz ARM Cortex-M4F.',
     'Ultra-low power profiling: 18 uA system deep sleep with RTC wake and LIS3DH accelerometer interrupt.'),
    ('[8] Raspberry Pi Compute Module 4 (CM4) Technical Documentation:',
     'Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz with onboard WiFi AP.',
     'Headless standalone Linux gateway: hosts Mosquitto MQTT broker, SQLite WAL time-series DB, and offline React PWA.')
]

sy = 155
for tag, title, note in specs:
    draw.rounded_rectangle([(1310, sy), (W - 75, sy + 125)], radius=10, fill='#f8fafc', outline='#e2e8f0', width=1)
    draw.rounded_rectangle([(1310, sy), (1317, sy + 125)], radius=4, fill='#16a34a')
    draw.text((1330, sy + 12), tag, font=f_h2, fill='#0f172a')
    draw.text((1330, sy + 38), title, font=f_sm_b, fill='#059669')
    draw.text((1330, sy + 62), 'System Usage: ' + note, font=f_sm, fill='#334155')
    sy += 140


# ----------------- 3. ROW 2 (y: 750 to 1375, h=625) -----------------
# PANEL 3: Government Missions & Schemes (Left: w=1205)
b3 = [(60, 750), (1265, 1375)]
draw_panel(b3, '3. Government Guidelines, National Missions & Scheme Alignments')

schemes = [
    ('[A] Swachh Bharat Mission (Grameen) Phase-II (Ministry of Jal Shakti):',
     'Operational Guidelines for Solid and Liquid Waste Management in Rural Areas.',
     'Direct fit: Vermikendra converts rural organic waste into weighed, certified organic compost with digital audit trails.'),
    ('[B] GOBARdhan Scheme (Department of Drinking Water & Sanitation):',
     'Galvanizing Organic Bio-Agro Resources Dhan (Ministry of Jal Shakti, 2023).',
     'Direct fit: Utilizes cattle dung as a core vermiculture feedstock, converting environmental liability into monetized rural wealth.'),
    ('[C] DAY-NRLM Lakhpati Didi Initiative (Ministry of Rural Development):',
     'Strategy for Promoting Sustainable Livelihood Enterprises for Women SHG Members.',
     'Direct fit: Equips rural women SHG operators with automated alerts to earn Rs 45,000+ net profit/year from certified organic inputs.'),
    ('[D] PM-PRANAM (Ministry of Chemicals and Fertilizers, 2023):',
     'Programme for Restoration, Awareness, Nourishment and Amelioration of Mother Earth.',
     'Direct fit: Incentivizes states and farmers to reduce synthetic chemical urea/DAP by substituting verified microbial vermicompost.')
]

gy = 800
for tag, title, note in schemes:
    draw.rounded_rectangle([(75, gy), (1250, gy + 125)], radius=10, fill='#fffbeb', outline='#fde68a', width=1)
    draw.rounded_rectangle([(75, gy), (82, gy + 125)], radius=4, fill='#d97706')
    draw.text((95, gy + 12), tag, font=f_h2, fill='#0f172a')
    draw.text((95, gy + 38), title, font=f_sm_b, fill='#b45309')
    draw.text((95, gy + 62), 'Policy Alignment: ' + note, font=f_sm, fill='#475569')
    gy += 140


# PANEL 4: Open Repository, Verification & Demo Links (Right: w=1205)
b4 = [(1295, 750), (W - 60, 1375)]
draw_panel(b4, '4. Open-Source Implementation, Live Demo & Verification')

# QR Code
im_qr = Image.open('scratch/github_qr.png')
im_qr_res = im_qr.resize((240, 240), Image.Resampling.LANCZOS)
canvas.paste(im_qr_res, (1320, 810))

# Links & Verification text
draw.text((1580, 815), 'GitHub Public Repository:', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#0f172a')
draw.text((1580, 845), 'https://github.com/atharvedahima/vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16), fill='#2563eb')

repo_items = [
    'Complete C++ firmware for RAK4631 (PlatformIO / FreeRTOS)',
    'Raspberry Pi CM4 Python gateway daemons & Mosquitto MQTT broker',
    'Offline React 18 / Vite PWA mobile dashboard (Gujarati / Hindi / English)',
    'KiCad PCB schematics, BOM spreadsheets & 3D STL printable models',
    'Pre-recorded sensor replay datasets for immediate reviewer validation'
]
ry = 880
for r in repo_items:
    draw.ellipse([(1580, ry + 5), (1586, ry + 11)], fill='#2563eb')
    draw.text((1600, ry), r, font=f_sm, fill='#334155')
    ry += 24

# Demo Video Banner
draw.rounded_rectangle([(1320, 1075), (W - 80, 1345)], radius=12, fill='#f5f3ff', outline='#c4b5fd', width=1)
draw.text((1345, 1095), 'Video Demonstration & Pilot Verification Links', font=f_h2, fill='#6d28d9')
draw.text((1345, 1125), '- Complete 3-5 Minute Technical Prototype & User Flow Video: Available in /demo on GitHub repository.', font=f_sm, fill='#334155')
draw.text((1345, 1150), '- Live Real-Bin Pilot Telemetry: Continuous 5-point thermal & CO2 logs validated at Rashtriya Raksha University.', font=f_sm, fill='#334155')
draw.text((1345, 1175), '- Hardware Replay Simulation: Run python -m tools.replay_sim to view full dashboard without live hardware.', font=f_sm, fill='#334155')
draw.text((1345, 1200), '- Contact & Institutional Verification: Team Vermikendra, RRU Gujarat | Email: atharveeee@gmail.com', font=f_sm_b, fill='#0f172a')


# ----------------- 5. FOOTER -----------------
draw.text((W/2, 1395), 'Comprehensive Peer-Reviewed References  |  Rashtriya Raksha University, Gujarat  |  Team ID: HSC|GJ|00009  |  Hack for Social Cause 2027', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1420), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_7_references_master.jpg'
canvas.save(out_path, quality=95)
print('Master Slide 7 References generated successfully at:', out_path)
