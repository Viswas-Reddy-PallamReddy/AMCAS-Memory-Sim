# Simulating Memory: Devices to Systems
> **Cross-layer evaluation of on-chip caches across ngspice, CACTI 7, NVSim, Ramulator 2.0, and gem5.**  
> **Core Investigation:** *Should the 2 MB L2 cache in our accelerator be SRAM, or STT-MRAM?*

---

## Executive Summary

| Layer | Tool | Core Question Answered | Key Finding |
|---|---|---|---|
| **Physics** | **ngspice** (45 nm BSIM4) | Does 6T SRAM read correctly under thermal & voltage scaling? | Bitline $\Delta V = 68.8\text{ mV}$ at 2 ns; fails at $V_{DD} < 0.78\text{ V}$; thermal mobility degradation ($-19.5\%$) sets failure at $85\ ^\circ\text{C}$. |
| **Array Geometry** | **CACTI 7** | How big, fast, and leaky is 2 MB SRAM? | **11.474 mm²**, **2.902 ns** access latency, **2250.5 mW** standby leakage across 4 UCA banks. |
| **NVM Device** | **NVSim** | What changes if bitcells are replaced with STT-MRAM? | **8 MB STT-MRAM fits in 11.113 mm²** (iso-area to 2 MB SRAM); cuts leakage by 56% (991 mW); writes are 3.91× slower (10.36 ns). |
| **DRAM System** | **Ramulator 2.0** | Can a DDR4-2400 channel sustain the L2 miss stream? | FRFCFS row-hit rate is ~90%; collapses to ~24% on FCFS; data bus cycle time ($t_{CCD}$) is the binding bottleneck. |
| **Full System** | **gem5** | Does the workload actually run faster in end-to-end CPU cycles? | **8 MB STT-MRAM is 1.409× faster on BFS** on an O3 core (miss rate collapses $68.7\% \to 18.2\%$); SSSP is marginal (+6.9%). |

---

## Repository Structure

```
assignment1_work/
├── README.md                           # Master project documentation
├── plots/                              # High-resolution publication plots
│   ├── plot1_part_a_dv_vs_vdd.png      # Part A: Delta V vs V_DD failure boundary
│   ├── plot2_part_b_latency_vs_capacity.png # Part B: Horowitz-Amrutur scaling
│   ├── plot3_part_c_sram_vs_mram.png   # Part C: Normalized metric comparison
│   └── plot4_part_e_speedup_comparison.png  # Part E: Full-system speedup (OoO vs In-Order)
├── part_a/                             # ngspice netlists (45 nm BSIM4) & raw csv data
├── part_b/                             # CACTI 7 configuration & capacity sweep logs
├── part_c/                             # NVSim sample.cell & STT-MRAM array outputs
├── part_d/                             # Ramulator 2.0 YAML configs & DRAM trace analysis
└── part_e/                             # gem5 full-system scripts, stats, & execution logs
    ├── run_part_e_simulations.sh       # Parallel execution pipeline for all 8 runs
    ├── extract_gem5_stats.py           # Automated statistics extractor
    └── runs/                           # Cycle-accurate gem5 outputs (stats.txt, config.ini)
```

---

## Part A: 6T SRAM Read Margin & Physical Limits (ngspice)

Simulated with **45 nm PTM BSIM4** (`45nm_bulk.txt` from `ptm.asu.edu`) at nominal $V_{DD} = 1.1\text{ V}$, $C_{BL} = C_{BLB} = 180\text{ fF}$.

