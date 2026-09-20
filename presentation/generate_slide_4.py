import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#f8fafc')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 46)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 21)
f_head = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24)
f_subhead = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 19)
f_kpi_val = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 42)
f_kpi_lbl = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_body = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
f_body_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
f_sm = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# 1. HEADER
draw.rounded_rectangle([(60, 25), (280, 80)], radius=27, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 52), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 24), fill='#9a3412', anchor='mm')

draw.text((W/2, 45), 'Impact Potential & Socio-Economic Value', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 88), 'Empowering SHG Livelihoods, Transforming Rural Waste into Wealth & Validating Organic Agriculture', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 25), (W-60, 80)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 41), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#16a34a', anchor='mm')
draw.text((W-200, 63), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#0f172a', anchor='mm')

draw.line([(60, 105), (W-60, 105)], fill='#e2e8f0', width=2)

# 2. TOP METRIC KPI CARDS (y: 118 to 235)
kpi_data = [
    ('0%', 'COLONY COLLAPSE', 'Autonomous misting & 5-point heat alerts eliminate catastrophic worm mortality (>35C).', '#dc2626', '#fef2f2', '#fecaca'),
    ('+35%', 'ANNUAL COMPOST YIELD', 'CO2 respiration slope pinpoints readiness, cutting 15-20 days of guesswork dormancy.', '#16a34a', '#f0fdf4', '#bbf7d0'),
    ('Rs.45,000+', 'ANNUAL NET SHG INCOME', 'Premium certified batches (Rs.12-15/kg vs Rs.5/kg) + Vermiwash biopesticide sales.', '#0284c7', '#f0f9ff', '#bae6fd'),
    ('2.4 Tons', 'BIOWASTE DIVERTED / BIN', 'Diverts crop straw, dairy cow dung & agro-waste from polluting open field burning.', '#d97706', '#fffbeb', '#fde68a')
]

kpi_w = 585
kpi_gap = 20
kpi_start_x = 60
kpi_y = 118
kpi_h = 112

for i, (val, title, desc, col_fg, col_bg, col_border) in enumerate(kpi_data):
    bx = kpi_start_x + i * (kpi_w + kpi_gap)
    draw.rounded_rectangle([(bx, kpi_y), (bx + kpi_w, kpi_y + kpi_h)], radius=12, fill=col_bg, outline=col_border, width=2)
    draw.rounded_rectangle([(bx, kpi_y), (bx + 12, kpi_y + kpi_h)], radius=6, fill=col_fg)
    
    draw.text((bx + 28, kpi_y + 38), val, font=f_kpi_val, fill=col_fg, anchor='lm')
    draw.text((bx + 28, kpi_y + 82), title, font=f_kpi_lbl, fill='#1e293b', anchor='lm')
    
    words = desc.split()
    l1 = ' '.join(words[:6])
    l2 = ' '.join(words[6:12])
    l3 = ' '.join(words[12:])
    draw.text((bx + 230, kpi_y + 30), l1, font=f_sm, fill='#334155')
    draw.text((bx + 230, kpi_y + 53), l2, font=f_sm, fill='#334155')
    draw.text((bx + 230, kpi_y + 76), l3, font=f_sm, fill='#475569')

# 3. MIDDLE SECTION: 3 IMPACT PILLARS (y: 245 to 780)
pillar_w = 786
pillar_gap = 21
pillar_y = 245
pillar_h = 530

pillars = [
    {
        'title': 'A. Social & Livelihood Impact',
        'subtitle': 'DAY-NRLM & Lakhpati Didi Empowerment',
        'color': '#7c3aed',
        'bg': '#f5f3ff',
        'border': '#ddd6fe',
        'icon_text': 'SHG',
        'items': [
            ('Women Micro-Enterprises:', 'Transforms marginal farmers and SHG women into commercial organic input producers with dependable monthly revenues.'),
            ('Drudgery Elimination:', 'Eliminates unhygienic, manual daily bed turning and messy deep probing in decomposing cow dung.'),
            ('Universal Accessibility:', 'Low-literacy friendly UI with intuitive color states (Green/Amber/Red), simple icons, and Gujarati/Hindi voice-assist.'),
            ('Community Resilience:', 'Builds decentralized village bio-resource hubs, ending dependence on external industrial chemical supply chains.')
        ]
    },
    {
        'title': 'B. Economic & Market Viability',
        'subtitle': 'Cluster ROI & Batch Certification',
        'color': '#0284c7',
        'bg': '#f0f9ff',
        'border': '#bae6fd',
        'icon_text': 'ROI',
        'items': [
            ('1 Gateway : 20 Bins Topology:', 'One solar LoRa gateway covers an entire village cluster within a 2 km radius, slashing per-bin telemetry cost.'),
            ('2.5x Price Realization:', 'QR-traceable batches certified via respiration stability command Rs.12-15/kg vs Rs.5-6/kg unverified market rate.'),
            ('Vermiwash Revenue Stream:', 'Real-time moisture balance maintains optimal drainage, yielding 15-20L high-value liquid foliar biopesticide per month.'),
            ('Rapid Capital Payback:', 'Capital hardware investment recovered within 2 harvest cycles (~4 months) solely from worm mortality prevention.')
        ]
    },
    {
        'title': 'C. Environmental & Soil Circularity',
        'subtitle': 'GOBARdhan, PM-PRANAM & Mission LiFE',
        'color': '#059669',
        'bg': '#f0fdf4',
        'border': '#a7f3d0',
        'icon_text': 'ECO',
        'items': [
            ('Stubble & Dung Waste Diversion:', 'Converts agro-residue, paddy straw, and cow dung into high-humus manure, reducing hazardous open-field burning.'),
            ('Chemical Fertilizer Displacement:', 'Replaces synthetic urea/DAP with living microbial compost, neutralizing soil acidity and preventing nitrate runoff.'),
            ('Soil Organic Carbon (SOC) Rebuilding:', 'Increases soil moisture retention by 20-30%, dramatically lowering irrigation water demand in drought-prone regions.'),
            ('Quantified Carbon Accounting:', 'Provides tamper-proof weighed digital ledger of biomass converted, creating potential for future voluntary carbon credits.')
        ]
    }
]

for i, p in enumerate(pillars):
    px = 60 + i * (pillar_w + pillar_gap)
    draw.rounded_rectangle([(px, pillar_y), (px + pillar_w, pillar_y + pillar_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)
    draw.rounded_rectangle([(px, pillar_y), (px + pillar_w, pillar_y + 70)], radius=16, fill=p['bg'], outline=p['border'], width=1)
    
    draw.rounded_rectangle([(px + 15, pillar_y + 10), (px + 75, pillar_y + 60)], radius=10, fill=p['color'])
    draw.text((px + 45, pillar_y + 35), p['icon_text'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18), fill='#ffffff', anchor='mm')
    
    draw.text((px + 90, pillar_y + 24), p['title'], font=f_head, fill='#0f172a')
    draw.text((px + 90, pillar_y + 50), p['subtitle'], font=f_sm_b, fill=p['color'])
    
    iy = pillar_y + 88
    for title, desc in p['items']:
        draw.ellipse([(px + 20, iy + 6), (px + 28, iy + 14)], fill=p['color'])
        draw.text((px + 38, iy), title, font=f_subhead, fill='#0f172a')
        iy += 25
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
        iy += 12

# 4. LOWER SECTION: 4-TIER STAKEHOLDER MATRIX (y: 790 to 1340)
sh_y = 790
sh_h = 540
draw.rounded_rectangle([(60, sh_y), (W - 60, sh_y + sh_h)], radius=16, fill='#ffffff', outline='#cbd5e1', width=2)

draw.rounded_rectangle([(60, sh_y), (W - 60, sh_y + 50)], radius=16, fill='#f8fafc', outline='#cbd5e1', width=1)
draw.text((W/2, sh_y + 25), 'Complete Multi-Stakeholder Ecosystem Value Matrix', font=f_head, fill='#0f172a', anchor='mm')

stakeholders = [
    {
        'role': '1. Village SHG Operator',
        'who': 'Rural women & smallholder farmers managing 2-10 vermi-beds',
        'pain': 'Silent colony heat death (>35C), crop residue rotting, zero records',
        'value': '100% offline alerts in Gujarati/Hindi; autonomous misting protects worms; automatic weight logging without paperwork',
        'kpi': 'Zero worm losses | 100% hands-free records',
        'color': '#ea580c',
        'bg': '#fff7ed',
        'border': '#ffedd5'
    },
    {
        'role': '2. Cluster Supervisor',
        'who': 'Panchayat secretaries, Block SRLM / Swachh Bharat coordinators',
        'pain': 'Fraudulent manual registers; impossible physical verification across remote sites',
        'value': 'Tamper-proof digital ledger; verified kilograms of waste digested; instant exportable government audit compliance reports',
        'kpi': '100% verifiable data | 1 Gateway for 20 units',
        'color': '#2563eb',
        'bg': '#eff6ff',
        'border': '#dbeafe'
    },
    {
        'role': '3. Bulk Commercial Buyer',
        'who': 'Organic farmers, FPOs, commercial nurseries & tea plantations',
        'pain': 'Inconsistent, foul, immature compost causing plant root burn and weed seeds',
        'value': 'QR-code batch traceability; verified CO2 respiration maturity plateau; guaranteed pathogen-free biological stability',
        'kpi': 'Lab-grade consistency | Verified premium NPK',
        'color': '#059669',
        'bg': '#f0fdf4',
        'border': '#dcfce7'
    },
    {
        'role': '4. KVK / Research Expert',
        'who': 'Krishi Vigyan Kendras, ICAR scientists & Agri University extension',
        'pain': 'Lack of real-time multi-depth telemetry on tropical earthworm kinetics',
        'value': 'High-resolution empirical 5-point thermal & gas dataset to tune regional bio-waste composting SOPs and advisory',
        'kpi': 'Open research telemetry | Climate-adaptive models',
        'color': '#7c3aed',
        'bg': '#faf5ff',
        'border': '#f3e8ff'
    }
]

card_w = 585
card_gap = 20
s_card_y = sh_y + 65
s_card_h = 455

for i, s in enumerate(stakeholders):
    cx = 60 + 15 + i * (card_w + card_gap)
    draw.rounded_rectangle([(cx, s_card_y), (cx + card_w, s_card_y + s_card_h)], radius=12, fill=s['bg'], outline=s['border'], width=2)
    draw.rounded_rectangle([(cx, s_card_y), (cx + card_w, s_card_y + 42)], radius=12, fill=s['color'])
    draw.text((cx + card_w/2, s_card_y + 21), s['role'], font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#ffffff', anchor='mm')
    
    cy = s_card_y + 52
    draw.text((cx + 15, cy), 'Target Persona:', font=f_sm_b, fill=s['color'])
    cy += 18
    draw.text((cx + 15, cy), s['who'], font=f_sm, fill='#334155')
    cy += 30
    
    draw.text((cx + 15, cy), 'Critical Pain Today:', font=f_sm_b, fill='#dc2626')
    cy += 18
    draw.text((cx + 15, cy), s['pain'], font=f_sm, fill='#475569')
    cy += 38
    
    draw.text((cx + 15, cy), 'Vermikendra Deliverable:', font=f_sm_b, fill='#16a34a')
    cy += 18
    words = s['value'].split()
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        if len(' '.join(cur)) > 46:
            cur.pop()
            lines.append(' '.join(cur))
            cur = [w]
    if cur:
        lines.append(' '.join(cur))
    for l in lines:
        draw.text((cx + 15, cy), l, font=f_sm, fill='#334155')
        cy += 20
        
    draw.rounded_rectangle([(cx + 15, s_card_y + s_card_h - 45), (cx + card_w - 15, s_card_y + s_card_h - 12)], radius=8, fill='#ffffff', outline=s['color'], width=1)
    draw.text((cx + card_w/2, s_card_y + s_card_h - 28), s['kpi'], font=f_sm_b, fill=s['color'], anchor='mm')

# 5. BOTTOM WATERMARK & GOVERNMENT SCHEMES
draw.text((W/2, 1360), 'Aligned with National Missions: Swachh Bharat Mission (Grameen) II | GOBARdhan | DAY-NRLM (Lakhpati Didi) | PM-PRANAM | Mission LiFE', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1395), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14), fill='#94a3b8', anchor='mm')

out_path = 'slide_4_impact_potential_master.jpg'
canvas.save(out_path, quality=95)
print('Master Slide 4 generated successfully at:', out_path)
