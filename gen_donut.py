import matplotlib.pyplot as plt
import numpy as np

# Donut chart for AI Tools Usage
labels = ['Visual Assets (StableDiffusion/Midjourney)', 'Code Assist (GitHub Copilot)', 'Text Refining (ChatGPT)', 'Human Authored (Core Logic)']
sizes = [20, 15, 10, 55]
colors = ['#f59e0b', '#3b82f6', '#10b981', '#64748b']

fig, ax = plt.subplots(figsize=(6, 3.5), dpi=150)
fig.patch.set_facecolor('#ffffff')

# Plot
wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.0f%%', pctdistance=0.75, colors=colors, startangle=140, wedgeprops=dict(width=0.4, edgecolor='w'))

# Enhance text
for t in autotexts:
    t.set_color('white')
    t.set_fontsize(12)
    t.set_fontweight('bold')

ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False, fontsize=10)
plt.title('Extent of AI Tools Usage', fontweight='bold', fontsize=12, pad=10)

plt.tight_layout()
plt.savefig('scratch/academic_slide3/ai_usage_donut.png', bbox_inches='tight', dpi=150)