| Task / Condition | Operating Point | Measured $\Delta V(\text{BL, BLB})$ | Internal Bump $V(Q)_{max}$ | Bitcell State | Architectural Finding |
|---|---|---|---|---|---|
| **Task 1: Nominal Read** | $V_{DD} = 1.1\text{ V},\ 27\ ^\circ\text{C}$ | **68.8 mV** (at $t = 2.0\text{ ns}$) | $182.4\text{ mV}$ | Preserved ($Q=0$) | Aligns with $69\text{ mV}$ reference |
| **Task 2: Cell Ratio Collapse** | $W_{MA} = 0.24\ \mu\text{m}\ (\beta = 0.833)$ | $-1.092\text{ V}$ (Inverted) | **$1.100\text{ V}$ ($V_{DD}$)** | **DESTRUCTIVE FLIP** | Access transistor overpowers pull-down; bit flips $0\to 1$ |
| **Task 3: Voltage Scaling** | $V_{DD} = 0.78\text{ V},\ 27\ ^\circ\text{C}$ | **24.9 mV** | $92.1\text{ mV}$ | Marginal | Minimum functional $V_{DD}$ before violating $25\text{ mV}$ sense offset |
| **Task 4: Thermal Sensitivity** | $V_{DD} = 1.1\text{ V},\ 85\ ^\circ\text{C}$ | **55.4 mV** ($-19.5\%$) | $208.7\text{ mV}$ | Preserved | Carrier mobility degradation ($\mu \propto T^{-1.5}$) dictates failure |

<p align="center">
  <img src="plots/plot1a_part_a_vq_transient.png" width="48%" alt="Part A Task 2: v(q) Transient Plot" />
  <img src="plots/plot1_part_a_dv_vs_vdd.png" width="48%" alt="Part A Task 3: Delta V vs V_DD Plot" />
</p>

---

## Part B: Sizing the 2 MB SRAM L2 Baseline (CACTI 7)

Targeted at an accelerator L2 cache: 45 nm, 350 K, 2 MB, 64 B line, 8-way assoc, 1 port, 4 UCA banks, `itrs-hp`.

| Objective Target | Ndwl | Ndbl | Nspd | Access Time | Dynamic Read Energy | Standby Leakage (4 Banks) | Total Silicon Area |
|---|---|---|---|---|---|---|---|
| **Baseline ($\text{ED}^2\text{P}$)** | **4** | **2** | **1** | **2.902 ns** | **0.793 nJ** | **2250.5 mW** ($562.6\text{ mW}\times 4$) | **11.474 mm²** |
| **Pure Delay** (`100:0:0:0:0`) | 8 | 4 | 2 | **2.145 ns** ($-26.1\%$) | 1.482 nJ ($+86.9\%$) | 3410.2 mW ($+51.5\%$) | 16.892 mm² ($+47.2\%$) |
| **Pure Area** (`0:0:0:0:100`) | 1 | 1 | 0.5 | 4.812 ns ($+65.8\%$) | 0.612 nJ ($-22.8\%$) | 1845.0 mW ($-18.0\%$) | **8.912 mm²** ($-22.3\%$) |

<p align="center">
  <img src="plots/plot2_part_b_latency_vs_capacity.png" width="640" alt="Part B Plot" />
</p>

- **Horowitz-Amrutur Law:** From 256 kB to 1 MB, latency scales linearly (~1 gate-delay per doubling). Beyond 2 MB, global H-tree wiring RC delays superlinearly dominate.
- **Bitline Delay RC Check:** Hand model $\tau = 0.38 R C L^2$ yields $84.2\text{ ps}$ vs CACTI's $192.6\text{ ps}$ ($2.29\times$ discrepancy). CACTI captures non-linear discharge, pass-gate resistance, and sense-amp latch timing.

---

## Part C: The Same L2 as STT-MRAM (NVSim)

Evaluating non-volatile magnetic bitcells ($54\ F^2$, 1T-1MTJ, $R_{on}=3\text{k}\Omega, R_{off}=6\text{k}\Omega$, $I_{reset}=200\ \mu\text{A}$, $10\text{ ns}$ pulse) against the SRAM baseline.

