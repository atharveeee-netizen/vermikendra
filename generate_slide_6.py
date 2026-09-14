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
f_kpi_val = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
f_kpi_lbl = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
f_body = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
f_body_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 25), (280, 80)], radius=27, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 52), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24), fill='#9a3412', anchor='mm')

draw.text((W/2, 45), 'Feasibility and Risk Analysis', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 88), 'Technical Viability, Offline Operational Readiness, Failsafe Architecture & Risk Mitigation Matrix', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 25), (W-60, 80)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 41), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#16a34a', anchor='mm')
draw.text((W-200, 63), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#0f172a', anchor='mm')

draw.line([(60, 105), (W-60, 105)], fill='#e2e8f0', width=2)

# ----------------- 2. TOP SECTION: 3 CORE FEASIBILITY PILLARS (y: 118 to 610) -----------------
f_pillars = [
    {
        'title': '1. Technical Feasibility',
        'subtitle': 'Hardware, Embedded Firmware & Wireless PHY',
        'badge': 'HARDWARE & RF',
        'color': '#0284c7',
        'bg': '#f0f9ff',
        'border': '#7dd3fc',
        'points': [
            ('COTS Industrial Hardware:', 'Utilizes globally proven Nordic nRF52840 (ARM Cortex-M4F) and Semtech SX1262 transceiver integrated on the RAK4631 module.'),
            ('License-Exempt Long Range Radio:', 'Operates on 865.0625 MHz (India license-exempt band) at SF9/125kHz, achieving 2+ km range across farm sheds without SIM cards.'),
            ('Validated Sensor Suite:', 'Combines rugged DS18B20 1-Wire waterproof probes, photoacoustic Sensirion SCD41 CO2, and 4x shear-beam load cells with HX711.'),
            ('Autonomous Solar Budget:', '6V/2W solar panel + TP4056 + 3000mAh 18650 Li-ion cell. With 18uA sleep current, the system delivers >7 days zero-sun autonomy.')
        ]
    },
    {
        'title': '2. Operational & Field Feasibility',
        'subtitle': '100% Offline Resilience & Low-Literacy Usability',
        'badge': 'RURAL DEPLOYMENT',
        'badge_bg': '#16a34a',
        'color': '#16a34a',
        'bg': '#f0fdf4',
        'border': '#86efac',
        'points': [
            ('Zero Cellular / Cloud Dependency:', 'Gateway Raspberry Pi CM4 operates fully offline, broadcasting a local WiFi hotspot (192.168.4.1) directly to operator phones.'),
            ('Universal Low-Literacy UX:', 'Designed with high-contrast color cards (Green/Amber/Red), simple iconography, and audio voice prompts in Gujarati, Hindi & English.'),
            ('Edge Safety Independence:', 'The node firmware autonomously triggers cooling misting if temp exceeds 33C, protecting worms even if the gateway is powered down.'),
            ('No Manual Paperwork:', 'Lid-tilt accelerometer + weighing platform automatically logs feed additions (+kg) and compost harvests (-kg) without manual data entry.')
        ]
    },
    {
        'title': '3. Economic & Commercial Feasibility',
        'subtitle': 'Cluster Scalability, Payback & Scheme Fit',
        'badge': 'FINANCIAL ROI',
        'badge_bg': '#d97706',
        'color': '#d97706',
        'bg': '#fffbeb',
        'border': '#fde68a',
        'points': [
            ('1 Gateway : 20 Bins Topology:', 'One central gateway serves an entire village cluster, driving satellite node costs down to a fraction of traditional industrial monitoring.'),
            ('Sub-4-Month Capital Payback:', 'Hardware investment recovered within 2 harvest cycles (~4 months) purely by preventing a single catastrophic earthworm colony loss.'),
            ('2.5x Market Price Realization:', 'Verified respiration maturity certificates allow SHGs to sell packaged vermicompost at Rs.12-15/kg vs Rs.5-6/kg uncertified bulk rates.'),
            ('National Mission Subsidies:', 'Eligible for village infrastructure grants under GOBARdhan, Swachh Bharat Mission (Grameen) II, and DAY-NRLM Lakhpati Didi funding.')
        ]
    }
]

p_w = 786
p_gap = 21
p_y = 118
p_h = 480

for i, p in enumerate(f_pillars):
    px = 60 + i * (p_w + p_gap)
    draw.rounded_rectangle([(px, p_y), (px + p_w, p_y + p_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
    draw.rounded_rectangle([(px, p_y), (px + p_w, p_y + 75)], radius=16, fill=p['bg'], outline=p['border'], width=1)
    
    draw.text((px + 20, p_y + 24), p['title'], font=f_head, fill='#0f172a')
    draw.text((px + 20, p_y + 50), p['subtitle'], font=f_sm_b, fill=p['color'])
    
    # Pill
    draw.rounded_rectangle([(px + p_w - 170, p_y + 15), (px + p_w - 15, p_y + 45)], radius=8, fill=p['color'])
    draw.text((px + p_w - 92, p_y + 30), p['badge'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12), fill='#ffffff', anchor='mm')
    
    iy = p_y + 92
    for title, desc in p['points']:
        draw.ellipse([(px + 20, iy + 6), (px + 28, iy + 14)], fill=p['color'])
        draw.text((px + 38, iy), title, font=f_subhead, fill='#0f172a')
        iy += 24
        
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
            draw.text((px + 38, iy), l, font=f_body, fill='#334155')
            iy += 21
        iy += 8

# ----------------- 3. LOWER SECTION: RISK REGISTER & MITIGATION MATRIX (y: 615 to 1340) -----------------
r_y = 615
r_h = 715
draw.rounded_rectangle([(60, r_y), (W - 60, r_y + r_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)

draw.rounded_rectangle([(60, r_y), (W - 60, r_y + 50)], radius=16, fill='#f8fafc', outline='#cbd5e1', width=1)
draw.text((W/2, r_y + 25), 'Comprehensive Risk Register & Engineering Mitigation Strategies (TRD FMEA Matrix)', font=f_head, fill='#0f172a', anchor='mm')

risks = [
    {
        'id': 'R1',
        'name': 'Corrosive Environment (Ammonia & 90%+ RH)',
        'level': 'SEVERITY: MEDIUM',
        'level_bg': '#ea580c',
        'impact': 'Condensation and bio-gas degrade exposed sensor circuitry, leading to measurement drift or node failure.',
        'strategy': 'IP65 ABS sealed enclosures, ePTFE hydrophobic breathable membrane (passes gas, blocks liquid), active 40mm flush fan, and conformal polyurethane PCB coating.',
        'owner': 'Hardware / ECE'
    },
    {
        'id': 'R2',
        'name': 'Solar Deprivation & Prolonged Monsoon Rains',
        'level': 'SEVERITY: MEDIUM',
        'level_bg': '#ea580c',
        'impact': 'Cloudy skies for 5+ days exhaust battery storage, shutting down LoRa telemetry and real-time monitoring.',
        'strategy': 'Aggressive duty-cycling (18uA deep sleep), switched 3V3_S power rail, actuators on separate supply, and 3000mAh 18650 cell providing >7 days zero-sun autonomy.',
        'owner': 'Hardware / ECE'
    },
    {
        'id': 'R3',
        'name': 'Lethal Compost Overheating (>35C Heat Spikes)',
        'level': 'SEVERITY: HIGH',
        'level_bg': '#dc2626',
        'impact': 'Fresh dung decomposition creates rapid thermal pockets that kill worms before operators notice surface heat.',
        'strategy': '5-point depth array catches hidden hot layers; 1D thermal diffusion model forecasts breach 60 min ahead; autonomous edge misting triggers locally without gateway.',
        'owner': 'Embedded Firmware'
    },
    {
        'id': 'R4',
        'name': 'SCD41 NDIR CO2 Sensor Baseline Drift',
        'level': 'SEVERITY: MEDIUM',
        'level_bg': '#ea580c',
        'impact': 'Automatic self-calibration assumes fresh outdoor air (400ppm), drifting erroneous baselines inside compost headspace.',
        'strategy': 'Disabled automatic self-calibration in firmware; forced outdoor fresh air calibration every 2 weeks; R2 > 0.95 linear regression quality gating on respiration slope.',
        'owner': 'Firmware & Analytics'
    },
    {
        'id': 'R5',
        'name': 'Outdoor Load Cell Creep & Thermal Hysteresis',
        'level': 'SEVERITY: LOW',
        'level_bg': '#0284c7',
        'impact': 'Daily ambient temperature swings (+-15C) cause baseline mass drift, corrupting static weight readings.',
        'strategy': 'Software tracks short-window differential mass steps (+-0.3kg) during lid-tilt interrupts rather than absolute static weight; automatic tare reset at harvest.',
        'owner': 'Gateway Software'
    },
    {
        'id': 'R6',
        'name': 'Gateway Hardware Supply & Radio Interface Delay',
        'level': 'SEVERITY: MEDIUM',
        'level_bg': '#ea580c',
        'impact': 'Supply chain delay in CM4 carrier boards or radio HAT pin incompatibility halts demonstration and deployment.',
        'strategy': 'Portable gateway architecture: runs identically on any Linux laptop via USB serial fallback (/dev/ttyUSB0 CP2102); pre-tested radio spike tests with packet replay simulator.',
        'owner': 'Gateway & Backend'
    }
]

# 2 Columns x 3 Rows
rx_w = 1190
rx_gap = 20
rx_h = 195
rx_y_start = r_y + 65

for i, r in enumerate(risks):
    col = i % 2
    row = i // 2
    
    rx = 60 + 15 + col * (rx_w + rx_gap)
    ry = rx_y_start + row * (rx_h + 15)
    
    draw.rounded_rectangle([(rx, ry), (rx + rx_w, ry + rx_h)], radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    
    # Left accent bar
    draw.rounded_rectangle([(rx, ry), (rx + 8, ry + rx_h)], radius=4, fill=r['level_bg'])
    
    # ID pill
    draw.rounded_rectangle([(rx + 18, ry + 12), (rx + 65, ry + 42)], radius=6, fill='#1e293b')
    draw.text((rx + 41, ry + 27), r['id'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16), fill='#ffffff', anchor='mm')
    
    # Title
    draw.text((rx + 80, ry + 16), r['name'], font=f_subhead, fill='#0f172a')
    
    # Level Badge
    draw.rounded_rectangle([(rx + rx_w - 180, ry + 12), (rx + rx_w - 15, ry + 42)], radius=6, fill=r['level_bg'])
    draw.text((rx + rx_w - 97, ry + 27), r['level'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11), fill='#ffffff', anchor='mm')
    
    # Impact
    draw.text((rx + 18, ry + 54), 'Potential Risk Impact:', font=f_sm_b, fill='#dc2626')
    words_i = r['impact'].split()
    l1 = ' '.join(words_i[:18])
    l2 = ' '.join(words_i[18:])
    draw.text((rx + 175, ry + 54), l1, font=f_sm, fill='#334155')
    if l2:
        draw.text((rx + 175, ry + 74), l2, font=f_sm, fill='#334155')
        
    # Mitigation Strategy
    draw.text((rx + 18, ry + 102), 'Mitigation Strategy:', font=f_sm_b, fill='#16a34a')
    words_s = r['strategy'].split()
    s1 = ' '.join(words_s[:16])
    s2 = ' '.join(words_s[16:32])
    s3 = ' '.join(words_s[32:])
    draw.text((rx + 175, ry + 102), s1, font=f_sm, fill='#0f172a')
    draw.text((rx + 175, ry + 122), s2, font=f_sm, fill='#0f172a')
    if s3:
        draw.text((rx + 175, ry + 142), s3, font=f_sm, fill='#334155')
        
    # Owner tag
    draw.text((rx + 18, ry + 168), 'Workstream Owner: ' + r['owner'], font=f_sm_b, fill='#64748b')

# ----------------- 4. BOTTOM FOOTER & TEMPLATE WATERMARK -----------------
draw.text((W/2, 1360), 'Rigorous Engineering Verification: FMEA Risk Analysis | Hardware Watchdog | Autonomous Edge Failsafe | Tested at Rashtriya Raksha University Labs', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1395), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14), fill='#94a3b8', anchor='mm')

out_path = 'slide_6_feasibility_risk_master.jpg'
canvas.save(out_path, quality=95)
print('Master Slide 6 generated successfully at:', out_path)
