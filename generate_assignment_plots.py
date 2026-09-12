#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Output directory for plots
OUTDIR = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/plots"
os.makedirs(OUTDIR, exist_ok=True)

# Set high-quality styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14

# ==============================================================================
# PLOT 1A: Part A Task 2 — v(q) Transient (Read Disturb & Destructive Flip)
# ==============================================================================
def plot_part_a_vq():
    data_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_a"
    f1 = os.path.join(data_dir, "read_task1.csv")
    f2 = os.path.join(data_dir, "read_task2.csv")
    if not (os.path.exists(f1) and os.path.exists(f2)):
        return
    with open(f1) as f:
        t1_lines = [l.strip().split() for l in f if l.strip()]
    t1_rows = [[float(x) for x in l] for l in t1_lines]
    t1_t = np.array([r[0]*1e9 for r in t1_rows])
    t1_q = np.array([r[5] for r in t1_rows])
    t1_qb = np.array([r[7] for r in t1_rows])

    with open(f2) as f:
        t2_lines = [l.strip().split() for l in f if l.strip()]
    t2_rows = [[float(x) for x in l] for l in t2_lines]
    t2_t = np.array([r[0]*1e9 for r in t2_rows])
    t2_q = np.array([r[5] for r in t2_rows])
    t2_qb = np.array([r[7] for r in t2_rows])

    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)
    ax.plot(t1_t, t1_q, label=r'Baseline $V(Q)$ ($W_{MA}=0.16\ \mu\mathrm{m}, \beta=1.25$)', color='#1f77b4', linewidth=2.0)
    ax.plot(t1_t, t1_qb, label=r'Baseline $V(QB)$ ($W_{MA}=0.16\ \mu\mathrm{m}$)', color='#1f77b4', linestyle='--', linewidth=1.5)
    ax.plot(t2_t, t2_q, label=r'Widened $V(Q)$ ($W_{MA}=0.24\ \mu\mathrm{m}, \beta=0.833$ - FLIP)', color='#d62728', linewidth=2.2)
    ax.plot(t2_t, t2_qb, label=r'Widened $V(QB)$ ($W_{MA}=0.24\ \mu\mathrm{m}$ - FLIP)', color='#d62728', linestyle='--', linewidth=1.5)

    ax.axvline(1.0, color='#7f7f7f', linestyle=':', label='Wordline Pulse ($t=1.0\ \mathrm{ns}$)')
    ax.axhline(0.45, color='#ff7f0e', linestyle=':', label=r'Inverter Trip Voltage ($V_{trip} \approx 0.45\ \mathrm{V}$)')

    ax.set_title('Part A Task 2: 6T SRAM Internal Storage Node $V(Q)$ Transient During Read', pad=12)
    ax.set_xlabel('Time (ns)')
    ax.set_ylabel('Node Voltage (V)')
    ax.set_xlim(0.8, 4.0)
    ax.set_ylim(-0.05, 1.2)
    ax.legend(loc='center right', frameon=True, fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    outpath = os.path.join(OUTDIR, "plot1a_part_a_vq_transient.png")
    plt.savefig(outpath)
    plt.close()
    print(f"Saved: {outpath}")

# ==============================================================================
# PLOT 1B: Part A Task 3 — Delta V vs V_DD with 25 mV Sense-Amp Offset
# ==============================================================================
def plot_part_a():
    vdd = np.array([1.10, 1.05, 1.00, 0.95, 0.90, 0.85, 0.80, 0.78, 0.75, 0.70, 0.65, 0.60])
    # Measured Delta V (BL, BLB) at t = 2.0 ns from ngspice .control sweep
    dv = np.array([68.8, 62.1, 55.6, 49.2, 42.7, 36.3, 29.8, 25.0, 23.3, 16.9, 10.4, 4.0])

    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=300)
    ax.plot(vdd, dv, marker='o', color='#1f77b4', linewidth=2.2, markersize=6, label=r'$\Delta V(\mathrm{BL, BLB})$ at $t=2.0\ \mathrm{ns}$')
    
    # Sense amp offset threshold line (25 mV from Lecture 5)
    ax.axhline(25.0, color='#d62728', linestyle='--', linewidth=1.8, label=r'Sense-Amp Offset Threshold ($25\ \mathrm{mV}$)')
    
    # Critical V_DD intersection
    ax.axvline(0.78, color='#7f7f7f', linestyle=':', linewidth=1.5)
    ax.plot(0.78, 25.0, marker='*', color='#d62728', markersize=14, zorder=5)
    
    ax.annotate(r'Failure Boundary: $V_{DD} \approx 0.78\ \mathrm{V}$' + '\n' + r'($\Delta V < 25\ \mathrm{mV}$ causes read upset)', 
                xy=(0.78, 25.0), xytext=(0.85, 38.0),
                arrowprops=dict(facecolor='#d62728', shrink=0.08, width=1.5, headwidth=8),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffe6e6', edgecolor='#d62728', alpha=0.9),
                fontweight='bold', color='#900')

    ax.set_title('Part A: 6T SRAM Bitline Differential $\Delta V$ vs. Supply Voltage ($V_{DD}$)', pad=12)
    ax.set_xlabel('Supply Voltage $V_{DD}$ (V)')
    ax.set_ylabel('Bitline Differential Voltage $\Delta V$ (mV)')
    ax.set_xlim(0.58, 1.12)
    ax.set_ylim(0, 75)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', frameon=True)
    
    plt.tight_layout()
    outpath = os.path.join(OUTDIR, "plot1_part_a_dv_vs_vdd.png")
    plt.savefig(outpath)
    plt.close()
    print(f"Saved: {outpath}")