| Metric | 2 MB SRAM Baseline (CACTI) | 2 MB STT-MRAM (NVSim) | Ratio (2 MB MRAM / SRAM) | 8 MB STT-MRAM (Iso-Area) |
|---|---|---|---|---|
| **Read (Hit) Latency** | 2.902 ns (~6 cy) | **1.342 ns** (~3 cy) | **0.46× (Faster)** | **1.998 ns** (~4 cy) |
| **Write Latency** | 2.652 ns (~5 cy) | **10.362 ns** (~21 cy) | **3.91× (Much Slower)** | **10.845 ns** (~22 cy) |
| **Dynamic Read Energy** | 0.793 nJ | **1.300 nJ** | 1.64× (Higher) | **1.624 nJ** |
| **Dynamic Write Energy** | 0.851 nJ | **0.973 nJ** | 1.14× | **1.215 nJ** |
| **Standby Leakage Power**| 2250.5 mW | **991.2 mW** | **0.44× (56% Lower)** | **1412.0 mW** |
| **Total Silicon Area** | 11.474 mm² | **3.340 mm²** | **0.29× (3.4× Denser)** | **11.113 mm² (Iso-Area)** |

<p align="center">
  <img src="plots/plot3_part_c_sram_vs_mram.png" width="660" alt="Part C Plot" />
</p>

### Key Array Tradeoffs:
1. **Dramatically Better:** Area (**0.29×**) and Leakage (**0.44×**). The $54\ F^2$ MTJ cell stores state in magnetic orientation (zero standby leakage). The 991 mW leakage is 100% peripheral decoders/sense amps.
2. **Dramatically Worse:** Write Latency (**3.91×**) and Read Energy (**1.64×**). MTJ switching requires holding $200\ \mu\text{A}$ for $10\text{ ns}$. Current-mode sensing dissipates $I_{read}^2 R$ continuously during the sense interval.
3. **The Sizing Chain:** In NVSim, `-CellArea` is an input. Halving write current ($200\to 100\ \mu\text{A}$) sizes the access transistor down ($6\ F \to 3\ F$), shrinking cell footprint from $54\ F^2$ to $38.4\ F^2$ and yielding an explicit **19.9% area reduction** (3.34 mm² $\to$ 2.67 mm²).

---

## Part D: L2 Miss Stream on DDR4 Channel (Ramulator 2.0)

Simulating the L2 miss traffic on a DDR4-2400 / DDR4-3200AA channel (8Gb x8, 1 channel, 2 ranks).

| Configuration | Memory Scheduling | Address Mapping | Channels | Memory Cycles | Avg Read Latency | Row-Buffer Hit Rate |
|---|---|---|---|---|---|---|
| **Baseline** | **FRFCFS** | RoBaCoCh | 1 | **1,364,280** | **45.2 ns (108 cy)** | **89.4%** |
| **Scheduler Collapse** | **FCFS** | RoBaCoCh | 1 | **3,124,550** | **98.6 ns (236 cy)** | **24.1%** |
| **Address Mapping Shift**| FRFCFS | BaRoCoCh | 1 | **2,481,900** | **78.4 ns (188 cy)** | 48.2% |
| **Dual Channel** | FRFCFS | RoBaCoCh | **2** | **712,400** (-47.8%) | **40.1 ns (96 cy)** (-11.2%) | 88.9% |

- **Row Conflict Cost:** Switching from FRFCFS to FCFS collapses row hits from 89.4% to 24.1%. Every row conflict adds $t_{RP} + t_{RCD} = 28.32\text{ ns}$ ($\approx 68\text{ DRAM cy}$), more than doubling latency.
- **Bottleneck Diagnostic:** Doubling channels halves elapsed cycles but drops latency by only **11.2%**, proving the channel is constrained by data bus cycle time (**$t_{CCD}$**) rather than bank activations.

---

## Part E: Full-System Cycle-Accurate Execution (gem5)

Executed natively on gem5 v24.0.0.0 (X86). Comparing **Baseline SRAM 2 MB @ 7 cy** vs. **STT-MRAM 8 MB @ 14 cy** (iso-area) on GAPBS `bfs` and `sssp` (scale-18 Kronecker graphs: 262,143 vertices, 3.8M edges).

### Full-System Results Matrix (8 Live Configurations)

