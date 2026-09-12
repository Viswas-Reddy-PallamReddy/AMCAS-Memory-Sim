# AMCAS Assignment 1 — Part E: gem5 Full-System Simulation Report

**Course:** ECE2.414 — Advanced Memory Circuits and Systems  
**Instructor:** Dr. Priyesh Shukla · IIIT Hyderabad · Monsoon 2026  
**Topic:** Simulating Memory: Devices to Systems (Part E — gem5)  
**Deliverable:** Full-System Performance Evaluation, Architectural Analysis & Final Design Decision  

---

## Overview & Simulation Methodology

The central design question spanning this assignment is:
> **"Should the 2 MB L2 cache in our accelerator be SRAM, or STT-MRAM?"**

While ngspice, CACTI, NVSim, and Ramulator solved device physics, array geometry, non-volatile cell switching, and DRAM scheduling respectively, **gem5** is the only simulator in this hierarchy that translates capacity and latency trades into real CPU cycles and program execution time.

### Simulation Setup & Hierarchy Parameters
All simulations were executed using **native gem5 v24.0.0.0 (X86)** in WSL (Ubuntu Linux, GCC 13 toolchain, static binaries).
- **Core Microarchitectures Evaluated:**
  - **Task 1:** Out-of-Order Core (`DerivO3CPU`, 2.0 GHz, 8-wide issue, 192-entry ROB).
  - **Task 3:** In-Order Core (`TimingSimpleCPU`, 2.0 GHz, single-issue pipeline).
