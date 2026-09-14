import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_kpi_val = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
f_kpi_lbl = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Impact Potential & Socio-Economic Value', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Peer-Reviewed Rural Agritech: Circular Bio-Economy Mass Balance, Worm Survival Kinetics & Multi-Stakeholder Economics', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# ----------------- 2. TOP KPI ROW (y: 105 to 185, h=80) -----------------
kpis = [
    ('0%', 'COLONY COLLAPSE', 'Autonomous misting & 5-point heat alerts eliminate catastrophic mortality (>33°C).', '#dc2626', '#fef2f2', '#fecaca'),
    ('+35%', 'ANNUAL COMPOST YIELD', 'CO2 respiration slope pinpoints readiness, cutting 15-20 days guesswork lag.', '#16a34a', '#f0fdf4', '#bbf7d0'),
    ('₹45,000+', 'NET SHG REVENUE / YR', 'Certified batches (₹12-15/kg vs ₹5/kg) + Vermiwash biopesticide revenue.', '#0284c7', '#f0f9ff', '#bae6fd'),
    ('2.4 Tons', 'BIOWASTE DIVERTED / BIN', 'Crop straw & dairy dung diverted away from hazardous open-field burning.', '#d97706', '#fffbeb', '#fde68a')
]

kw = 585
kgap = 20
ky = 105
for i, (val, title, desc, col_fg, col_bg, col_bd) in enumerate(kpis):
    kx = 60 + i * (kw + kgap)
    draw.rounded_rectangle([(kx, ky), (kx + kw, ky + 80)], radius=10, fill=col_bg, outline=col_bd, width=1)
    draw.rounded_rectangle([(kx, ky), (kx + 8, ky + 80)], radius=4, fill=col_fg)
    
    draw.text((kx + 22, ky + 25), val, font=f_kpi_val, fill=col_fg, anchor='lm')
    draw.text((kx + 22, ky + 58), title, font=f_kpi_lbl, fill='#1e293b', anchor='lm')
    
    words = desc.split()
    l1 = ' '.join(words[:6])
    l2 = ' '.join(words[6:])
    draw.text((kx + 195, ky + 25), l1, font=f_sm, fill='#334155', anchor='lm')
    draw.text((kx + 195, ky + 55), l2, font=f_sm, fill='#475569', anchor='lm')

def draw_panel(box, title):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 36)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 15, box[0][1] + 18), title, font=f_fig_title, fill='#0f172a', anchor='lm')

# ----------------- 3. ROW 1: Circular Economy & Stakeholder Network (y: 195 to 765, h=570) -----------------
# PANEL 1: Circular Bioeconomy (Left: w=1205)
b1 = [(60, 195), (1265, 765)]
draw_panel(b1, 'Fig. 4A. Circular Bio-Economy Mass Balance & Value Realization')

im_flow = Image.open('scratch/circular_bioeconomy_flow.png')
w_f = 1170
h_f = int(im_flow.height * (w_f / im_flow.width))
if h_f > 495:
    h_f = 495
    w_f = int(im_flow.width * (h_f / im_flow.height))
im_flow_res = im_flow.resize((w_f, h_f), Image.Resampling.LANCZOS)
canvas.paste(im_flow_res, (60 + (1205 - w_f)//2, 245))


# PANEL 2: Stakeholder Network (Right: w=1205)
b2 = [(1295, 195), (W - 60, 765)]
draw_panel(b2, 'Fig. 4B. Multi-Stakeholder Closed-Loop Value Realization Matrix')

im_sh = Image.open('scratch/stakeholder_value_network.png')
w_s = 1170
h_s = int(im_sh.height * (w_s / im_sh.width))
if h_s > 495:
    h_s = 495
    w_s = int(im_sh.width * (h_s / im_sh.height))
im_sh_res = im_sh.resize((w_s, h_s), Image.Resampling.LANCZOS)
canvas.paste(im_sh_res, (1295 + (1205 - w_s)//2, 245))


# ----------------- 4. ROW 2: Biological Survival & Economic Payback Curves (y: 775 to 1375, h=600) -----------------
# PANEL 3: Biological Survival Plot (Left: w=1205)
b3 = [(60, 775), (1265, 1375)]
draw_panel(b3, 'Fig. 4C. Empirical Earthworm Survival Kinetics & Thermal Protection')

im_wb = Image.open('scratch/plot_worm_survival.png')
w_wb = 840
h_wb = int(im_wb.height * (w_wb / im_wb.width))
if h_wb > 480:
    h_wb = 480
    w_wb = int(im_wb.width * (h_wb / im_wb.height))
im_wb_res = im_wb.resize((w_wb, h_wb), Image.Resampling.LANCZOS)
canvas.paste(im_wb_res, (60 + (1205 - w_wb)//2, 825))

draw.text((80, 825 + h_wb + 18), 'Key Biological Validation: Autonomous misting triggers at 33°C, keeping bed within optimal 20-28°C range.', font=f_sm_b, fill='#047857')
draw.text((80, 825 + h_wb + 40), 'Without telemetry, unmonitored beds cross 35°C during summer decomposition peaks, leading to 100% mortality.', font=f_sm_b, fill='#dc2626')


# PANEL 4: Economic Payback Plot (Right: w=1205)
b4 = [(1295, 775), (W - 60, 1375)]
draw_panel(b4, 'Fig. 4D. Cumulative Cash Flow & Capital Payback Trajectory')

im_pb = Image.open('scratch/plot_economic_payback.png')
w_pb = 840
h_pb = int(im_pb.height * (w_pb / im_pb.width))
if h_pb > 480:
    h_pb = 480
    w_pb = int(im_pb.width * (h_pb / im_pb.height))
im_pb_res = im_pb.resize((w_pb, h_pb), Image.Resampling.LANCZOS)
canvas.paste(im_pb_res, (1295 + (1205 - w_pb)//2, 825))

draw.text((1315, 825 + h_pb + 18), 'Financial Payback: Initial hardware capital recovered within 2 harvest cycles (~3.8 months) solely via saved seed worms.', font=f_sm_b, fill='#0284c7')
draw.text((1315, 825 + h_pb + 40), 'Annual Net Surplus: Delivers ₹45,000+ per unit through premium batch pricing (₹12-15/kg) and vermiwash sales.', font=f_sm_b, fill='#16a34a')


# ----------------- 5. FOOTER -----------------
draw.text((W/2, 1395), 'Aligned with National Missions: Swachh Bharat Mission (Grameen) II | GOBARdhan | DAY-NRLM (Lakhpati Didi) | PM-PRANAM | Mission LiFE', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1420), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_4_impact_research_journal.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 4 generated successfully at:', out_path)
