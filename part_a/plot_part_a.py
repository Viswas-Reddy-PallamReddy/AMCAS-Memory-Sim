import math

# Load Task 1 data (W = 0.16u)
with open("read_task1.csv") as f:
    t1_lines = [l.strip().split() for l in f if l.strip()]
t1_rows = [[float(x) for x in l] for l in t1_lines]
t1_t = [r[0]*1e9 for r in t1_rows]
t1_q = [r[5] for r in t1_rows]
t1_qb = [r[7] for r in t1_rows]
t1_bl = [r[1] for r in t1_rows]
t1_blb = [r[3] for r in t1_rows]

# Load Task 2 data (W = 0.24u)
with open("read_task2.csv") as f:
    t2_lines = [l.strip().split() for l in f if l.strip()]
t2_rows = [[float(x) for x in l] for l in t2_lines]
t2_t = [r[0]*1e9 for r in t2_rows]
t2_q = [r[5] for r in t2_rows]
t2_qb = [r[7] for r in t2_rows]
t2_bl = [r[1] for r in t2_rows]
t2_blb = [r[3] for r in t2_rows]

# --- PLOT 1: Task 2 V(Q) & V(QB) Disturbance Plot (SVG) ---
w, h = 800, 500
pad_l, pad_r, pad_t, pad_b = 80, 40, 50, 60
plot_w = w - pad_l - pad_r
plot_h = h - pad_t - pad_b

t_min, t_max = 0.0, 4.0
v_min, v_max = -0.05, 1.2

def x_map(t):
    return pad_l + (t - t_min) / (t_max - t_min) * plot_w

def y_map(v):
    return pad_t + (1.0 - (v - v_min) / (v_max - v_min)) * plot_h

svg1 = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#ffffff; font-family:system-ui,-apple-system,sans-serif;">']

# Title and subtitle
svg1.append(f'<text x="{w/2}" y="28" text-anchor="middle" font-size="16" font-weight="bold" fill="#111827">6T SRAM Read Disturb &amp; Storage Node Voltage v(q) Transient</text>')
svg1.append(f'<text x="{w/2}" y="44" text-anchor="middle" font-size="12" fill="#4b5563">Part A Task 2: Cell Ratio Degradation (Wax = 0.16 um [CR=1.25] vs Wax = 0.24 um [CR=0.833])</text>')

# Grid and axes
for t_val in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    x = x_map(t_val)
    svg1.append(f'<line x1="{x}" y1="{pad_t}" x2="{x}" y2="{pad_t+plot_h}" stroke="#e5e7eb" stroke-width="1"/>')
    svg1.append(f'<text x="{x}" y="{pad_t+plot_h+20}" text-anchor="middle" font-size="11" fill="#6b7280">{t_val:.1f}</text>')

for v_val in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]:
    y = y_map(v_val)
    svg1.append(f'<line x1="{pad_l}" y1="{y}" x2="{pad_l+plot_w}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>')
    svg1.append(f'<text x="{pad_l-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#6b7280">{v_val:.1f} V</text>')

# Axis labels
svg1.append(f'<text x="{pad_l+plot_w/2}" y="{h-15}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151">Time (ns)</text>')
svg1.append(f'<text x="25" y="{pad_t+plot_h/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151" transform="rotate(-90 25 {pad_t+plot_h/2})">Node Voltage (V)</text>')

# Wordline activation highlight (t >= 1.0 ns)
x_wl_on = x_map(1.0)
svg1.append(f'<rect x="{x_wl_on}" y="{pad_t}" width="{x_map(4.0)-x_wl_on}" height="{plot_h}" fill="#f3f4f6" opacity="0.4"/>')
svg1.append(f'<line x1="{x_wl_on}" y1="{pad_t}" x2="{x_wl_on}" y2="{pad_t+plot_h}" stroke="#9ca3af" stroke-dasharray="4,4" stroke-width="1.5"/>')
svg1.append(f'<text x="{x_wl_on+5}" y="{pad_t+15}" font-size="11" font-weight="bold" fill="#6b7280">WL High (Read Phase)</text>')

