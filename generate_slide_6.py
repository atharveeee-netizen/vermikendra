import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_th = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_td = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
f_td_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Feasibility & Risk: Engineering Validation Matrix', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Comprehensive FMEA, Mitigation Strategies, and Physical Verification Status', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# ----------------- 2. VALIDATION MATRIX -----------------
matrix_data = [
    {
        "comp": "IoT Telemetry Node\n(Hardware)",
        "risk": "Corrosive Environment\n(NH3 & >90% RH)",
        "mitigation": "IP65 ABS sealed enclosures, ePTFE hydrophobic breathable membrane,\nactive 40mm flush fan, and conformal polyurethane PCB coating.",
        "test": "Accelerated humidity (95% RH) &\nNH3 chamber exposure (48 hrs)",
        "status": "BUILT",
        "bg": "#f0fdf4",
        "c_status": "#166534",
        "bg_status": "#bbf7d0"
    },
    {
        "comp": "Edge Firmware\n(State Machine)",
        "risk": "Lethal Compost Overheating\n(Heat Spikes >33°C)",
        "mitigation": "5-point DS18B20 depth array catches hidden hot layers.\nOffline local threshold triggers autonomous micro-misting without gateway.",
        "test": "Induced thermal runaway simulation\nusing active heating pads",
        "status": "BUILT",
        "bg": "#f0fdf4",
        "c_status": "#166534",
        "bg_status": "#bbf7d0"
    },
    {
        "comp": "Power Subsystem\n(Energy Budget)",
        "risk": "Solar Deprivation during\nProlonged Monsoon",
        "mitigation": "Aggressive duty-cycling (18µA deep sleep), switched 3V3_S power rail,\nand 3000mAh 18650 cell providing >7 days zero-sun autonomy.",
        "test": "7-day zero-sun continuous\noperation current drain test",
        "status": "VALIDATED",
        "bg": "#f0f9ff",
        "c_status": "#075985",
        "bg_status": "#bae6fd"
    },
    {
        "comp": "Gas Sensor (SCD41)\n(Analytics)",
        "risk": "NDIR CO2 Sensor\nBaseline Drift",
        "mitigation": "Disabled automatic self-calibration in firmware. Forced outdoor fresh air\ncalibration every 2 weeks. R² > 0.95 linear regression quality gating.",
        "test": "14-day continuous baseline\ndrift observation vs control",
        "status": "UNDER VALIDATION",
        "bg": "#fffbeb",
        "c_status": "#92400e",
        "bg_status": "#fde68a"
    },
    {
        "comp": "Static Load Cells\n(Mass Balance)",
        "risk": "Thermal Hysteresis &\nDiurnal Temp Drift",
        "mitigation": "Software tracks short-window differential mass steps (+-0.3kg) during\nlid-tilt interrupts rather than absolute static weight. Auto tare reset.",
        "test": "Diurnal temperature swing\nstatic mass drift test (+-15°C)",
        "status": "PLANNED",
        "bg": "#f8fafc",
        "c_status": "#475569",
        "bg_status": "#e2e8f0"
    },
    {
        "comp": "Gateway Radio (LoRa)\n(Comms)",
        "risk": "Supply Chain & Radio\nHAT Incompatibility",
        "mitigation": "Portable architecture: Gateway daemon runs identically on any Linux\nlaptop via USB serial fallback (/dev/ttyUSB0 CP2102) if HATs fail.",
        "test": "Packet replay simulator\nspike load testing (100 nodes)",
        "status": "BUILT",
        "bg": "#f0fdf4",
        "c_status": "#166534",
        "bg_status": "#bbf7d0"
    }
]

# Draw Table Headers
col_w = [250, 250, 750, 350, 250]
start_x = (W - sum(col_w)) // 2
y_tbl = 160
row_h = 160

headers = ["SYSTEM COMPONENT", "FAILURE MODE / RISK", "ENGINEERING MITIGATION", "VALIDATION TEST", "STATUS"]
hx = start_x
draw.rounded_rectangle([(start_x, y_tbl), (start_x + sum(col_w), y_tbl + 50)], radius=8, fill='#1e293b')
for i, h in enumerate(headers):
    draw.text((hx + 20, y_tbl + 25), h, font=f_th, fill='#ffffff', anchor='lm')
    hx += col_w[i]

y_tbl += 70

# Draw Table Rows
for idx, row in enumerate(matrix_data):
    # Row BG
    draw.rounded_rectangle([(start_x, y_tbl), (start_x + sum(col_w), y_tbl + row_h - 10)], radius=8, fill=row['bg'], outline='#cbd5e1', width=1)
    
    cx = start_x
    
    # 1. Comp
    draw.text((cx + 20, y_tbl + 40), row['comp'].split('\n')[0], font=f_td_b, fill='#0f172a')
    draw.text((cx + 20, y_tbl + 65), row['comp'].split('\n')[1], font=f_td, fill='#475569')
    cx += col_w[0]
    
    # 2. Risk
    draw.text((cx + 20, y_tbl + 40), row['risk'].split('\n')[0], font=f_td_b, fill='#dc2626')
    draw.text((cx + 20, y_tbl + 65), row['risk'].split('\n')[1], font=f_td, fill='#475569')
    cx += col_w[1]
    
    # 3. Mitigation
    lines = row['mitigation'].split('\n')
    draw.text((cx + 20, y_tbl + 40), lines[0], font=f_td, fill='#334155')
    if len(lines) > 1:
        draw.text((cx + 20, y_tbl + 65), lines[1], font=f_td, fill='#334155')
    cx += col_w[2]
    
    # 4. Test
    lines = row['test'].split('\n')
    draw.text((cx + 20, y_tbl + 40), lines[0], font=f_td, fill='#0f172a')
    if len(lines) > 1:
        draw.text((cx + 20, y_tbl + 65), lines[1], font=f_td, fill='#0f172a')
    cx += col_w[3]
    
    # 5. Status
    draw.rounded_rectangle([(cx + 20, y_tbl + 40), (cx + 200, y_tbl + 75)], radius=6, fill=row['bg_status'])
    draw.text((cx + 110, y_tbl + 57), row['status'], font=f_td_b, fill=row['c_status'], anchor='mm')
    cx += col_w[4]
    
    y_tbl += row_h

# ----------------- 3. SYSTEM ARCHITECTURE / CAD BACKUP -----------------
# We can include a small architecture snippet or render below the table if needed.
# To keep it ultra-clean, we will leave the focus on the Engineering Matrix.

# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1380), 'Rigorous Engineering Verification: FMEA Risk Analysis | Hardware Watchdog | Autonomous Edge Failsafe | Tested at Rashtriya Raksha University Labs', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1410), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_6_feasibility_risk_master.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 5 (Feasibility & Risk Matrix) generated successfully at:', out_path)
