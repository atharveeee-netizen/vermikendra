import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#f8fafc')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 46)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 21)
f_head = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24)
f_subhead = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_name = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
f_role = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17)
f_body = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
f_body_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 25), (280, 80)], radius=27, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 52), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24), fill='#9a3412', anchor='mm')

draw.text((W/2, 45), 'Team Vermikendra & Engineering Leadership', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 88), 'Rashtriya Raksha University (RRU), Gujarat  |  Team ID: HSC|GJ|00009  |  Multi-Disciplinary Synergy', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 25), (W-60, 80)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 41), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#16a34a', anchor='mm')
draw.text((W-200, 63), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#0f172a', anchor='mm')

draw.line([(60, 105), (W-60, 105)], fill='#e2e8f0', width=2)

# ----------------- 2. TOP SECTION: 3 MEMBER PROFILE CARDS (y: 118 to 780) -----------------
members = [
    {
        'name': 'Atharve Dahima',
        'branch': 'Electronics & Communication Engineering (ECE)',
        'role': 'Hardware, Embedded Firmware & Power Systems Lead',
        'badge': 'ECE LEAD',
        'badge_bg': '#ea580c',
        'border': '#fdba74',
        'bg': '#fff7ed',
        'avatar_text': 'AD',
        'deliverables': [
            ('Embedded Node Firmware:', 'Authored C++ firmware on RAK4631 (nRF52840) with FreeRTOS / PlatformIO; integrated 1-Wire & I2C drivers.'),
            ('Sensor Suite Integration:', 'Wired & calibrated 5-point DS18B20 depth probes, Sensirion SCD41 CO2 pod, BME688, and HX711 load cells.'),
            ('Ultra-Low-Power Profiling:', 'Designed power sequencing with low-quiescent LDO and switched 3V3_S rail; achieved 18uA deep-sleep current.'),
            ('Solar Energy Harvesting:', 'Calculated battery power budget; integrated 6V/2W solar panel, TP4056 charger, and 3000mAh 18650 Li-ion cell (>7d autonomy).'),
            ('Mechanical Enclosure & Prototyping:', 'Designed IP65 junction box housing, ePTFE hydrophobic vent, cable glands, and lid pod airflow duct.')
        ],
        'tech_stack': 'C++ | PlatformIO | nRF52840 | LoRa SX1262 | 1-Wire | KiCad'
    },
    {
        'name': 'Akshit Agarwal',
        'branch': 'Computer Science & Engineering (CSE)',
        'role': 'Gateway Architecture, Backend & ML Analytics Lead',
        'badge': 'CSE BACKEND & ML',
        'badge_bg': '#0284c7',
        'border': '#7dd3fc',
        'bg': '#f0f9ff',
        'avatar_text': 'AA',
        'deliverables': [
            ('Raspberry Pi CM4 Architecture:', 'Configured headless Linux systemd services, Waveshare SX1262 LoRa HAT UART interface, and hardware watchdog.'),
            ('High-Performance IPC Ingestion:', 'Architected decoupled message broker using Mosquitto MQTT; implemented Python serial packet deserializer.'),
            ('Offline REST & WebSocket Server:', 'Built asynchronous FastAPI & Uvicorn application layer pushing real-time telemetry to connected clients.'),
            ('Time-Series Persistence:', 'Designed SQLite3 database with Write-Ahead Logging (WAL) and automated 90-day time-series retention schema.'),
            ('Predictive Analytics Engine:', 'Implemented 1D thermal diffusion (dT/dt) early risk forecasting and linear regression slope for CO2 respiration kinetics.')
        ],
        'tech_stack': 'Python 3.10 | FastAPI | SQLite3 WAL | Mosquitto MQTT | Scikit-Learn | Linux'
    },
    {
        'name': 'Charvi Meddita',
        'branch': 'Computer Science & Engineering (CSE)',
        'role': 'Frontend PWA, Multi-lingual UX & Product Strategy Lead',
        'badge': 'CSE FRONTEND & PRODUCT',
        'badge_bg': '#7c3aed',
        'border': '#c4b5fd',
        'bg': '#f5f3ff',
        'avatar_text': 'CM',
        'deliverables': [
            ('Offline-First PWA Dashboard:', 'Engineered responsive Progressive Web App in React, Vite & Tailwind CSS served entirely from CM4 hotspot.'),
            ('Low-Literacy Universal UX:', 'Designed high-visibility color hierarchy (Green/Amber/Red), action-driven cards, and tactile status cards for rural users.'),
            ('Multilingual Localization (i18n):', 'Implemented complete regional localization in Gujarati, Hindi, and English with voice-guided alert prompts.'),
            ('Traceable Batch Records:', 'Built automated batch history ledger and scannable QR verification certificates for commercial compost buyers.'),
            ('Field Research & User Flows:', 'Mapped operator journeys (J1-J5); conducted usability testing with non-technical village composting stakeholders.')
        ],
        'tech_stack': 'React 18 | Vite | Tailwind CSS | PWA | Chart.js | i18n Localization'
    }
]

card_w = 786
card_gap = 21
card_y = 118
card_h = 670

for i, m in enumerate(members):
    cx = 60 + i * (card_w + card_gap)
    draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + card_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
    
    # Top card banner
    draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + 90)], radius=16, fill=m['bg'], outline=m['border'], width=1)
    
    # Avatar circle
    draw.ellipse([(cx + 18, card_y + 15), (cx + 78, card_y + 75)], fill=m['badge_bg'])
    draw.text((cx + 48, card_y + 45), m['avatar_text'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24), fill='#ffffff', anchor='mm')
    
    # Name & Branch
    draw.text((cx + 95, card_y + 24), m['name'], font=f_name, fill='#0f172a')
    draw.text((cx + 95, card_y + 54), m['branch'], font=f_sm_b, fill='#475569')
    
    # Badge Pill
    draw.rounded_rectangle([(cx + card_w - 175, card_y + 15), (cx + card_w - 15, card_y + 45)], radius=8, fill=m['badge_bg'])
    draw.text((cx + card_w - 95, card_y + 30), m['badge'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12), fill='#ffffff', anchor='mm')
    
    # Role banner
    draw.rounded_rectangle([(cx + 15, card_y + 102), (cx + card_w - 15, card_y + 138)], radius=8, fill='#f1f5f9')
    draw.text((cx + card_w/2, card_y + 120), m['role'], font=f_role, fill='#1e293b', anchor='mm')
    
    # Deliverables bullets
    dy = card_y + 150
    for title, desc in m['deliverables']:
        draw.ellipse([(cx + 18, dy + 5), (cx + 25, dy + 12)], fill=m['badge_bg'])
        draw.text((cx + 35, dy), title, font=f_subhead, fill='#0f172a')
        dy += 24
        
        words = desc.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(' '.join(cur)) > 62:
                cur.pop()
                lines.append(' '.join(cur))
                cur = [w]
        if cur:
            lines.append(' '.join(cur))
        for l in lines:
            draw.text((cx + 35, dy), l, font=f_body, fill='#334155')
            dy += 21
        dy += 10
        
    # Tech stack tag bottom bar
    draw.rounded_rectangle([(cx + 15, card_y + card_h - 48), (cx + card_w - 15, card_y + card_h - 12)], radius=8, fill=m['bg'], outline=m['border'], width=1)
    draw.text((cx + 25, card_y + card_h - 30), 'Stack Owned:', font=f_sm_b, fill=m['badge_bg'])
    draw.text((cx + 125, card_y + card_h - 30), m['tech_stack'], font=f_sm_b, fill='#1e293b')

