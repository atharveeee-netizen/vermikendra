import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_callout = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_body = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 11)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Technical Approach & System Architecture', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Peer-Reviewed Systems Engineering: Hardware Instrumentation, Firmware State Machine, Power Timing & Predictive Kinetics', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# Helper function for card containers
def draw_panel(box, title):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    # Header bar
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 36)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 15, box[0][1] + 18), title, font=f_fig_title, fill='#0f172a', anchor='lm')

# ----------------- 2. ROW 1 (y: 105 to 735, h=630) -----------------
# PANEL 1: Physical Bin CAD (Left: w=870)
b1 = [(60, 105), (930, 735)]
draw_panel(b1, 'Fig. 1. Physical Bin CAD Cutaway & Depth Sensor Array')

im_bin = Image.open('academic_isometric_bin_1789388647042.jpg')
# Target size ~840 x 470
w_target = 840
h_target = int(im_bin.height * (w_target / im_bin.width))
if h_target > 480:
    h_target = 480
    w_target = int(im_bin.width * (h_target / im_bin.height))
im_bin_res = im_bin.resize((w_target, h_target), Image.Resampling.LANCZOS)
px = 60 + (870 - w_target)//2
canvas.paste(im_bin_res, (px, 150))

# Concise Callouts under Fig. 1
callouts_1 = [
    ('[A] 5-Point 1-Wire Array:', 'DS18B20 at 5cm, 15cm (core & wall), 25cm to detect lethal heat inversion.'),
    ('[B] Respiration Lid Pod:', 'SCD41 NDIR CO2 + BME688 + LIS3DH lid-tilt + 40mm 5V flush fan.'),
    ('[C] Mass Platform:', '4x 50kg shear-beam load cells + HX711 (+-200g automatic feed/harvest log).'),
    ('[D] Solar Harvesting:', '6V/2W panel + TP4056 + 3000mAh 18650 Li-ion cell (18uA sleep, >7d autonomy).')
]
cy = 150 + h_target + 8
for tag, desc in callouts_1:
    draw.text((75, cy), tag, font=f_sm_b, fill='#0284c7')
    draw.text((260, cy), desc, font=f_sm, fill='#334155')
    cy += 20


# PANEL 2: Architectural Pipeline Schematic (Center: w=960)
b2 = [(950, 105), (1910, 735)]
draw_panel(b2, 'Fig. 2. End-to-End Signal Pipeline & Offline Gateway Architecture')

im_diag = Image.open('vermikendra_academic_diagram_1789388354923.jpg')
w_d = 930
h_d = int(im_diag.height * (w_d / im_diag.width))
if h_d > 520:
    h_d = 520
    w_d = int(im_diag.width * (h_d / im_diag.height))
im_diag_res = im_diag.resize((w_d, h_d), Image.Resampling.LANCZOS)
px2 = 950 + (960 - w_d)//2
canvas.paste(im_diag_res, (px2, 148))

# Concise Callout under Fig. 2
pipeline_text = 'Signal Path: RAK4631 (nRF52840) --[LoRa P2P 865MHz SF9 44B Signed]--> Raspberry Pi CM4 Gateway (/dev/ttyUSB0) --> Mosquitto MQTT --> FastAPI --> SQLite WAL --> Offline PWA (192.168.4.1)'
draw.text((965, 148 + h_d + 12), pipeline_text, font=f_sm_b, fill='#0f172a')


# PANEL 3: Technology Stack Grid (Right: w=570)
b3 = [(1930, 105), (2500, 735)]
draw_panel(b3, 'Fig. 3. Full-Stack Technology Matrix')

tech_badges = [
    ('C++ / Arduino', 'RAK4631 Firmware', '#00599C'),
    ('Python 3.10+', 'Gateway Daemon', '#3776AB'),
    ('FastAPI', 'Offline REST & WS', '#05998B'),
    ('SQLite3 WAL', 'Time-Series DB', '#003B57'),
    ('React / Vite', 'Offline Mobile PWA', '#0284c7'),
    ('LoRa SX1262', '865 MHz P2P PHY', '#b91c1c'),
    ('Mosquitto', 'MQTT IPC Broker', '#475569'),
    ('Scikit-Learn', 'Thermal & ODE ML', '#d97706')
]

# 2 columns x 4 rows
bw = 255
bh = 115
bx_gap = 20
by_gap = 14
start_bx = 1950
start_by = 155

for i, (name, role, color) in enumerate(tech_badges):
    col = i % 2
    row = i // 2
    tx = start_bx + col * (bw + bx_gap)
    ty = start_by + row * (bh + by_gap)
    
    draw.rounded_rectangle([(tx, ty), (tx + bw, ty + bh)], radius=10, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.rounded_rectangle([(tx, ty), (tx + 8, ty + bh)], radius=4, fill=color)
    
    # Icon circle placeholder with initials
    draw.ellipse([(tx + 18, ty + 25), (tx + 65, ty + 72)], fill=color)
    initials = name.split()[0][:3]
    draw.text((tx + 41, ty + 48), initials, font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13), fill='#ffffff', anchor='mm')
    
    draw.text((tx + 75, ty + 32), name, font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14), fill='#0f172a')
    draw.text((tx + 75, ty + 56), role, font=f_sm, fill='#475569')
    draw.rounded_rectangle([(tx + 75, ty + 78), (tx + bw - 15, ty + 98)], radius=4, fill='#e2e8f0')
    draw.text((tx + 82, ty + 88), 'Production Verified', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 9), fill='#334155', anchor='lm')


