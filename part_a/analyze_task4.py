with open("read_task4.csv") as f:
    lines = [line.strip().split() for line in f if line.strip()]

rows = [[float(x) for x in l] for l in lines]
times = [r[0] for r in rows]
bl = [r[1] for r in rows]
blb = [r[3] for r in rows]
q = [r[5] for r in rows]
qb = [r[7] for r in rows]
dv = [blb[i] - bl[i] for i in range(len(rows))]

print("--- Task 4 (85C) vs Task 1 (27C) ---")
for t_tgt in [1.10e-9, 1.15e-9, 1.20e-9, 2.0e-9]:
    idx = min(range(len(times)), key=lambda i: abs(times[i] - t_tgt))
    print(f"t = {times[idx]*1e9:.3f} ns: dv = {dv[idx]*1e3:.2f} mV, q = {q[idx]*1e3:.2f} mV, qb = {qb[idx]:.4f} V")

qmax_85 = max(q[i] for i in range(len(times)) if times[i] >= 1.0e-9)
print(f"qmax at 85C: {qmax_85*1e3:.2f} mV")
