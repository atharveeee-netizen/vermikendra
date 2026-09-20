import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
f_fig_desc = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'System Architecture & Hardware Instrumentation', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Structural schematic of physical sensing node and end-to-end telemetry pipeline', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

def draw_panel(box, title, desc):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 45)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    
    # Square off bottom of header
    draw.rectangle([(box[0][0], box[0][1] + 25), (box[1][0], box[0][1] + 45)], fill='#f8fafc')
    
    draw.text((box[0][0] + 20, box[0][1] + 22), title, font=f_fig_title, fill='#0f172a', anchor='lm')
    draw.text((box[0][0] + 20, box[1][1] - 35), desc, font=f_fig_desc, fill='#334155', anchor='lm')

# ----------------- 2. LEFT PANEL: HARDWARE CAD -----------------
b1 = [(60, 115), (1240, 1375)]
draw_panel(b1, 'Figure 1(a). Edge Node Physical Instrumentation (Cross-Section)', 'Cross-sectional view detailing 5-point thermal array placement, NDIR gas chamber, and micro-misting actuators.')

im_bin = Image.open('scratch/academic_slide3/fig1_bin_instrumentation_clean.png')

# Maximize within the panel (1180 width, 1180 height max)
w_b = 1140
h_b = int(im_bin.height * (w_b / im_bin.width))
if h_b > 1140:
    h_b = 1140
    w_b = int(im_bin.width * (h_b / im_bin.height))
    
im_bin_res = im_bin.resize((w_b, h_b), Image.Resampling.LANCZOS)
px_b = 60 + (1180 - w_b)//2
py_b = 115 + 45 + (1215 - h_b)//2 - 20
canvas.paste(im_bin_res, (px_b, py_b))


# ----------------- 3. RIGHT PANEL: ARCHITECTURE PIPELINE -----------------
b2 = [(1280, 115), (2500, 1375)]
draw_panel(b2, 'Figure 1(b). End-to-End System Architecture & Telemetry Data Flow', 'Data acquisition, edge-processing state machine, LoRa PHY transmission, and cloud ingestion topology.')

im_diag = Image.open('scratch/academic_slide3/fig2_system_architecture_clean.png')

# Maximize within the panel
w_d = 1180
h_d = int(im_diag.height * (w_d / im_diag.width))
if h_d > 1180:
    h_d = 1180
    w_d = int(im_diag.width * (h_d / im_diag.height))

im_diag_res = im_diag.resize((w_d, h_d), Image.Resampling.LANCZOS)
px_d = 1280 + (1220 - w_d)//2
py_d = 115 + 45 + (1215 - h_d)//2 - 20
canvas.paste(im_diag_res, (px_d, py_d))


# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1395), 'Pure Pictorial Systems Engineering Diagram  |  Rashtriya Raksha University, Gujarat  |  Team ID: HSC|GJ|00009', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1420), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_3_research_journal_master.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 3 (Pure Pictorial Version) generated successfully at:', out_path)