# ----------------- 3. ROW 2 (y: 750 to 1375, h=625) -----------------
# PANEL 4: Respiration Kinetics & Depth Temperature Plots (Left: w=870)
b4 = [(60, 750), (930, 1375)]
draw_panel(b4, 'Fig. 4. Empirical Biological Kinetics & Depth Heat Inversion')

im_p1 = Image.open('scratch/plot_co2_kinetics.png')
im_p2 = Image.open('scratch/plot_depth_temp.png')

# Resize plots to fit side-by-side
pw_target = 410
ph_target = int(im_p1.height * (pw_target / im_p1.width))
if ph_target > 480:
    ph_target = 480
    pw_target = int(im_p1.width * (ph_target / im_p1.height))

im_p1_res = im_p1.resize((pw_target, ph_target), Image.Resampling.LANCZOS)
im_p2_res = im_p2.resize((pw_target, ph_target), Image.Resampling.LANCZOS)

canvas.paste(im_p1_res, (80, 800))
canvas.paste(im_p2_res, (505, 800))

draw.text((80, 800 + ph_target + 12), 'Key Evidence: Closed-lid CO2 plateau (18 ppm/min, R2=0.98) validates compost stability without lab tests.', font=f_sm_b, fill='#059669')
draw.text((80, 800 + ph_target + 32), 'Thermal Inversion: 5-point array detects lethal 34.2C core hotspot while surface appears normal (28C).', font=f_sm_b, fill='#dc2626')


# PANEL 5: Firmware State Machine & Power Timing (Center: w=960)
b5 = [(950, 750), (1910, 1375)]
draw_panel(b5, 'Fig. 5. Power Profiling (18 µA Sleep) & Autonomous Failsafe State Machine')

im_fsm = Image.open('scratch/firmware_power_statemachine.png')
w_fsm = 925
h_fsm = int(im_fsm.height * (w_fsm / im_fsm.width))
if h_fsm > 500:
    h_fsm = 500
    w_fsm = int(im_fsm.width * (h_fsm / im_fsm.height))
im_fsm_res = im_fsm.resize((w_fsm, h_fsm), Image.Resampling.LANCZOS)
px5 = 950 + (960 - w_fsm)//2
canvas.paste(im_fsm_res, (px5, 800))

draw.text((970, 800 + h_fsm + 16), 'Edge Safety Rule EF-1: If T >= 33C and Moisture < 75%, local misting activates autonomously without gateway.', font=f_sm_b, fill='#0284c7')


# PANEL 6: GitHub Repo QR & AI Tools Donut Infographic (Right: w=570)
b6 = [(1930, 750), (2500, 1375)]
draw_panel(b6, 'Fig. 6. Real Repository & Extent of AI Tools Usage')

# Top: QR Code
im_qr = Image.open('scratch/github_qr.png')
im_qr_res = im_qr.resize((210, 210), Image.Resampling.LANCZOS)
canvas.paste(im_qr_res, (1950, 800))

draw.text((2180, 820), 'Open Repository:', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15), fill='#0f172a')
draw.text((2180, 848), 'Scan for Source & Demo', font=f_sm_b, fill='#2563eb')
draw.text((2180, 878), 'https://github.com/', font=f_sm, fill='#475569')
draw.text((2180, 898), 'atharvedahima/vermikendra', font=f_sm_b, fill='#0f172a')
draw.rounded_rectangle([(2180, 930), (2475, 965)], radius=6, fill='#f1f5f9', outline='#cbd5e1', width=1)
draw.text((2190, 947), 'Live Code | Schematics | CAD', font=f_sm_b, fill='#334155', anchor='lm')

draw.line([(1950, 1030), (2480, 1030)], fill='#e2e8f0', width=1)

# Bottom: AI Donut chart
im_donut = Image.open('scratch/ai_usage_donut.png')
w_don = 510
h_don = int(im_donut.height * (w_don / im_donut.width))
if h_don > 310:
    h_don = 310
    w_don = int(im_donut.width * (h_don / im_donut.height))
im_don_res = im_donut.resize((w_don, h_don), Image.Resampling.LANCZOS)
canvas.paste(im_don_res, (1960, 1045))


# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1395), 'Journal Quality Technical Architecture  |  Rashtriya Raksha University, Gujarat  |  Team ID: HSC|GJ|00009  |  Multi-Disciplinary ECE & CSE Co-Design', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1420), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_3_research_journal_master.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 3 generated successfully at:', out_path)
