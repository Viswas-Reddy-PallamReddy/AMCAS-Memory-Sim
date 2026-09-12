# Generate SVG plot for Part B Task 2: Access Time vs log2(Capacity)
import math

data = [
    ("256 kB", 8, 2.4171),
    ("512 kB", 9, 2.4845),
    ("1 MB", 10, 2.6338),
    ("2 MB", 11, 2.9018),
    ("4 MB", 12, 3.5308),
    ("8 MB", 13, 4.4727),
    ("16 MB", 14, 6.3624),
]

w, h = 800, 520
pad_l, pad_r, pad_t, pad_b = 80, 50, 55, 65
plot_w = w - pad_l - pad_r
plot_h = h - pad_t - pad_b

x_min, x_max = 7.5, 14.5
y_min, y_max = 2.0, 7.0

def x_map(x):
    return pad_l + (x - x_min) / (x_max - x_min) * plot_w

def y_map(y):
    return pad_t + (1.0 - (y - y_min) / (y_max - y_min)) * plot_h

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#ffffff; font-family:system-ui,-apple-system,sans-serif;">']

# Title
svg.append(f'<text x="{w/2}" y="26" text-anchor="middle" font-size="16" font-weight="bold" fill="#111827">CACTI 7: L2 Cache Access Time vs. log₂(Capacity)</text>')
svg.append(f'<text x="{w/2}" y="44" text-anchor="middle" font-size="12" fill="#4b5563">Testing Amrutur &amp; Horowitz\'s "One Gate Delay per Doubling" Scaling Hypothesis (45 nm Bulk CMOS)</text>')

# Grid and X ticks
for label, log2_val, t_acc in data:
    x = x_map(log2_val)
    svg.append(f'<line x1="{x}" y1="{pad_t}" x2="{x}" y2="{pad_t+plot_h}" stroke="#e5e7eb" stroke-width="1"/>')
    svg.append(f'<text x="{x}" y="{pad_t+plot_h+20}" text-anchor="middle" font-size="11" fill="#374151">{log2_val} ({label})</text>')

# Y ticks
for y_val in [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
    y = y_map(y_val)
    svg.append(f'<line x1="{pad_l}" y1="{y}" x2="{pad_l+plot_w}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>')
    svg.append(f'<text x="{pad_l-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#6b7280">{y_val:.1f} ns</text>')

# Axis labels
svg.append(f'<text x="{pad_l+plot_w/2}" y="{h-18}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151">log₂(Capacity in kB)</text>')
svg.append(f'<text x="25" y="{pad_t+plot_h/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151" transform="rotate(-90 25 {pad_t+plot_h/2})">Access Time (ns)</text>')

# Ideal "One Gate Delay per Doubling" line (slope = ~20 ps to 67 ps per doubling from 256 kB baseline)
# Let's project a linear line with slope = 0.0674 ns/doubling (the 256k->512k slope)
ideal_pts = []
for log2_val in [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]:
    t_ideal = 2.4171 + (log2_val - 8.0) * 0.0674
    ideal_pts.append(f"{x_map(log2_val):.1f},{y_map(t_ideal):.1f}")
svg.append(f'<path d="M ' + ' L '.join(ideal_pts) + '" fill="none" stroke="#9ca3af" stroke-width="2" stroke-dasharray="6,4"/>')

# Actual CACTI Access Time curve
cacti_pts = [f"{x_map(log2_val):.1f},{y_map(t_acc):.1f}" for _, log2_val, t_acc in data]
svg.append(f'<path d="M ' + ' L '.join(cacti_pts) + '" fill="none" stroke="#2563eb" stroke-width="3"/>')

for label, log2_val, t_acc in data:
    x = x_map(log2_val)
    y = y_map(t_acc)
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#2563eb"/>')
    svg.append(f'<text x="{x:.1f}" y="{y-10:.1f}" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">{t_acc:.2f} ns</text>')

# Annotation of the two regimes
# Regime 1: Logic-dominated (small)
x_r1 = (x_map(8) + x_map(9)) / 2
svg.append(f'<rect x="{pad_l+10}" y="{pad_t+plot_h-95}" width="260" height="75" fill="#f0fdf4" stroke="#86efac" rx="4" opacity="0.95"/>')
svg.append(f'<text x="{pad_l+20}" y="{pad_t+plot_h-75}" font-size="11" font-weight="bold" fill="#15803d">Regime 1: Logic-Dominated (256k–512k)</text>')
svg.append(f'<text x="{pad_l+20}" y="{pad_t+plot_h-58}" font-size="10" fill="#166534">Δt ≈ +67 ps/doubling (~2–3 FO4 gates)</text>')
svg.append(f'<text x="{pad_l+20}" y="{pad_t+plot_h-43}" font-size="10" fill="#166534">Amrutur &amp; Horowitz scaling visible here!</text>')

# Regime 2: Wire-dominated (large)
svg.append(f'<rect x="{x_map(11)-40}" y="{pad_t+40}" width="290" height="85" fill="#fef2f2" stroke="#fca5a5" rx="4" opacity="0.95"/>')
svg.append(f'<text x="{x_map(11)-30}" y="{pad_t+60}" font-size="11" font-weight="bold" fill="#b91c1c">Regime 2: Interconnect-Dominated (1M–16M)</text>')
svg.append(f'<text x="{x_map(11)-30}" y="{pad_t+77}" font-size="10" fill="#991b1b">Global H-tree wire delay explodes (L ∝ √Area)</text>')
svg.append(f'<text x="{x_map(11)-30}" y="{pad_t+92}" font-size="10" fill="#991b1b">Δt rises from +149 ps up to +1890 ps/doubling!</text>')
svg.append(f'<text x="{x_map(11)-30}" y="{pad_t+107}" font-size="10" fill="#991b1b">Shatters pure linear gate-delay model.</text>')

# Legend
leg_x, leg_y = pad_l + 25, pad_t + 20
svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="310" height="65" fill="#ffffff" stroke="#d1d5db" rx="4" opacity="0.95"/>')
svg.append(f'<line x1="{leg_x+10}" y1="{leg_y+20}" x2="{leg_x+40}" y2="{leg_y+20}" stroke="#2563eb" stroke-width="3"/>')
svg.append(f'<circle cx="{leg_x+25}" cy="{leg_y+20}" r="4" fill="#2563eb"/>')
svg.append(f'<text x="{leg_x+48}" y="{leg_y+24}" font-size="11" fill="#111827">Actual CACTI Access Time (ns)</text>')

svg.append(f'<line x1="{leg_x+10}" y1="{leg_y+45}" x2="{leg_x+40}" y2="{leg_y+45}" stroke="#9ca3af" stroke-width="2" stroke-dasharray="6,4"/>')
svg.append(f'<text x="{leg_x+48}" y="{leg_y+49}" font-size="11" fill="#4b5563">Ideal "One Gate Delay/Doubling" (+67 ps/db)</text>')

svg.append('</svg>')

with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_b/task2_cacti_access_vs_capacity.svg", "w") as f:
    f.write("\n".join(svg))

print("Saved task2_cacti_access_vs_capacity.svg")