# Inverter trip threshold line (~0.52 V)
y_vtrip = y_map(0.52)
svg1.append(f'<line x1="{pad_l}" y1="{y_vtrip}" x2="{pad_l+plot_w}" y2="{y_vtrip}" stroke="#dc2626" stroke-dasharray="5,5" stroke-width="1.5"/>')
svg1.append(f'<text x="{pad_l+plot_w-10}" y="{y_vtrip-6}" text-anchor="end" font-size="11" font-weight="bold" fill="#dc2626">Inverter Trip Voltage Vtrip ≈ 0.52 V</text>')

def build_path(times, vals):
    pts = [f"{x_map(t):.1f},{y_map(v):.1f}" for t, v in zip(times, vals) if t_min <= t <= t_max]
    return "M " + " L ".join(pts)

# Draw Task 1: v(q) baseline (blue solid)
svg1.append(f'<path d="{build_path(t1_t, t1_q)}" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
# Draw Task 1: v(qb) baseline (blue dashed)
svg1.append(f'<path d="{build_path(t1_t, t1_qb)}" fill="none" stroke="#3b82f6" stroke-width="1.8" stroke-dasharray="4,2"/>')

# Draw Task 2: v(q) widened (orange-red solid)
svg1.append(f'<path d="{build_path(t2_t, t2_q)}" fill="none" stroke="#ea580c" stroke-width="2.5"/>')
# Draw Task 2: v(qb) widened (orange dashed)
svg1.append(f'<path d="{build_path(t2_t, t2_qb)}" fill="none" stroke="#fb923c" stroke-width="1.8" stroke-dasharray="4,2"/>')

# Peak annotations
# Task 1 peak: 270 mV at 1.15 ns
x1_pk, y1_pk = x_map(1.1525), y_map(0.2703)
svg1.append(f'<circle cx="{x1_pk}" cy="{y1_pk}" r="4" fill="#2563eb"/>')
svg1.append(f'<text x="{x1_pk+8}" y="{y1_pk-8}" font-size="11" font-weight="bold" fill="#2563eb">CR=1.25 peak: 270 mV</text>')

# Task 2 peak: 475 mV at 1.41 ns
x2_pk, y2_pk = x_map(1.4075), y_map(0.4751)
svg1.append(f'<circle cx="{x2_pk}" cy="{y2_pk}" r="4" fill="#ea580c"/>')
svg1.append(f'<text x="{x2_pk+8}" y="{y2_pk-8}" font-size="11" font-weight="bold" fill="#ea580c">CR=0.833 peak: 475 mV (Near Vtrip!)</text>')

# Legend box
leg_x, leg_y = pad_l + 20, pad_t + 30
svg1.append(f'<rect x="{leg_x}" y="{leg_y}" width="280" height="105" fill="#ffffff" stroke="#d1d5db" rx="4" opacity="0.95"/>')
# item 1
svg1.append(f'<line x1="{leg_x+10}" y1="{leg_y+20}" x2="{leg_x+40}" y2="{leg_y+20}" stroke="#2563eb" stroke-width="2.5"/>')
svg1.append(f'<text x="{leg_x+48}" y="{leg_y+24}" font-size="11" fill="#111827">v(q) Baseline (Wax = 0.16um, CR=1.25)</text>')
# item 2
svg1.append(f'<line x1="{leg_x+10}" y1="{leg_y+40}" x2="{leg_x+40}" y2="{leg_y+40}" stroke="#3b82f6" stroke-width="1.8" stroke-dasharray="4,2"/>')
svg1.append(f'<text x="{leg_x+48}" y="{leg_y+44}" font-size="11" fill="#111827">v(qb) Baseline (Wax = 0.16um)</text>')
# item 3
svg1.append(f'<line x1="{leg_x+10}" y1="{leg_y+60}" x2="{leg_x+40}" y2="{leg_y+60}" stroke="#ea580c" stroke-width="2.5"/>')
svg1.append(f'<text x="{leg_x+48}" y="{leg_y+64}" font-size="11" fill="#111827">v(q) Widened (Wax = 0.24um, CR=0.833)</text>')
# item 4
svg1.append(f'<line x1="{leg_x+10}" y1="{leg_y+80}" x2="{leg_x+40}" y2="{leg_y+80}" stroke="#fb923c" stroke-width="1.8" stroke-dasharray="4,2"/>')
svg1.append(f'<text x="{leg_x+48}" y="{leg_y+84}" font-size="11" fill="#111827">v(qb) Widened (Wax = 0.24um, sag to 0.72V)</text>')

svg1.append('</svg>')

with open("task2_vq_plot.svg", "w") as f:
    f.write("\n".join(svg1))

print("Saved task2_vq_plot.svg")


# --- PLOT 2: Task 3 Delta V vs VDD Sweep Plot (SVG) ---
# Data points from check_times.py and run_task3_sweep.py:
# VDD from 1.10 down to 0.60, and down to 0.20
vdd_pts = [1.10, 1.05, 1.00, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20]
dv_2000 = [540.76, 508.82, 476.15, 442.78, 408.72, 373.99, 338.65, 302.77, 266.48, 229.94, 193.44, 157.38, 122.43, 89.57, 60.21, 36.14, 18.91, 8.73, 3.72]
# Early sensing strobe at t = 1.15 ns (100 ps after WL full):
dv_1150 = [74.29, 69.47, 64.61, 59.70, 54.75, 49.77, 44.78, 39.77, 34.78, 29.83, 24.96]

w2, h2 = 800, 520
pad_l2, pad_r2, pad_t2, pad_b2 = 80, 40, 55, 65
plot_w2 = w2 - pad_l2 - pad_r2
plot_h2 = h2 - pad_t2 - pad_b2

v_min2, v_max2 = 0.15, 1.15
dv_min, dv_max = 0, 600

def x2_map(v):
    return pad_l2 + (v - v_min2) / (v_max2 - v_min2) * plot_w2

def y2_map(dv):
    return pad_t2 + (1.0 - (dv - dv_min) / (dv_max - dv_min)) * plot_h2

svg2 = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w2} {h2}" width="{w2}" height="{h2}" style="background:#ffffff; font-family:system-ui,-apple-system,sans-serif;">']