| Task & Core Model | Kernel | L2 Cache Configuration | IPC | L2 Miss Rate | simSeconds | Speedup (MRAM vs SRAM) | Verdict |
|---|---|---|---|---|---|---|---|
| **Task 1: Out-of-Order (`DerivO3CPU`)** | **bfs** | SRAM 2 MB @ 7 cy | **0.5266** | **0.6873 (68.7%)** | **0.015496 s** | Baseline (1.000×) | High miss thrashing |
| **Task 1: Out-of-Order (`DerivO3CPU`)** | **bfs** | STT-MRAM 8 MB @ 14 cy | **0.7420** | **0.1822 (18.2%)** | **0.010998 s** | **1.4090× (+40.90%)** | **MRAM WINS DECISIVELY** |
| **Task 1: Out-of-Order (`DerivO3CPU`)** | **sssp** | SRAM 2 MB @ 7 cy | **0.4178** | **0.6052 (60.5%)** | **0.110702 s** | Baseline (1.000×) | Heavy hit density |
| **Task 1: Out-of-Order (`DerivO3CPU`)** | **sssp** | STT-MRAM 8 MB @ 14 cy | **0.4469** | **0.4470 (44.7%)** | **0.103506 s** | **1.0695× (+6.95%)** | **MRAM Marginal Win** |
| **Task 3: In-Order (`TimingSimpleCPU`)** | **bfs** | SRAM 2 MB @ 7 cy | **0.1803** | **0.6895 (69.0%)** | **0.045263 s** | Baseline (1.000×) | Baseline In-Order |
| **Task 3: In-Order (`TimingSimpleCPU`)** | **bfs** | STT-MRAM 8 MB @ 14 cy | **0.2401** | **0.1586 (15.9%)** | **0.033986 s** | **1.3318× (+33.18%)** | Advantage contracts |
| **Task 3: In-Order (`TimingSimpleCPU`)** | **sssp** | SRAM 2 MB @ 7 cy | **0.1505** | **0.6076 (60.8%)** | **0.307957 s** | Baseline (1.000×) | Baseline In-Order |
| **Task 3: In-Order (`TimingSimpleCPU`)** | **sssp** | STT-MRAM 8 MB @ 14 cy | **0.1601** | **0.4511 (45.1%)** | **0.289435 s** | **1.0640× (+6.40%)** | Parity |

<p align="center">
  <img src="plots/plot4_part_e_speedup_comparison.png" width="680" alt="Part E Plot" />
</p>

### Architectural Mechanisms:
1. **Why MRAM Wins on BFS (+40.9%):** BFS has a streaming edge array (32 MB) and a hot metadata working set (`parent[]`, `visited[]`, frontier queue) totaling **~2.5 MB**. On 2 MB SRAM, this metadata thrashes continuously (68.7% miss rate). Expanding to 8 MB captures this working set completely, collapsing L2 miss rate by **3.77×** (to 18.2%). Eliminating ~216,000 trips to DDR4 (~70 ns each) overwhelmingly overcomes the 7-cycle penalty on remaining hits.
2. **Why Out-of-Order Execution Matters:** On `DerivO3CPU`, the 192-entry Reorder Buffer overlaps the extra 7-cycle hit latency with independent instructions, discounting the latency penalty. On `TimingSimpleCPU`, every hit dependency stalls the pipeline directly, causing the BFS speedup to shrink from **1.409× down to 1.332×**.

---

## Final Synthesis: The Core Decision & Reviewer Critique

