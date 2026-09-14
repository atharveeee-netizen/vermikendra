import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('scratch/academic_slide5', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.2

fig, ax = plt.subplots(figsize=(16.8, 5.2), dpi=220)
plt.subplots_adjust(left=0.17, right=0.98, top=0.88, bottom=0.10)

# Timeline phases (x-axis: 0 to 100)
phases = [
    ('Phase 1: Field Recon & Agro Baseline\n(Aug 2026)', 0, 18, '#f1f5f9'),
    ('Phase 2: Lab Co-Design at RRU\n(Sep 2026 W1-W2)', 18, 42, '#f8fafc'),
    ('Phase 3: Live Pilot & Stress Test\n(Sep 2026 W3-W4)', 42, 68, '#f1f5f9'),
    ('Phase 4: HSC Finals Demo\n(Oct 2026)', 68, 84, '#f8fafc'),
    ('Phase 5: National Scale\n(2027 Horizon)', 84, 100, '#f1f5f9')
]

for name, x0, x1, bg in phases:
    ax.axvspan(x0, x1, color=bg, alpha=0.6, zorder=0)
    ax.axvline(x1, color='#cbd5e1', linestyle='--', linewidth=1.0, zorder=1)
    ax.text((x0 + x1)/2, 8.65, name, ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#1e293b')

tasks = [
    # ECE Track (Atharve)
    {'y': 7.6, 'x0': 18, 'w': 19, 'color': '#ea580c', 'label': 'TPS62740 Buck & 5-Probe Depth Array'},
    {'y': 6.8, 'x0': 27, 'w': 21, 'color': '#c2410c', 'label': 'Firmware State Machine & 18 uA Sleep'},
    
    # CSE Systems Track (Akshit)
    {'y': 5.6, 'x0': 19, 'w': 21, 'color': '#0284c7', 'label': 'CM4 Daemon & 44B Binary HMAC Parser'},
    {'y': 4.8, 'x0': 32, 'w': 22, 'color': '#0369a1', 'label': 'Mosquitto MQTT & SQLite3 WAL Engine'},
    
    # CSE UX Track (Charvi)
    {'y': 3.6, 'x0': 20, 'w': 22, 'color': '#7c3aed', 'label': 'React 18 PWA Shell & Gujarati i18n'},
    {'y': 2.8, 'x0': 34, 'w': 23, 'color': '#6d28d9', 'label': 'Low-Literacy Dials & FCO QR Ledger'},
    
    # Joint Track (All)
    {'y': 1.6, 'x0': 2, 'w': 15, 'color': '#16a34a', 'label': 'Gujarat Field Survey (12 Sites)'},
    {'y': 1.6, 'x0': 44, 'w': 20, 'color': '#15803d', 'label': 'Live Eisenia fetida Pilot @ 33°C'},
    {'y': 0.8, 'x0': 68, 'w': 14, 'color': '#047857', 'label': 'HSC Live Hardware Demo'},
    {'y': 0.8, 'x0': 84, 'w': 14, 'color': '#065f46', 'label': '20-Bin Rural KVK Cluster'}
]

for t in tasks:
    rect = patches.FancyBboxPatch((t['x0'], t['y'] - 0.28), t['w'], 0.56,
                                  boxstyle="round,pad=0.2,rounding_size=0.4",
                                  facecolor=t['color'], edgecolor='none', zorder=3)
    ax.add_patch(rect)
    ax.text(t['x0'] + 0.8, t['y'], t['label'], va='center', ha='left',
            fontsize=8.5, fontweight='bold', color='#ffffff', zorder=4)

# Milestones (Diamonds with verified benchmark tags)
milestones = [
    (38.5, 7.6, 'M1: 18 uA Sleep Verified', '#ea580c', 1.0, 0.35),
    (49.5, 6.8, 'M2: LoRa PDR 98.4% @ 1.5km', '#c2410c', 1.0, 0.35),
    (55.5, 4.8, 'M3: SQLite Ingest <45ms', '#0284c7', 1.0, 0.35),
    (58.5, 2.8, 'M4: PWA Cold Launch <250ms', '#7c3aed', 1.0, 0.35),
    (65.5, 1.6, 'M5: 33°C Misting Validated', '#15803d', 1.0, 0.35),
    (98.5, 0.8, 'M6: National Scale (20 Bins)', '#065f46', -17.5, 0.35)
]

for mx, my, mtext, mcolor, ox, oy in milestones:
    ax.plot(mx, my, marker='D', markersize=8.5, color='#ffffff', markeredgecolor=mcolor, markeredgewidth=2.2, zorder=5)
    ax.annotate(mtext, xy=(mx, my), xytext=(mx + ox, my + oy),
                fontsize=8.2, fontweight='bold', color=mcolor, zorder=6,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor=mcolor, alpha=0.95, lw=1.2))

# Y-Axis formatting with Teammate Swimlane Labels
ax.set_yticks([7.2, 5.2, 3.2, 1.2])
ax.set_yticklabels([
    'Atharve Dahima (ECE)\n[Embedded & Power]',
    'Akshit Agarwal (CSE)\n[Gateway & ML Engine]',
    'Charvi Meddita (CSE)\n[PWA & Grassroots UX]',
    'Multi-Disciplinary Integration\n[All Teammates]'
], fontsize=9.8, fontweight='bold', color='#0f172a')

for y_div in [6.2, 4.2, 2.2]:
    ax.axhline(y_div, color='#cbd5e1', linestyle='-', linewidth=1.2, zorder=2)

ax.set_xlim(0, 100)
ax.set_ylim(0.2, 9.8)
ax.set_xticks([])

for spine in ax.spines.values():
    spine.set_edgecolor('#94a3b8')
    spine.set_linewidth(1.4)

out_path = 'scratch/academic_slide5/fig3_engineering_roadmap_gantt.png'
plt.savefig(out_path, bbox_inches='tight', pad_inches=0.08)
plt.close()
print('Generated publication-grade Figure 3 Gantt at:', out_path)
