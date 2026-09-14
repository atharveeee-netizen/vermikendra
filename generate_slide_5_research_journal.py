import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_fig_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'Team Vermikendra & Multi-Disciplinary Engineering Leadership', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Rashtriya Raksha University (RRU), Gujarat  |  Team ID: HSC|GJ|00009  |  Department of ECE & CSE Collaboration', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

def draw_panel(box, title):
    draw.rounded_rectangle(box, radius=12, fill='#ffffff', outline='#94a3b8', width=2)
    h_box = [(box[0][0], box[0][1]), (box[1][0], box[0][1] + 36)]
    draw.rounded_rectangle(h_box, radius=12, fill='#f8fafc', outline='#cbd5e1', width=1)
    draw.text((box[0][0] + 15, box[0][1] + 18), title, font=f_fig_title, fill='#0f172a', anchor='lm')

# ----------------- 2. ROW 1: System Ownership Architecture (y: 105 to 715, h=610) -----------------
b1 = [(60, 105), (W - 60, 715)]
draw_panel(b1, 'Fig. 5A. Multi-Disciplinary Architecture Ownership & Hardware-Software Interfaces')

im_sys = Image.open('scratch/team_system_ownership_diagram.png')
w_sys = 2410
h_sys = int(im_sys.height * (w_sys / im_sys.width))
if h_sys > 550:
    h_sys = 550
    w_sys = int(im_sys.width * (h_sys / im_sys.height))
im_sys_res = im_sys.resize((w_sys, h_sys), Image.Resampling.LANCZOS)
canvas.paste(im_sys_res, (60 + (2440 - w_sys)//2, 150))

# ----------------- 3. ROW 2: Challenges vs Solutions & Roadmap (y: 730 to 1375, h=645) -----------------
# PANEL 2: Challenges Trade-Off Graphs (Left: w=1205)
b2 = [(60, 730), (1265, 1375)]
draw_panel(b2, 'Fig. 5B. Critical Engineering Challenges Solved via Empirical Trade-off Optimization')

im_tr = Image.open('scratch/team_challenges_tradeoff.png')
w_tr = 1170
h_tr = int(im_tr.height * (w_tr / im_tr.width))
if h_tr > 450:
    h_tr = 450
    w_tr = int(im_tr.width * (h_tr / im_tr.height))
im_tr_res = im_tr.resize((w_tr, h_tr), Image.Resampling.LANCZOS)
canvas.paste(im_tr_res, (60 + (1205 - w_tr)//2, 780))

# Captions under trade-offs
cy = 780 + h_tr + 18
draw.text((80, cy), '[1. Power Autonomy]: Aggressive 18 µA sleep duty-cycling guarantees >7 days zero-sunlight endurance.', font=f_sm_b, fill='#047857')
draw.text((80, cy + 24), '[2. Zero Cloud Dependency]: Standalone CM4 WiFi hotspot (192.168.4.1) eliminates rural 4G packet loss.', font=f_sm_b, fill='#0284c7')
draw.text((80, cy + 48), '[3. Respiration Fidelity]: 40mm fan flush pod & linear regression (R² > 0.95) eliminates ambient noise.', font=f_sm_b, fill='#7c3aed')


# PANEL 3: Gantt Roadmap & Milestones (Right: w=1205)
b3 = [(1295, 730), (W - 60, 1375)]
draw_panel(b3, 'Fig. 5C. Multi-Disciplinary Engineering Roadmap & Milestone Execution')

im_gt = Image.open('scratch/team_gantt_roadmap.png')
w_gt = 1170
h_gt = int(im_gt.height * (w_gt / im_gt.width))
if h_gt > 450:
    h_gt = 450
    w_gt = int(im_gt.width * (h_gt / im_gt.height))
im_gt_res = im_gt.resize((w_gt, h_gt), Image.Resampling.LANCZOS)
canvas.paste(im_gt_res, (1295 + (1205 - w_gt)//2, 780))

# Captions under Gantt
gy = 780 + h_gt + 18
draw.text((1315, gy), '[Phase 1-2 Discovery & Co-Design]: Field visits in Gujarat followed by ECE + CSE lab synthesis at RRU.', font=f_sm_b, fill='#0f172a')
draw.text((1315, gy + 24), '[Phase 3 Real-Bin Pilot]: Instrumented live Eisenia fetida bed; validated autonomous misting during 33°C spikes.', font=f_sm_b, fill='#16a34a')
draw.text((1315, gy + 48), '[Phase 4 Scale Vision]: Deploying 20-bin village clusters via KVK extension experts and DAY-NRLM SHGs.', font=f_sm_b, fill='#7c3aed')


# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1395), 'Peer-Reviewed Engineering Team Architecture  |  Rashtriya Raksha University, Gujarat  |  School of Applied Sciences, Technology & National Security', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1420), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_5_team_research_journal.jpg'
canvas.save(out_path, quality=95)
print('Master Academic Research Slide 5 generated successfully at:', out_path)