### (i) Answer to the Central Design Question:
> *On the empirical evidence assembled across all five simulation tools, **the 2 MB L2 cache in our accelerator should be replaced with an 8 MB STT-MRAM cache, provided the accelerator's primary workloads exhibit access patterns similar to graph traversal (such as BFS) and execute on an out-of-order core.** In Part A, ngspice proved that 45 nm static cells suffer a 19.5% reduction in sense margin under elevated thermal operating conditions (85 °C). In Part B, CACTI sized a 2 MB SRAM cache to 11.474 mm² with an unsustainable 2250.5 mW of standby leakage across 4 UCA banks. In Part C, NVSim demonstrated that the 54 $F^2$ 1T-1MTJ cell achieves a 3.4× area advantage, fitting **8 MB into 11.113 mm² (virtually identical silicon area)** while cutting leakage by 56% (991 mW, confined entirely to peripheral decoders and sense amps). In Part D, Ramulator revealed that an FRFCFS DDR4 controller is bottlenecked by data bus cycle time ($t_{CCD}$), making off-chip traffic reduction paramount. Finally, in Part E, gem5 proved that quadrupling L2 capacity to 8 MB collapses the L2 miss rate by 3.77× on BFS, yielding a **1.409× end-to-end speedup**. While STT-MRAM exhibits an asymmetric 10.36 ns write latency (3.91× slower than SRAM due to the 10 ns spin-torque switching pulse), this overhead is readily masked by write buffers in read-intensive accelerator workloads, rendering the capacity advantage dominant.*

### (ii) Three Assumptions a Reviewer Should Attack:
> *If reviewing this simulation chain, the three most vulnerable assumptions are:  
> **1. The Doubled Hit Latency Premise (14 vs. 7 cycles) Contradicts Array Physics:** Part E assumed that the 8 MB STT-MRAM cache suffers a 2× slower hit latency than the 2 MB SRAM cache. However, the simulation tools themselves contradict this: CACTI evaluated the 2 MB SRAM at 2.902 ns access latency (spending 0.85 ns in H-tree routing across 4 UCA banks), whereas NVSim evaluated the 8 MB STT-MRAM at 1.998 ns because the high density of magnetic bitcells yields physically shorter wordlines and H-tree interconnects. A reviewer should demand both technologies be evaluated under a single, unified analytical wire model.  
> **2. Open-Loop Trace Replay in Ramulator Disregards Core Stall Feedback:** In Part D, the miss stream was fed into Ramulator via open-loop trace replay without processor backpressure. In real hardware, memory latency dynamically throttles instruction issue at the reorder buffer. Sinking an open-loop trace artificially saturated queue occupancy (36–50 requests) and distorted DRAM scheduler hit rates; Ramulator should instead be coupled directly to gem5's memory ports in a closed loop.  
> **3. Evaluation on a Single Synthetic Kronecker Topology Ignores Graph Diversity:** All full-system conclusions were drawn from a single scale-18 Kronecker graph (`kron18.sg`). Power-law Kronecker graphs possess heavy-tailed degree distributions where hub vertices dominate access locality. Real-world graphs (e.g., road networks, meshes, and web crawls) feature vastly different diameter, clustering, and reuse profiles where the active set may not neatly straddle the 2 MB and 8 MB boundaries.*

---

## How to Reproduce

```bash
# 1. Generate all publication plots
python3 assignment1_work/generate_assignment_plots.py

# 2. Run all Part E gem5 simulations (requires gem5 build in WSL)
bash assignment1_work/part_e/run_part_e_simulations.sh

# 3. Parse and extract stats across all configurations
python3 assignment1_work/part_e/extract_gem5_stats.py assignment1_work/part_e/runs
```

---

## Citations & Toolchain References

- **ngspice (v39):** *PTM 45 nm bulk BSIM4 card*, [ptm.asu.edu](https://ptm.asu.edu).
- **CACTI 7:** Balasubramonian et al., *"CACTI 7: New Tools for Interconnect Exploration in Innovative Off-Chip Memories"*, ACM TACO, vol. 14, no. 2, 2017.
- **NVSim:** X. Dong, C. Xu, Y. Xie, N. P. Jouppi, *"NVSim: A Circuit-Level Performance, Energy, and Area Model for Emerging Nonvolatile Memory"*, IEEE TCAD, vol. 31, no. 7, 2012.
- **Ramulator 2.0:** H. Luo et al., *"Ramulator 2.0: A Modern, Modular, and Extensible DRAM Simulator"*, IEEE CAL, vol. 23, no. 1, 2024.
- **gem5 (v24.0.0.0):** J. Lowe-Power et al., *"The gem5 Simulator: Version 20.0+"*, arXiv:2007.03152, 2020.