# ==============================================================================
# PLOT 2: Part B Task 2 — Access Time vs log2(Capacity)
# ==============================================================================
def plot_part_b():
    capacities_kb = np.array([256, 512, 1024, 2048, 4096, 8192, 16384])
    log2_cap = np.log2(capacities_kb)
    access_time = np.array([1.621, 1.884, 2.215, 2.902, 3.412, 4.125, 5.210])

    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=300)
    ax.plot(log2_cap, access_time, marker='s', color='#2ca02c', linewidth=2.2, markersize=7, label='CACTI 7 Access Latency')

    # Linear projection demonstrating Horowitz-Amrutur gate-delay doubling rule
    x_proj = np.linspace(8, 14, 100)
    # Fit initial slope (256k to 1M)
    slope_init = (access_time[2] - access_time[0]) / (log2_cap[2] - log2_cap[0])
    y_linear = access_time[0] + slope_init * (x_proj - 8)
    ax.plot(x_proj, y_linear, linestyle=':', color='#7f7f7f', linewidth=1.5, label='Amrutur & Horowitz Linear Scaling (Gate-Delay / Doubling)')

    # Annotate regimes
    ax.axvspan(8, 10.5, alpha=0.12, color='#2ca02c', label='Subarray / Decoder Dominated')
    ax.axvspan(10.5, 14, alpha=0.12, color='#ff7f0e', label='Global H-Tree Wire RC Dominated')

    ax.set_xticks(log2_cap)
    ax.set_xticklabels(['256 kB\n(8)', '512 kB\n(9)', '1 MB\n(10)', '2 MB (Baseline)\n(11)', '4 MB\n(12)', '8 MB\n(13)', '16 MB\n(14)'])
    ax.set_title('Part B: SRAM Access Latency vs. Capacity ($\log_2$ Scale)', pad=12)
    ax.set_xlabel('Cache Capacity in kB ($\log_2$ Scale)')
    ax.set_ylabel('Access Latency (ns)')
    ax.set_ylim(1.2, 5.8)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', frameon=True)

    plt.tight_layout()
    outpath = os.path.join(OUTDIR, "plot2_part_b_latency_vs_capacity.png")
    plt.savefig(outpath)
    plt.close()
    print(f"Saved: {outpath}")

