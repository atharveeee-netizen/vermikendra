import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 40)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
f_panel_hdr = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_caption_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12.5)
f_caption = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12.5)
f_footer = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
f_footer_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
# Vermikendra Logo Badge
draw.rounded_rectangle([(50, 18), (270, 72)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((160, 45), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

# Center Titles
draw.text((W/2, 34), 'Team Vermikendra & Multi-Disciplinary Engineering Leadership', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 68), 'Rashtriya Raksha University (RRU), Gujarat  |  Team ID: HSC|GJ|00009  |  Hardware-Firmware-Cloud Co-Design & Deployment Roadmap', font=f_sub, fill='#475569', anchor='mm')

# Right Badge
draw.rounded_rectangle([(W - 320, 18), (W - 50, 72)], radius=10, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W - 185, 34), 'YOUTH TECH CHALLENGE', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 11), fill='#ea580c', anchor='mm')
draw.text((W - 185, 54), 'HACKATHON 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 14.5), fill='#0f172a', anchor='mm')

# Separator line
draw.line([(50, 84), (W - 50, 84)], fill='#cbd5e1', width=2)


# ----------------- 2. ROW 1: MASTER FIGURE 1 (y: 92 to 748, h=656) -----------------
# Load research-grade Figure 1
im_f1 = Image.open('scratch/academic_slide5/fig1_team_system_ownership_master.png')
# Target dimensions: w = 2460, h = 656
im_f1_res = im_f1.resize((2460, 656), Image.Resampling.LANCZOS)
canvas.paste(im_f1_res, (50, 92))


# ----------------- 3. ROW 2: PANELS FOR FIGURE 2 & FIGURE 3 (y: 758 to 1380, h=622) -----------------
def draw_panel_box(box, title):
    draw.rounded_rectangle(box, radius=10, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 34)]
    draw.rounded_rectangle(h_box, radius=10, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 16, box[0][1] + 17), title, font=f_panel_hdr, fill='#0f172a', anchor='lm')

# PANEL LEFT: FIGURE 2 (Width: 1215 px)
b2 = [(50, 758), (1275, 1380)]
draw_panel_box(b2, 'Figure 2. Empirical Engineering Trade-Offs & Multi-Objective Pareto Optimization')

# Paste Figure 2 plots
im_f2 = Image.open('scratch/academic_slide5/fig2_engineering_tradeoffs.png')
w_f2 = 1205
h_f2 = int(im_f2.height * (w_f2 / im_f2.width))
if h_f2 > 455:
    h_f2 = 455
    w_f2 = int(im_f2.width * (h_f2 / im_f2.height))
im_f2_res = im_f2.resize((w_f2, h_f2), Image.Resampling.LANCZOS)
f2_x = 50 + (1225 - w_f2) // 2
canvas.paste(im_f2_res, (f2_x, 802))

# Fig 2 Explanatory Scientific Captions
c2_y = 802 + h_f2 + 12
draw.text((68, c2_y), '[2A. Power Autonomy Pareto Frontier]:', font=f_caption_b, fill='#0284c7')
draw.text((345, c2_y), '18 uA deep sleep duty-cycling achieves 583.2 days autonomy; provides >7d zero-sunlight monsoon reserve.', font=f_caption, fill='#334155')

draw.text((68, c2_y + 24), '[2B. Rural Canopy LoRa Link Margin]:', font=f_caption_b, fill='#15803d')
draw.text((345, c2_y + 24), 'Spreading Factor SF9 sustains >= 95% Packet Delivery Rate up to 2.2 km through dense sugarcane/wheat biomass.', font=f_caption, fill='#334155')

draw.text((68, c2_y + 48), '[2C. Respiration Purge Signal-to-Noise]:', font=f_caption_b, fill='#1e40af')
draw.text((345, c2_y + 48), '40mm active fan flush purges ambient drift; subsequent linear CO2 accumulation yields R2 = 0.982 respiration fidelity.', font=f_caption, fill='#334155')


# PANEL RIGHT: FIGURE 3 (Width: 1225 px)
b3 = [(1285, 758), (W - 50, 1380)]
draw_panel_box(b3, 'Figure 3. Multi-Disciplinary Systems Engineering Roadmap, TRL Progression & Milestones')

# Paste Figure 3 Gantt
im_f3 = Image.open('scratch/academic_slide5/fig3_engineering_roadmap_gantt.png')
w_f3 = 1205
h_f3 = int(im_f3.height * (w_f3 / im_f3.width))
if h_f3 > 455:
    h_f3 = 455
    w_f3 = int(im_f3.width * (h_f3 / im_f3.height))
im_f3_res = im_f3.resize((w_f3, h_f3), Image.Resampling.LANCZOS)
f3_x = 1285 + (1225 - w_f3) // 2
canvas.paste(im_f3_res, (f3_x, 802))

# Fig 3 Explanatory Scientific Captions
c3_y = 802 + h_f3 + 12
draw.text((1303, c3_y), '[Phase 1-2 Co-Design & Lab Synthesis]:', font=f_caption_b, fill='#ea580c')
draw.text((1585, c3_y), '12 Gujarat agro-surveys -> ECE hardware prototyping (18 uA sleep) -> CSE gateway daemons (<45ms).', font=f_caption, fill='#334155')

draw.text((1303, c3_y + 24), '[Phase 3 Live Pilot & Bio-Stress Test]:', font=f_caption_b, fill='#15803d')
draw.text((1585, c3_y + 24), 'Instrumented live Eisenia fetida bed; validated autonomous misting failsafe at 33 C core thermal spike.', font=f_caption, fill='#334155')

draw.text((1303, c3_y + 48), '[Phase 4-5 National Scaling Vision]:', font=f_caption_b, fill='#7c3aed')
draw.text((1585, c3_y + 48), 'Live hardware demonstration at HSC Finals -> 20-bin village cluster rollout with KVK & DAY-NRLM SHGs.', font=f_caption, fill='#334155')


# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1398), 'Peer-Reviewed Systems Engineering Leadership  |  Rashtriya Raksha University, Gujarat  |  School of Applied Sciences, Technology & National Security', font=f_footer_b, fill='#475569', anchor='mm')
draw.text((W/2, 1422), '@HSC submission- Template  |  Team ID: HSC|GJ|00009', font=f_footer, fill='#94a3b8', anchor='mm')

out_path = 'slide_5_team_research_journal.jpg'
canvas.save(out_path, quality=98)
print('Master Slide 5 generated successfully at:', out_path)
