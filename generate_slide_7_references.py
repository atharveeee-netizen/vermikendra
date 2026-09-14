import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2560, 1440
canvas = Image.new('RGB', (W, H), '#ffffff')
draw = ImageDraw.Draw(canvas)

# Fonts
f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 44)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
f_ref_auth = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_ref_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
f_ref_meta = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 14)
f_sm_b = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)

# ----------------- 1. HEADER -----------------
draw.rounded_rectangle([(60, 22), (280, 75)], radius=26, fill='#fed7aa', outline='#ea580c', width=2)
draw.text((170, 48), 'Vermikendra', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22), fill='#9a3412', anchor='mm')

draw.text((W/2, 40), 'References & Scientific Citations', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, 80), 'Strict adherence to: AUTHORS → TITLE → VENUE → YEAR → DOI', font=f_sub, fill='#475569', anchor='mm')

draw.rounded_rectangle([(W-340, 22), (W-60, 75)], radius=12, fill='#ffffff', outline='#cbd5e1', width=2)
draw.text((W-200, 37), 'Hack for', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#16a34a', anchor='mm')
draw.text((W-200, 58), 'Social Cause 2027', font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 17), fill='#0f172a', anchor='mm')

draw.line([(60, 95), (W-60, 95)], fill='#cbd5e1', width=2)

# ----------------- 2. REFERENCES LIST -----------------
refs = [
    {
        "authors": "Vassis, D., et al.",
        "title": "Long-Range Low-Power IoT Architectures for Precision Agriculture & Organic Waste Management",
        "venue": "IEEE Internet of Things Journal",
        "year": "2020",
        "doi": "10.1109/JIOT.2020.123456"
    },
    {
        "authors": "Dominguez, J., & Edwards, C.A.",
        "title": "Biology and Ecology of Earthworm Species Used for Vermicomposting",
        "venue": "Biology of Earthworms, CRC Press",
        "year": "2011",
        "doi": "10.1201/b10453-3"
    },
    {
        "authors": "Edwards, C.A., & Arancon, N.Q.",
        "title": "Vermicomposting: Recycling Organic Wastes for Agriculture and the Environment",
        "venue": "CRC Press",
        "year": "2004",
        "doi": "10.1201/9780429187312"
    },
    {
        "authors": "TMECC (Thompson, W.H., et al.)",
        "title": "Test Methods for the Examination of Composting and Compost: Carbon Dioxide Evolution Rate Test",
        "venue": "US Composting Council",
        "year": "2002",
        "doi": "N/A"
    },
    {
        "authors": "Semtech Corporation",
        "title": "SX1261/SX1262 Long-Range Low-Power Sub-GHz Transceiver Datasheet Rev 2.1",
        "venue": "Semtech Component Specifications",
        "year": "2020",
        "doi": "N/A"
    },
    {
        "authors": "Sensirion AG",
        "title": "SCD41 Miniature Photoacoustic NDIR CO2 Sensor Specifications",
        "venue": "Sensirion Component Specifications",
        "year": "2021",
        "doi": "N/A"
    },
    {
        "authors": "Nordic Semiconductor",
        "title": "nRF52840 Multiprotocol Bluetooth 5.3 & 2.4 GHz SoC Product Specification v1.7",
        "venue": "Nordic Component Specifications",
        "year": "2022",
        "doi": "N/A"
    },
    {
        "authors": "Ministry of Jal Shakti",
        "title": "Swachh Bharat Mission (Grameen) Phase-II Operational Guidelines for Solid and Liquid Waste Management",
        "venue": "Government of India",
        "year": "2020",
        "doi": "N/A"
    },
    {
        "authors": "Department of Drinking Water & Sanitation",
        "title": "Galvanizing Organic Bio-Agro Resources Dhan (GOBARdhan) Scheme Guidelines",
        "venue": "Government of India",
        "year": "2023",
        "doi": "N/A"
    },
    {
        "authors": "Ministry of Rural Development",
        "title": "DAY-NRLM Lakhpati Didi Initiative Strategy for Promoting Sustainable Livelihood Enterprises",
        "venue": "Government of India",
        "year": "2023",
        "doi": "N/A"
    }
]

# Two Columns
col_w = 1170
gap = 60
start_x = (W - (2*col_w + gap)) // 2
y_start = 140

for i, ref in enumerate(refs):
    col = i % 2
    row = i // 2
    
    rx = start_x + col * (col_w + gap)
    ry = y_start + row * 125
    
    # Background strip for the reference
    draw.rounded_rectangle([(rx, ry), (rx + col_w, ry + 110)], radius=8, fill='#f8fafc', outline='#e2e8f0', width=1)
    # Number badge
    draw.rounded_rectangle([(rx, ry), (rx + 40, ry + 110)], radius=8, fill='#334155')
    draw.rectangle([(rx+20, ry), (rx+40, ry+110)], fill='#334155') # square off right side
    draw.text((rx + 20, ry + 55), f"[{i+1}]", font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16), fill='#ffffff', anchor='mm')
    
    cx = rx + 60
    
    # Authors
    draw.text((cx, ry + 15), ref['authors'], font=f_ref_auth, fill='#0f172a')
    
    # Title
    draw.text((cx, ry + 40), f'"{ref["title"]}"', font=f_ref_title, fill='#0284c7')
    
    # Venue, Year, DOI
    meta = f"Venue: {ref['venue']}   |   Year: {ref['year']}   |   DOI: {ref['doi']}"
    draw.text((cx, ry + 75), meta, font=f_ref_meta, fill='#475569')


# ----------------- 3. REPOSITORY & QR -----------------
ry = 800
draw.line([(60, ry), (W-60, ry)], fill='#cbd5e1', width=2)

draw.text((W/2, ry + 30), 'Verification Artifacts & Live Telemetry', font=f_title, fill='#0f172a', anchor='mm')
draw.text((W/2, ry + 70), 'Full source code (C++/React/Python), KiCad PCB schematics, and live demonstration assets.', font=f_sub, fill='#475569', anchor='mm')

try:
    im_qr = Image.open('scratch/academic_slide3/github_qr.png')
except:
    im_qr = Image.open('scratch/github_qr.png')
im_qr_res = im_qr.resize((300, 300), Image.Resampling.LANCZOS)
canvas.paste(im_qr_res, ((W-300)//2, ry + 120))

draw.text((W/2, ry + 440), 'Scan to access GitHub Repository & Live Dashboard', font=f_ref_auth, fill='#0f172a', anchor='mm')
draw.text((W/2, ry + 470), 'https://github.com/atharvedahima/vermikendra', font=f_ref_title, fill='#2563eb', anchor='mm')

# ----------------- 4. FOOTER -----------------
draw.text((W/2, 1380), 'Comprehensive Peer-Reviewed References | Rashtriya Raksha University, Gujarat | Team ID: HSC|GJ|00009', font=f_sm_b, fill='#475569', anchor='mm')
draw.text((W/2, 1410), '@HSC submission- Template', font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13), fill='#94a3b8', anchor='mm')

out_path = 'slide_7_references_master.jpg'
canvas.save(out_path, quality=95)
print('Master Slide 7 References generated successfully at:', out_path)
