import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set font styling
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.titlesize': 14
})

fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)

# 1. Bar Chart: Key Metrics Normalized to SRAM (Part B = 1.0)
categories = ['Read Latency\n(ns)', 'Write Latency\n(ns)', 'Read Energy\n(nJ)', 'Write Energy\n(nJ)', 'Leakage\n(W)', 'Total Area\n(mm²)']
sram_vals = [2.902, 2.652, 0.793, 0.793, 2.251, 11.474]
stt_t1_vals = [1.589, 10.608, 0.760, 0.531, 0.425, 3.590]
stt_t4b_vals = [1.517, 10.717, 0.646, 0.323, 0.313, 2.209]

x = np.arange(len(categories))
width = 0.25

rects1 = axes[0].bar(x - width, [v/s for v,s in zip(sram_vals, sram_vals)], width, label='6T SRAM (Baseline)', color='#4C72B0', edgecolor='black')
rects2 = axes[0].bar(x, [v/s for v,s in zip(stt_t1_vals, sram_vals)], width, label='STT-MRAM (200µA, 54F²)', color='#C44E52', edgecolor='black')
rects3 = axes[0].bar(x + width, [v/s for v,s in zip(stt_t4b_vals, sram_vals)], width, label='STT-MRAM (100µA, 36F²)', color='#55A868', edgecolor='black')

axes[0].axhline(1.0, color='gray', linestyle='--', linewidth=1)
axes[0].set_ylabel('Normalized to SRAM Baseline')
axes[0].set_title('(a) SRAM vs STT-MRAM Metrics (Relative)', pad=10)
axes[0].set_xticks(x)
axes[0].set_xticklabels(categories)
axes[0].set_yscale('log')
axes[0].set_ylim(0.05, 10.0)
axes[0].grid(axis='y', linestyle=':', alpha=0.6)
axes[0].legend(loc='upper right', framealpha=0.9)

# 2. Area vs Access Transistor Sizing (Task 4 Design Coupling Chain)
configs = ['6T SRAM\n(146 F²)', 'STT Baseline\n(200µA, 6F, 54F²)', 'STT Case A\n(100µA unscaled)', 'STT Case B\n(100µA, 3F, 36F²)']
macro_area = [11.474, 3.590, 3.590, 2.209]
data_area = [10.271, 3.142, 3.142, 1.946]
colors = ['#4C72B0', '#C44E52', '#8172B3', '#55A868']

x_cfg = np.arange(len(configs))
w_cfg = 0.35
axes[1].bar(x_cfg - w_cfg/2, macro_area, w_cfg, label='Total Macro Area', color='#2b5c8f', edgecolor='black')
axes[1].bar(x_cfg + w_cfg/2, data_area, w_cfg, label='Data Array Area', color='#6baed6', edgecolor='black')

for i, (m, d) in enumerate(zip(macro_area, data_area)):
    axes[1].text(i - w_cfg/2, m + 0.25, f"{m:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
    axes[1].text(i + w_cfg/2, d + 0.25, f"{d:.2f}", ha='center', va='bottom', fontsize=9)

axes[1].set_ylabel('Area (mm²)')
axes[1].set_title('(b) Task 4: Area Impact of Write Current Sizing', pad=10)
axes[1].set_xticks(x_cfg)
axes[1].set_xticklabels(configs, rotation=15, ha='right')
axes[1].set_ylim(0, 13.5)
axes[1].grid(axis='y', linestyle=':', alpha=0.6)
axes[1].legend(loc='upper right')

# 3. Task 3: TMR 100% vs 200% Sensing Margin vs Array Metrics
metrics_tmr = ['Read Latency\n(ns)', 'Write Latency\n(ns)', 'Read Energy\n(nJ)', 'Write Energy\n(nJ)', 'Macro Area\n(mm²)', 'ΔV_sense\n(mV)']
t1_tmr = [1.589, 10.608, 0.760, 0.531, 3.590, 60.0]
t3_tmr = [1.594, 10.657, 0.758, 0.529, 3.580, 160.0]

# Normalized to Task 1
x_tmr = np.arange(len(metrics_tmr))
w_tmr = 0.32
norm_t1 = [1.0]*6
norm_t3 = [t3/t1 for t3, t1 in zip(t3_tmr, t1_tmr)]

axes[2].bar(x_tmr - w_tmr/2, norm_t1, w_tmr, label='TMR 100% (3kΩ / 6kΩ)', color='#4C72B0', edgecolor='black')
axes[2].bar(x_tmr + w_tmr/2, norm_t3, w_tmr, label='TMR 200% (4kΩ / 12kΩ)', color='#DD8452', edgecolor='black')

for i, n in enumerate(norm_t3):
    axes[2].text(i + w_tmr/2, n + 0.05, f"{n:.2f}×", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#c44e52' if n > 1.5 else 'black')

axes[2].axhline(1.0, color='gray', linestyle='--', linewidth=1)
axes[2].set_ylabel('Ratio (TMR 200% / TMR 100%)')
axes[2].set_title('(c) Task 3: What TMR 200% Actually Changes', pad=10)
axes[2].set_xticks(x_tmr)
axes[2].set_xticklabels(metrics_tmr, rotation=20, ha='right')
axes[2].set_ylim(0, 3.0)
axes[2].grid(axis='y', linestyle=':', alpha=0.6)
axes[2].legend(loc='upper left')

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
out_svg = os.path.join(out_dir, "part_c_metrics.svg")
out_png = os.path.join(out_dir, "part_c_metrics.png")
plt.savefig(out_svg, format='svg')
plt.savefig(out_png, format='png', dpi=300)
print(f"Saved plots to {out_svg} and {out_png}")