- **L1 Caches:** 32 kB 8-way L1-Data Cache, 32 kB 8-way L1-Instruction Cache (2-cycle hit latency).
- **L2 Cache Configurations Compared:**
  - **Baseline SRAM (from CACTI Part B):** 2 MB capacity, 8-way associativity, **7-cycle hit latency** (matching CACTI's 2.90 ns access time).
  - **Alternative STT-MRAM (from NVSim Part C):** **8 MB capacity** (occupies 11.11 mm², matching the 11.47 mm² silicon area of 2 MB SRAM), 8-way associativity, **14-cycle hit latency** (~2× slower hit latency penalty).
- **Main Memory:** DDR4-2400 8x8 (4 GB address space, single-channel, dual-rank).
- **Workloads:** GAP Benchmark Suite (GAPBS) executing on synthetic scale-18 Kronecker graphs (`kron18.sg` for BFS, `kron18.wsg` for SSSP; 262,143 vertices, 3,805,449 undirected edges):
  - **Breadth-First Search (`bfs`):** Fast-forwarded 20,385,460 instructions through graph ingestion and Trial 1 warmup on `AtomicSimpleCPU`, switching to detailed simulation at the Trial 2 boundary.
  - **Single-Source Shortest Path (`sssp`):** Fast-forwarded 150,137,297 instructions through graph ingestion and Trial 1 warmup on `AtomicSimpleCPU`, switching to detailed simulation at the Trial 2 boundary.
  - `m5.stats.reset()` invoked at CPU switch to ensure statistics represent pure detailed kernel execution.

---

## Task 1: Out-of-Order Simulation Results (`DerivO3CPU`)

The cycle-accurate simulation statistics extracted from gem5 `stats.txt` are tabulated below:

### Table E1. Full-System Performance on Out-of-Order Core (`DerivO3CPU`)

| Kernel | L2 Cache Configuration | Capacity | Hit Latency | IPC | L2 Miss Rate | Simulated Time (simSeconds) | Total L2 Accesses | Avg L2 Miss Latency | Speedup (MRAM vs SRAM) |
|---|---|---|---|---|---|---|---|---|---|
| **bfs** | Baseline SRAM | 2 MB | 7 cy (3.5 ns) | **0.5266** | **0.6873 (68.73%)** | **0.015496 s** | 428,034 | 66.14 ns | Baseline (1.000×) |
| **bfs** | STT-MRAM Alternative | 8 MB | 14 cy (7.0 ns) | **0.7420** | **0.1822 (18.22%)** | **0.010998 s** | 424,650 | 71.89 ns | **1.4090× (+40.90%)** |
| **sssp** | Baseline SRAM | 2 MB | 7 cy (3.5 ns) | **0.4178** | **0.6052 (60.52%)** | **0.110702 s** | 3,293,898 | 72.29 ns | Baseline (1.000×) |
| **sssp** | STT-MRAM Alternative | 8 MB | 14 cy (7.0 ns) | **0.4469** | **0.4470 (44.70%)** | **0.103506 s** | 3,293,570 | 77.31 ns | **1.0695× (+6.95%)** |

---

## Task 2: Architectural Analysis of the Capacity-Latency Tradeoff

The central tradeoff of replacing SRAM with STT-MRAM at iso-silicon-area is **exchanging hit latency for capacity**: the STT-MRAM cache is **4× larger (8 MB vs 2 MB)** but pays a **2× hit latency penalty (14 cycles vs 7 cycles)**.

### For which kernel does that trade win?
The trade wins decisively for **Breadth-First Search (`bfs`)**, yielding an end-to-end execution speedup of **1.4090× (+40.90%)**. For Single-Source Shortest Path (`sssp`), the trade yields only a minor performance improvement of **1.0695× (+6.95%)**.

### What property of the kernel determines the outcome?
The decisive property is **whether the kernel's active, reused working set straddles the two cache capacities**, combined with the **ratio of L2 hits to DRAM misses**.

1. **Working Set Straddling in BFS:**
   - In scale-18 BFS, the total edge array is 32 MB and is streamed linearly once per level (spatial locality with zero long-term temporal reuse; neither 2 MB nor 8 MB can hold the full graph).
   - However, the hot traversal metadata—specifically the `parent` array ($262,143 \text{ vertices} \times 4\text{ B} \approx 1.05\text{ MB}$), the visited bitmap ($\approx 32\text{ kB}$), and the frontier/queue buffers—collectively requires **~2.2 to 3.5 MB** of storage.
   - On the 2 MB SRAM cache, this hot working set constantly thrashes and spills out to main memory, resulting in an atrocious **68.73% L2 miss rate**.
   - Expanding the cache to 8 MB allows this critical working set to fit comfortably on-chip. Consequently, the L2 miss rate plummets by **3.77×** (from **0.6873 down to 0.1822**).
   - Because each avoided DRAM miss saves $\approx 140\text{--}160\text{ CPU cycles}$ (~70 ns), eliminating over 215,000 trips to DDR4 main memory overwhelmingly compensates for paying an extra 7 cycles on the remaining L2 hits.

2. **Access Density and Reuse Saturation in SSSP:**
   - In SSSP ($\Delta$-stepping), execution involves intense priority-bucket relaxations and vertex distance updates. SSSP generates **3,293,898 L2 accesses** (nearly **7.7× higher access density** than BFS's 428,034 accesses).
   - Because distance relaxation continuously revisits adjacent vertices, SSSP has a much larger, scattered footprint. Moving from 2 MB to 8 MB only reduces the miss rate from **60.52% to 44.70%** (a 1.35× reduction).
   - More crucially, SSSP registers over **1.82 million L2 hits**. Every single one of these 1.82 million hits incurs the doubled 14-cycle latency penalty.
   - The cumulative latency penalty paid on millions of L2 hits heavily erodes the latency saved by avoiding DRAM misses, leaving only a modest 6.95% net speedup.

**Architectural Takeaway:** An iso-area capacity-for-latency trade pays off in direct proportion to how much miss traffic the extra capacity eliminates relative to the total number of hits penalized.

---

## Task 3: In-Order Core Comparison (`TimingSimpleCPU`)

To isolate the impact of core microarchitecture on memory hierarchy evaluations, both workloads were simulated on an in-order pipeline (`TimingSimpleCPU`) under identical cache configurations:

### Table E2. In-Order Core Performance (`TimingSimpleCPU`)

| Kernel | L2 Cache Configuration | Capacity | Hit Latency | IPC | L2 Miss Rate | Simulated Time (simSeconds) | Speedup (MRAM vs SRAM) |
|---|---|---|---|---|---|---|---|
| **bfs** | Baseline SRAM | 2 MB | 7 cy | **0.1803** | **0.6895** | **0.045263 s** | Baseline (1.000×) |
| **bfs** | STT-MRAM Alternative | 8 MB | 14 cy | **0.2401** | **0.1586** | **0.033986 s** | **1.3318× (+33.18%)** |
| **sssp** | Baseline SRAM | 2 MB | 7 cy | **0.1505** | **0.6076** | **0.307957 s** | Baseline (1.000×) |
| **sssp** | STT-MRAM Alternative | 8 MB | 14 cy | **0.1601** | **0.4511** | **0.289435 s** | **1.0640× (+6.40%)** |

### What Out-of-Order Execution Was Doing to Task 1 Results:
The out-of-order execution engine was **actively hiding the latency penalty of the STT-MRAM hit while allowing the core to harvest the full benefit of expanded capacity**.

1. **Latency Hiding via Dynamic Scheduling:**
   - The `DerivO3CPU` contains a 192-entry Reorder Buffer (ROB), register renaming, and multiple Miss Status Holding Registers (MSHRs).
   - When an L2 hit takes 14 cycles instead of 7 cycles, the OoO scheduler searches ahead in the instruction window and executes independent arithmetic, address generation, and non-blocking memory operations. Thus, the extra 7 cycles of hit latency are largely overlapped with independent execution, costing far less than 7 cycles of wall-clock delay.
   - However, when an access misses L2 and travels to DDR4 (~140–180 cycles), the ROB inevitably fills up and stalls even the most aggressive OoO engine. Therefore, eliminating DRAM misses delivers near-maximal performance gains to an OoO core.

2. **Full Pipeline Exposure on In-Order Core:**
   - On the `TimingSimpleCPU`, there is no ROB, no out-of-order execution, and no speculative issue. The pipeline stalls strictly upon encountering any memory load dependency.
   - Every single one of the extra 7 cycles for an L2 hit is exposed directly on the critical path as a dead pipeline stall.
   - Consequently, IPC across all benchmarks collapses by ~3× (from ~0.53 down to ~0.18 on BFS). On BFS, the MRAM speedup advantage shrinks from **1.409× down to 1.332×**. 
   - This proves that **the observed MRAM advantage in Task 1 is partially a property of the processor's microarchitecture, not of the memory technology alone**.

---

## Task 4: The Primary Deliverable

### (i) Final Recommendation & Synthesis Across Parts A–E

Based on the cumulative evidence gathered across the entire five-tool simulation pipeline, **the 2 MB L2 cache in our accelerator should indeed be replaced with an 8 MB STT-MRAM cache, provided the accelerator's primary workloads exhibit access patterns similar to graph traversal (such as BFS) and execute on an out-of-order core.** In Part A, ngspice verified that at 45 nm bulk BSIM4, static storage is physically robust at nominal $V_{DD}$ but suffers a 19.5% reduction in sense margin under elevated thermal operating conditions (85 °C). In Part B, CACTI sized a 2 MB SRAM cache to an area of 11.474 mm² and revealed a severe standby leakage dissipation of 2250.5 mW across 4 UCA banks. In Part C, NVSim demonstrated that the 54 $F^2$ 1T-1MTJ STT-MRAM bitcell achieves a 3.4× area density advantage over 6T SRAM, allowing **8 MB of STT-MRAM to fit into 11.113 mm² (virtually identical silicon footprint)** while reducing array leakage by 56% (991 mW, arising exclusively from peripheral circuits). In Part D, Ramulator proved that a single DDR4-2400 channel operating under an FRFCFS scheduler is bottlenecked by data bus cycle time ($t_{CCD}$) rather than activation timing, meaning that reducing off-chip traffic is paramount to avoiding severe queueing delays. Finally, in Part E, gem5 full-system cycle-accurate simulations proved that quadrupling L2 capacity to 8 MB collapses the L2 miss rate by 3.77× on BFS (from 68.7% down to 18.2%), producing a decisive **1.409× end-to-end execution speedup**. The primary caveat is STT-MRAM's asymmetric 10.36 ns write latency (3.91× slower than SRAM, dictated by the 10 ns spin-transfer torque switching pulse); for read-dominated accelerator workloads (e.g., graph search and neural network inference), this write overhead is easily absorbed by write buffers and MSHRs, making the 4× capacity win dominant.

### (ii) Three Assumptions to Attack as a Reviewer

If tasked with critically reviewing this simulation methodology, the three most vulnerable assumptions are:

1. **The Doubled Hit Latency Premise (14 vs. 7 cycles) Contradicts Array Physics:** Part E presumes that the 8 MB STT-MRAM cache suffers a 2× slower hit latency than the 2 MB SRAM cache. However, the simulation tools themselves contradict this: CACTI evaluated the 2 MB SRAM at 2.902 ns access latency (spending 0.85 ns in H-tree routing alone across 4 UCA banks), whereas NVSim evaluated the 8 MB STT-MRAM at 1.998 ns access latency because the smaller footprint of magnetic bitcells yields physically shorter wordlines and H-tree interconnects. The 14-cycle penalty was an arbitrary pedagogical constraint rather than a physical result. A rigorous reviewer would demand that both memory technologies be evaluated using a single, unified analytical wire and routing model.
2. **Open-Loop DRAM Trace Replay Ignores Processor Feedback:** In Part D, the L2 miss stream was evaluated in Ramulator via open-loop trace replay. The trace replay engine dispatches requests without backpressure from processor core stalls or pipeline dependency chains. In reality, memory latency dynamically throttles request generation at the CPU reorder buffer. Sinking an open-loop trace into Ramulator artificially inflated queue occupancy (averaging 36–50 requests) and distorted DRAM scheduler hit rates. The DRAM subsystem should instead be simulated with gem5 closed-loop driving the DDR4 controller in real time.
3. **Evaluation on a Single Kronecker Topology Ignores Graph Degree Heterogeneity:** All gem5 full-system conclusions were drawn from a single synthetic scale-18 Kronecker graph (`kron18.sg`/`kron18.wsg`, 262k nodes, 3.8M edges). Power-law Kronecker graphs possess heavy-tailed degree distributions where a small fraction of hub vertices account for a large portion of accesses. Real-world sparse graphs (e.g., road networks, web crawls, and biological interaction graphs) have drastically different clustering coefficients, diameter, and working set footprints. Declaring a technology-wide architectural win for STT-MRAM based on a single synthetic topology risks gross mischaracterization under workloads where the active set does not neatly straddle the 2 MB and 8 MB thresholds.

---

## Final Verification Checklist

- [x] gem5 v24.0.0.0 compiled and linked natively in WSL with zero compiler warnings/errors.
- [x] All 8 Part E full-system simulations executed to completion with exact statistics extracted.
- [x] Task 1: O3 CPU simulated on BFS and SSSP; IPC, miss rate, simSeconds reported.
- [x] Task 2: Architectural explanation of working set straddling and access density detailed.
- [x] Task 3: In-Order CPU simulated on BFS and SSSP; OoO latency-hiding mechanism explained.
- [x] Task 4: Two comprehensive deliverable paragraphs addressing the central design question and three reviewer critique points.
- [x] Zero external code or text plagiarism; all results derived directly from native execution.
