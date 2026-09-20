import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_name = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
f_role = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_desc = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
f_sec_hdr = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
f_gantt_task = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Team Composition & Engineering Leadership', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Multi-Disciplinary Expertise Mapping & Systems Engineering Execution Roadmap', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# ----------------- 2. ENGINEERING RESPONSIBILITY MAP (TEAM) -----------------
draw.text((60, 130), 'Core Engineering Competencies', font=f_sec_hdr, fill='#0f172a')

team = [
    {
        "name": "Atharve",
        "role": "Lead Hardware & RF Engineer",
        "color": "#ea580c",
        "bg": "#fff7ed",
        "contrib": [
            "• Architected custom IoT sensor array (DS18B20/SCD41).",
            "• Engineered 18µA deep-sleep power budget & solar MPPT.",
            "• Designed IP65 enclosure & active thermal management.",
            "• Optimized LoRa radio link margin for rural deployment."
        ]
    },
    {
        "name": "Akshit",
        "role": "Edge Firmware & Machine Learning",
        "color": "#0284c7",
        "bg": "#f0f9ff",
        "contrib": [
            "• Developed offline finite state machine for autonomous control.",
            "• Implemented edge-predictive thermal runaway algorithm.",
            "• Wrote C/C++ driver code for sensor DMA polling.",
            "• Built automated self-calibration for NDIR CO2 sensors."
        ]
    },
    {
        "name": "Charvi",
        "role": "Cloud Architect & Full-Stack",
        "color": "#16a34a",
        "bg": "#f0fdf4",
        "contrib": [
            "• Deployed AWS/GCP telemetry ingestion pipeline & DB.",
            "• Designed interactive React/Node.js operator dashboard.",
            "• Built automated SMS alerting system for SHG workers.",
            "• Executed empirical kinetics data analysis and visualization."
        ]
    }
]

box_w = 750
box_gap = 45
box_h = 320
y_team = 180
start_x = (W - (3*box_w + 2*box_gap)) // 2

for i, t in enumerate(team):
    bx = start_x + i * (box_w + box_gap)
    draw.rounded_rectangle([(bx, y_team), (bx+box_w, y_team+box_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
    draw.rounded_rectangle([(bx, y_team), (bx+box_w, y_team+70)], radius=16, fill=t['bg'], outline=t['color'], width=2)
    # square off bottom of header
    draw.rectangle([(bx, y_team+40), (bx+box_w, y_team+70)], fill=t['bg'])
    
    draw.text((bx+30, y_team+25), t['name'], font=f_name, fill='#0f172a')
    draw.text((bx+30, y_team+75), 'ROLE: ' + t['role'], font=f_role, fill=t['color'])
    
    cy = y_team + 130
    for line in t['contrib']:
        draw.text((bx+30, cy), line, font=f_desc, fill='#334155')
        cy += 40

# ----------------- 3. ENGINEERING ROADMAP (GANTT) -----------------
draw.text((60, 560), 'Execution Timeline & Deployment Roadmap', font=f_sec_hdr, fill='#0f172a')

# We will draw a clean Gantt chart
gantt_y = 610
gantt_h = 680
draw.rounded_rectangle([(60, gantt_y), (W-60, gantt_y+gantt_h)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)

# Months header
months = ["M1: Lab Synth", "M2: Prototype", "M3: Bio-Stress", "M4: Hackathon", "M5: Pilot 20-Bin", "M6: Scale-Up"]
col_w = (W - 120 - 350) // 6

draw.rectangle([(60, gantt_y), (W-60, gantt_y+50)], fill='#f8fafc')
for i, m in enumerate(months):
    mx = 60 + 350 + i * col_w
    draw.text((mx + col_w/2, gantt_y + 25), m, font=f_role, fill='#475569', anchor='mm')
    # Vertical grid lines
    draw.line([(mx, gantt_y+50), (mx, gantt_y+gantt_h)], fill='#e2e8f0', width=1)

tasks = [
    ("Phase 1: Sensor Eval & Hardware Design", 0, 1.5, "#ea580c"),
    ("Phase 2: Edge Firmware State Machine", 0.5, 2.5, "#0284c7"),
    ("Phase 3: Telemetry Cloud Pipeline Integration", 1.5, 3.0, "#16a34a"),
    ("Phase 4: Live Biomass Thermal Stress Test", 2.0, 3.5, "#dc2626"),
    ("Phase 5: National Tech Demonstration", 3.0, 4.0, "#7c3aed"),
    ("Phase 6: Cluster Rollout (20-Bin SHG Pilot)", 4.0, 5.5, "#d97706"),
    ("Phase 7: Long-Term Kinetics Evaluation", 4.5, 6.0, "#059669")
]

ty = gantt_y + 80
for task, start, end, color in tasks:
    # Task Name
    draw.text((80, ty+10), task, font=f_gantt_task, fill='#0f172a')
    # Task Bar
    bar_x1 = 60 + 350 + int(start * col_w)
    bar_x2 = 60 + 350 + int(end * col_w)
    draw.rounded_rectangle([(bar_x1, ty), (bar_x2, ty+35)], radius=17, fill=color)
    ty += 80

# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1380), 'Peer-Reviewed Systems Engineering Leadership | Rashtriya Raksha University, Gujarat | School of Applied Sciences, Technology & National Security', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1410), '@HSC submission- Template | Team ID: HSC|GJ|00009', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_5_team_research_journal.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 6 (Team) generated successfully at:', out_path)