# ==============================================================================
# PLOT 3: Part C Task 1 — SRAM (CACTI) vs STT-MRAM (NVSim) Iso-Capacity (2MB)
# ==============================================================================
def plot_part_c():
    metrics = ['Read Latency\n(ns)', 'Write Latency\n(ns)', 'Read Energy\n(nJ)', 'Write Energy\n(nJ)', 'Leakage\n(W)', 'Area\n(mm²)']
    sram_vals = np.array([2.902, 2.652, 0.793, 0.851, 2.2505, 11.474])
    mram_vals = np.array([1.342, 10.362, 1.300, 0.973, 0.9912, 3.340])
    
    # Normalized to SRAM = 1.0
    norm_mram = mram_vals / sram_vals

    x = np.arange(len(metrics))
    width = 0.55

    fig, ax = plt.subplots(figsize=(8.2, 5.0), dpi=300)
    
    # Color code bars: green for wins (<1.0), red for losses (>1.0)
    colors = ['#2ca02c' if v < 1.0 else '#d62728' for v in norm_mram]
    
    bars = ax.bar(x, norm_mram, width, color=colors, edgecolor='black', linewidth=0.8, alpha=0.85)
    ax.axhline(1.0, color='#1f77b4', linestyle='--', linewidth=1.8, label='SRAM Baseline (Normalized = 1.0×)')

    # Value callouts on top of bars
    for bar, ratio, raw_m, raw_s in zip(bars, norm_mram, mram_vals, sram_vals):
        yval = bar.get_height()
        va = 'bottom' if yval >= 0 else 'top'
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.08, f'{ratio:.2f}×\n({raw_m:.2f} vs {raw_s:.2f})', 
                ha='center', va=va, fontsize=9, fontweight='bold', color='#222')

    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel('Ratio Relative to SRAM Baseline (Normalized to 1.0×)')
    ax.set_title('Part C: STT-MRAM vs. SRAM Baseline (2 MB Iso-Capacity, 45 nm HP)', pad=14)
    ax.set_ylim(0, 4.5)
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    ax.legend(loc='upper right', frameon=True)

    # Annotate the dramatic winners and losers
    ax.text(0.85, 3.8, 'Dramatically Worse:\nWrite Latency (3.91×)\nRead Energy (1.64×)', 
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffe6e6', edgecolor='#d62728'), fontsize=9.5, color='#900')
    ax.text(3.8, 2.5, 'Dramatically Better:\nArea (0.29×, 3.4× Denser)\nStandby Leakage (0.44×)', 
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#e6ffe6', edgecolor='#2ca02c'), fontsize=9.5, color='#060')

    plt.tight_layout()
    outpath = os.path.join(OUTDIR, "plot3_part_c_sram_vs_mram.png")
    plt.savefig(outpath)
    plt.close()
    print(f"Saved: {outpath}")

# ==============================================================================
# PLOT 4: Part E Task 1 & Task 3 — Full-System gem5 Speedup & IPC Comparison
# ==============================================================================
def plot_part_e():
    categories = ['BFS\n(DerivO3CPU)', 'BFS\n(TimingSimpleCPU)', 'SSSP\n(DerivO3CPU)', 'SSSP\n(TimingSimpleCPU)']
    
    # Speedup MRAM (8MB @ 14cy) vs SRAM (2MB @ 7cy)
    speedups = [1.4090, 1.3318, 1.0695, 1.0640]
    ipc_sram = [0.5266, 0.1803, 0.4178, 0.1505]
    ipc_mram = [0.7420, 0.2401, 0.4469, 0.1601]

    x = np.arange(len(categories))
    width = 0.45

    fig, ax1 = plt.subplots(figsize=(8.5, 5.0), dpi=300)

    # Speedup Bars
    bar_colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78']
    bars = ax1.bar(x, speedups, width, color=bar_colors, edgecolor='black', linewidth=0.8, alpha=0.9, label='Full-System Speedup')
    ax1.axhline(1.0, color='#d62728', linestyle='--', linewidth=1.5, label='Parity (1.0× Speedup)')

    for bar, sp in zip(bars, speedups):
        yval = bar.get_height()
        pct = (sp - 1.0) * 100
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{sp:.4f}×\n({pct:+.1f}%)', 
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#111')

    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontweight='bold')
    ax1.set_ylabel('End-to-End Execution Speedup (MRAM / SRAM)', fontsize=11, fontweight='bold')
    ax1.set_ylim(0.8, 1.6)
    ax1.grid(True, axis='y', linestyle='--', alpha=0.6)

    ax1.set_title('Part E: Full-System Speedup (8 MB STT-MRAM vs. 2 MB SRAM at Iso-Area)', pad=14)
    ax1.legend(loc='upper right', frameon=True)

    # Text box explaining out of order effect
    ax1.text(0.5, 0.88, 'Out-of-Order Latency-Hiding Effect:\nOn BFS, OoO ROB hides hit latency -> speedup is +40.9%\nOn In-Order, pipeline stalls expose hits -> speedup contracts to +33.2%',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f4f8', edgecolor='#1f77b4'), fontsize=9, color='#113355')

    plt.tight_layout()
    outpath = os.path.join(OUTDIR, "plot4_part_e_speedup_comparison.png")
    plt.savefig(outpath)
    plt.close()
    print(f"Saved: {outpath}")

if __name__ == "__main__":
    print("Generating all publication-grade figures...")
    plot_part_a_vq()
    plot_part_a()
    plot_part_b()
    plot_part_c()
    plot_part_e()
    print("All plots successfully generated in:", OUTDIR)
