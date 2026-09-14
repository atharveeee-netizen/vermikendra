import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_box_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
f_box_body = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Impact Potential & Socio-Economic Value', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Evidence-Based Autonomous Value Chain & Rural Economic Empowerment', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# ----------------- 2. IMPACT PIPELINE (PROBLEM -> BENEFIT) -----------------
def draw_pipeline_box(x, y, w, h, step_name, title, body_lines, color_bg, color_border, color_text):
    draw.rounded_rectangle([(x, y), (x+w, y+h)], radius=12, fill=color_bg, outline=color_border, width=2)
    # Step badge
    draw.rounded_rectangle([(x, y), (x+w, y+35)], radius=12, fill=color_border)
    # Fill bottom corners of badge to make it flat on bottom
    draw.rectangle([(x, y+15), (x+w, y+35)], fill=color_border)
    
    draw.text((x + w/2, y + 17), step_name, font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14), fill='#ffffff', anchor='mm')
    
    draw.text((x + 20, y + 60), title, font=f_box_title, fill=color_text)
    
    cy = y + 100
    for line in body_lines:
        draw.text((x + 20, cy), line, font=f_box_body, fill='#334155')
        cy += 25

stages = [
    ('PROBLEM', 'Hazardous Biomass Burning', ['Open-field crop stubble', 'and dairy dung burning', 'cause severe pollution', 'and soil degradation.'], '#fef2f2', '#dc2626', '#991b1b'),
    ('DETECTION', 'Telemetry & Sensors', ['5-point DS18B20 core', 'temperature array and', 'SCD41 NDIR CO2 sensor', 'continuously sample bin.'], '#fffbeb', '#d97706', '#92400e'),
    ('DECISION', 'Edge AI State Machine', ['Local offline firmware', 'detects lethal core', 'inversion (T > 33°C)', 'predicting collapse.'], '#f8fafc', '#475569', '#334155'),
    ('ACTION', 'Autonomous Mitigation', ['Micro-misting & aeration', 'trigger automatically,', 'stabilizing thermal', 'runaway without human.'], '#f0f9ff', '#0284c7', '#075985'),
    ('BENEFIT', 'Economic & Ecological', ['2.4 Tons Biowaste Diverted', 'Zero Colony Mortality', '₹45,000/yr Net Revenue', 'Premium Compost Yield'], '#f0fdf4', '#16a34a', '#166534')
]

y_pipe = 150
w_box = 420
h_box = 220
gap = (2440 - (5 * w_box)) // 4
start_x = 60

for i, (step, title, lines, bg, bd, fg) in enumerate(stages):
    bx = start_x + i * (w_box + gap)
    draw_pipeline_box(bx, y_pipe, w_box, h_box, step, title, lines, bg, bd, fg)
    
    # Draw arrow to next
    if i < 4:
        arr_x = bx + w_box
        arr_y = y_pipe + h_box//2
        draw.line([(arr_x, arr_y), (arr_x + gap, arr_y)], fill='#94a3b8', width=4)
        # Arrowhead
        draw.polygon([(arr_x + gap - 15, arr_y - 10), (arr_x + gap, arr_y), (arr_x + gap - 15, arr_y + 10)], fill='#94a3b8')

# ----------------- 3. EMPIRICAL EVIDENCE PANELS -----------------
def draw_panel(box, title):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 36)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 15, box[0][1] + 18), title, font=f_fig_title, fill='#0f172a', anchor='lm')

y_evid = 450
h_evid = 850

# LEFT: Biological Evidence
b1 = [(60, y_evid), (1250, y_evid + h_evid)]
draw_panel(b1, 'Fig. 1. Evidence of ACTION: Empirical Earthworm Survival Kinetics & Thermal Protection')

im_wb = Image.open('scratch/plot_worm_survival.png')
w_wb = 1100
h_wb = int(im_wb.height * (w_wb / im_wb.width))
if h_wb > 750:
    h_wb = 750
    w_wb = int(im_wb.width * (h_wb / im_wb.height))
im_wb_res = im_wb.resize((w_wb, h_wb), Image.Resampling.LANCZOS)
canvas.paste(im_wb_res, (60 + (1190 - w_wb)//2, y_evid + 60))

# RIGHT: Economic Evidence
b2 = [(1310, y_evid), (2500, y_evid + h_evid)]
draw_panel(b2, 'Fig. 2. Evidence of BENEFIT: Cumulative Cash Flow & Capital Payback Trajectory')

im_pb = Image.open('scratch/plot_economic_payback.png')
w_pb = 1100
h_pb = int(im_pb.height * (w_pb / im_pb.width))
if h_pb > 750:
    h_pb = 750
    w_pb = int(im_pb.width * (h_pb / im_pb.height))
im_pb_res = im_pb.resize((w_pb, h_pb), Image.Resampling.LANCZOS)
canvas.paste(im_pb_res, (1310 + (1190 - w_pb)//2, y_evid + 60))

# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1380), 'Aligned with National Missions: Swachh Bharat Mission (Grameen) II | GOBARdhan | DAY-NRLM (Lakhpati Didi) | PM-PRANAM | Mission LiFE', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1410), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_4_impact_research_journal.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 4 generated successfully at:', out_path)