# Title and subtitle
svg2.append(f'<text x="{w2/2}" y="26" text-anchor="middle" font-size="16" font-weight="bold" fill="#111827">Part A Task 3: Differential Bitline Voltage ΔV vs Supply Voltage V_DD</text>')
svg2.append(f'<text x="{w2/2}" y="44" text-anchor="middle" font-size="12" fill="#4b5563">Evaluation of Sensing Margin against 25 mV Sense-Amplifier Offset</text>')

# Grid and axes
for v_val in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]:
    x = x2_map(v_val)
    svg2.append(f'<line x1="{x}" y1="{pad_t2}" x2="{x}" y2="{pad_t2+plot_h2}" stroke="#e5e7eb" stroke-width="1"/>')
    svg2.append(f'<text x="{x}" y="{pad_t2+plot_h2+20}" text-anchor="middle" font-size="11" fill="#6b7280">{v_val:.1f} V</text>')

for dv_val in [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
    y = y2_map(dv_val)
    svg2.append(f'<line x1="{pad_l2}" y1="{y}" x2="{pad_l2+plot_w2}" y2="{y}" stroke="#e5e7eb" stroke-width="1"/>')
    svg2.append(f'<text x="{pad_l2-10}" y="{y+4}" text-anchor="end" font-size="11" fill="#6b7280">{dv_val} mV</text>')

# Axis labels
svg2.append(f'<text x="{pad_l2+plot_w2/2}" y="{h2-18}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151">Supply Voltage V_DD (V)</text>')
svg2.append(f'<text x="25" y="{pad_t2+plot_h2/2}" text-anchor="middle" font-size="13" font-weight="600" fill="#374151" transform="rotate(-90 25 {pad_t2+plot_h2/2})">Bitline Differential ΔV (mV)</text>')

# 25 mV Sense Amplifier Offset line
y_sa = y2_map(25)
svg2.append(f'<line x1="{pad_l2}" y1="{y_sa}" x2="{pad_l2+plot_w2}" y2="{y_sa}" stroke="#dc2626" stroke-dasharray="6,4" stroke-width="2"/>')
svg2.append(f'<text x="{pad_l2+plot_w2-10}" y="{y_sa-7}" text-anchor="end" font-size="11" font-weight="bold" fill="#dc2626">Sense-Amp Input-Referred Offset = 25 mV (Lecture 5)</text>')

# Draw curve 1: dv at t = 2.0 ns
pts1 = [f"{x2_map(v):.1f},{y2_map(d):.1f}" for v, d in zip(vdd_pts, dv_2000)]
svg2.append(f'<path d="M ' + ' L '.join(pts1) + '" fill="none" stroke="#2563eb" stroke-width="2.5"/>')
for v, d in zip(vdd_pts, dv_2000):
    svg2.append(f'<circle cx="{x2_map(v):.1f}" cy="{y2_map(d):.1f}" r="3.5" fill="#2563eb"/>')

# Draw curve 2: dv at t = 1.15 ns (early sensing window)
pts2 = [f"{x2_map(v):.1f},{y2_map(d):.1f}" for v, d in zip(vdd_pts[:11], dv_1150)]
svg2.append(f'<path d="M ' + ' L '.join(pts2) + '" fill="none" stroke="#059669" stroke-width="2.5" stroke-dasharray="6,3"/>')
for v, d in zip(vdd_pts[:11], dv_1150):
    svg2.append(f'<circle cx="{x2_map(v):.1f}" cy="{y2_map(d):.1f}" r="3.5" fill="#059669"/>')

# Intersections and annotations
# At t = 1.15 ns, VDD = 0.60 V -> 24.96 mV (~25 mV)
x_cross1, y_cross1 = x2_map(0.60), y2_map(24.96)
svg2.append(f'<circle cx="{x_cross1}" cy="{y_cross1}" r="6" fill="none" stroke="#dc2626" stroke-width="2"/>')
svg2.append(f'<text x="{x_cross1+10}" y="{y_cross1+16}" font-size="11" font-weight="bold" fill="#059669">Early sensing failure: VDD = 0.60 V (ΔV = 24.96 mV)</text>')

# At t = 2.0 ns, crossing is around VDD = 0.323 V
v_cross2 = 0.323
x_cross2, y_cross2 = x2_map(v_cross2), y2_map(25.0)
svg2.append(f'<circle cx="{x_cross2}" cy="{y_cross2}" r="6" fill="none" stroke="#dc2626" stroke-width="2"/>')
svg2.append(f'<text x="{x_cross2-15}" y="{y_cross2-12}" font-size="11" font-weight="bold" fill="#2563eb" text-anchor="end">Unstrobed (2 ns) crossing: VDD ≈ 0.32 V</text>')

# Legend
leg2_x, leg2_y = pad_l2 + 25, pad_t2 + 20
svg2.append(f'<rect x="{leg2_x}" y="{leg2_y}" width="340" height="90" fill="#ffffff" stroke="#d1d5db" rx="4" opacity="0.95"/>')
svg2.append(f'<line x1="{leg2_x+10}" y1="{leg2_y+20}" x2="{leg2_x+40}" y2="{leg2_y+20}" stroke="#2563eb" stroke-width="2.5"/>')
svg2.append(f'<circle cx="{leg2_x+25}" cy="{leg2_y+20}" r="3.5" fill="#2563eb"/>')
svg2.append(f'<text x="{leg2_x+48}" y="{leg2_y+24}" font-size="11" fill="#111827">ΔV at t = 2.0 ns (netlist meas: 1 ns after WL)</text>')

svg2.append(f'<line x1="{leg2_x+10}" y1="{leg2_y+45}" x2="{leg2_x+40}" y2="{leg2_y+45}" stroke="#059669" stroke-width="2.5" stroke-dasharray="6,3"/>')
svg2.append(f'<circle cx="{leg2_x+25}" cy="{leg2_y+45}" r="3.5" fill="#059669"/>')
svg2.append(f'<text x="{leg2_x+48}" y="{leg2_y+49}" font-size="11" fill="#111827">ΔV at t = 1.15 ns (realistic ~100 ps sensing strobe)</text>')

svg2.append(f'<line x1="{leg2_x+10}" y1="{leg2_y+70}" x2="{leg2_x+40}" y2="{leg2_y+70}" stroke="#dc2626" stroke-dasharray="6,4" stroke-width="2"/>')
svg2.append(f'<text x="{leg2_x+48}" y="{leg2_y+74}" font-size="11" fill="#dc2626" font-weight="bold">Sense-Amp Offset Limit (25 mV)</text>')

svg2.append('</svg>')

with open("task3_dv_vs_vdd.svg", "w") as f:
    f.write("\n".join(svg2))

print("Saved task3_dv_vs_vdd.svg")
