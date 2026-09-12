with open("read_task2.csv") as f:
    lines = [line.strip().split() for line in f if line.strip()]

rows = [[float(x) for x in l] for l in lines]
times = [r[0] for r in rows]
bl = [r[1] for r in rows]
blb = [r[3] for r in rows]
q = [r[5] for r in rows]
qb = [r[7] for r in rows]

print("--- Task 2 Key Timepoints ---")
for t_target in [0.5e-9, 1.0e-9, 1.2e-9, 1.4075e-9, 1.6e-9, 2.0e-9, 3.0e-9, 4.0e-9]:
    idx = min(range(len(times)), key=lambda i: abs(times[i] - t_target))
    t_val = times[idx] * 1e9
    print(f"t={t_val:.3f}ns: q={q[idx]:.4f}V, qb={qb[idx]:.4f}V, bl={bl[idx]:.4f}V, blb={blb[idx]:.4f}V, dv={(blb[idx]-bl[idx])*1e3:.1f}mV")