# ----------------- 3. LOWER SECTION: CHALLENGES & JOURNEY (y: 800 to 1340) -----------------
low_y = 800
low_h = 530

# LEFT COLUMN: Technical Challenges & Engineering Solutions (w = 1190)
c_box = [(60, low_y), (1250, low_y + low_h)]
draw.rounded_rectangle(c_box, radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
draw.rounded_rectangle([(60, low_y), (1250, low_y + 50)], radius=16, fill='#f8fafc', outline='#cbd5e1', width=1)
draw.text((655, low_y + 25), 'Engineering Challenges Faced & Overcome', font=f_head, fill='#0f172a', anchor='mm')

challenges = [
    {
        'title': '1. Off-Grid Power Budget & Monsoon Autonomy (Hardware / ECE)',
        'prob': 'Initial active prototyping drew >120mA continuously, depleting batteries within 24 hours under cloudy skies.',
        'sol': 'Engineered aggressive sleep duty-cycling (18uA deep sleep) via low-quiescent LDO, switched 3V3_S sensor power rails, and optimized LoRa SF9 transmit bursts, achieving >7 days zero-sun autonomy.',
        'col': '#ea580c'
    },
    {
        'title': '2. Complete Internet Independence & Offline Hotspot (Backend / CSE)',
        'prob': 'Cellular 4G dongles in rural farms suffer frequent signal drops, causing cloud telemetry loss and dashboard freeze.',
        'sol': 'Pivoted to a 100% offline-first architecture on the Raspberry Pi CM4. Serves its own standalone WiFi access point (192.168.4.1) hosting the FastAPI backend, SQLite DB, and local PWA with zero cloud dependency.',
        'col': '#0284c7'
    },
    {
        'title': '3. Biological Respiration vs. Ambient Noise (AI & UX / CSE)',
        'prob': 'Ambient temperature and wind caused erratic raw CO2 readings inside the compost headspace.',
        'sol': 'Designed an active lid pod with a 40mm flush fan running a 120s pre-flush followed by a 600s sealed chamber build-up. Scikit-learn linear regression calculates slope (ppm/min) with R2 > 0.95 quality gating.',
        'col': '#7c3aed'
    }
]

cy = low_y + 65
for ch in challenges:
    draw.rounded_rectangle([(75, cy), (1235, cy + 140)], radius=10, fill='#f8fafc', outline='#e2e8f0', width=1)
    draw.rounded_rectangle([(75, cy), (82, cy + 140)], radius=4, fill=ch['col'])
    
    draw.text((95, cy + 12), ch['title'], font=f_subhead, fill='#0f172a')
    draw.text((95, cy + 40), 'Challenge:', font=f_sm_b, fill='#dc2626')
    
    words = ch['prob'].split()
    l1 = ' '.join(words[:14])
    l2 = ' '.join(words[14:])
    draw.text((175, cy + 40), l1, font=f_sm, fill='#334155')
    if l2:
        draw.text((175, cy + 58), l2, font=f_sm, fill='#334155')
        
    draw.text((95, cy + 82), 'Solution:', font=f_sm_b, fill='#16a34a')
    words_s = ch['sol'].split()
    s1 = ' '.join(words_s[:15])
    s2 = ' '.join(words_s[15:30])
    s3 = ' '.join(words_s[30:])
    draw.text((175, cy + 82), s1, font=f_sm, fill='#334155')
    draw.text((175, cy + 100), s2, font=f_sm, fill='#334155')
    if s3:
        draw.text((175, cy + 118), s3, font=f_sm, fill='#475569')
    cy += 150

# RIGHT COLUMN: Team Journey, Mentorship & Vision (w = 1190)
j_box = [(1270, low_y), (W - 60, low_y + low_h)]
draw.rounded_rectangle(j_box, radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
draw.rounded_rectangle([(1270, low_y), (W - 60, low_y + 50)], radius=16, fill='#f8fafc', outline='#cbd5e1', width=1)
draw.text((1915, low_y + 25), 'Our Engineering Journey & Vision for Bharat', font=f_head, fill='#0f172a', anchor='mm')

journey_milestones = [
    {
        'phase': 'Phase 1: Problem Discovery & Ground Reality',
        'date': 'Aug 2026',
        'text': 'Visited rural vermiculture beds in Gujarat. Saw women SHGs abandon units after silent heat waves wiped out entire earthworm populations. Identified critical need for multi-depth thermal telemetry.',
        'icon_bg': '#ea580c'
    },
    {
        'phase': 'Phase 2: Hardware-Software Co-Design at RRU Labs',
        'date': 'Sep 2026',
        'text': 'Combined ECE circuit engineering with CSE systems architecture at Rashtriya Raksha University. Sourced sensors, built WisBlock LoRa prototype, 3D printed lid pods, and coded the offline gateway daemon.',
        'icon_bg': '#0284c7'
    },
    {
        'phase': 'Phase 3: Live Real-Bin Validation & Stress Testing',
        'date': 'Late Sep 2026',
        'text': 'Instrumented a live pilot bin with live Eisenia fetida worms. Successfully validated autonomous misting during 33C heat spikes, verified respiration plateau against manual maturity, and refined Gujarati UI.',
        'icon_bg': '#16a34a'
    },
    {
        'phase': 'Phase 4: Scaling Vision & National Field Deployment',
        'date': 'Oct 2026 - 2027',
        'text': 'Partnering with local Krishi Vigyan Kendras (KVK) and DAY-NRLM cluster federations to deploy 20-bin village clusters under GOBARdhan and Swachh Bharat Phase II, scaling Lakhpati Didi enterprises.',
        'icon_bg': '#7c3aed'
    }
]

jy = low_y + 65
for jm in journey_milestones:
    draw.rounded_rectangle([(1285, jy), (W - 75, jy + 105)], radius=10, fill='#f8fafc', outline='#e2e8f0', width=1)
    
    # Milestone pill
    draw.rounded_rectangle([(1295, jy + 10), (1400, jy + 36)], radius=6, fill=jm['icon_bg'])
    draw.text((1347, jy + 23), jm['date'], font=f_sm_b, fill='#ffffff', anchor='mm')
    
    draw.text((1415, jy + 15), jm['phase'], font=f_subhead, fill='#0f172a')
    
    words = jm['text'].split()
    l1 = ' '.join(words[:18])
    l2 = ' '.join(words[18:36])
    l3 = ' '.join(words[36:])
    draw.text((1300, jy + 45), l1, font=f_sm, fill='#334155')
    draw.text((1300, jy + 65), l2, font=f_sm, fill='#334155')
    if l3:
        draw.text((1300, jy + 85), l3, font=f_sm, fill='#475569')
    jy += 115

# ----------------- 4. BOTTOM FOOTER & TEMPLATE WATERMARK -----------------
draw.text((W/2, 1360), 'Rashtriya Raksha University, Gujarat  |  School of Applied Sciences, Technology & National Security  |  Mentorship: KVK & Agriculture Extension Experts', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1395), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14), fill='#94a3b8', anchor='mm')

out_path = 'slide_5_team_master.jpg'
canvas.save(out_path, quality=95)
print('Master Slide 5 generated successfully at:', out_path)
