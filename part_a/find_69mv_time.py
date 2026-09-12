with open("read_task1.csv") as f:
    lines = [line.strip().split() for line in f if line.strip()]

rows = [[float(x) for x in l] for l in lines]
times = [r[0] for r in rows]
bl = [r[1] for r in rows]
blb = [r[3] for r in rows]
dv = [blb[i] - bl[i] for i in range(len(rows))]

# Find when dv >= 0.069 V (69 mV)
for i in range(len(dv)):
    if times[i] >= 1.0e-9 and dv[i] >= 0.069:
        t_69 = times[i]
        dt = t_69 - 1.0e-9
        print(f"Delta V reaches 69 mV at t = {t_69*1e9:.4f} ns (i.e. {dt*1e12:.1f} ps after WL starts rising)")
        print(f"At this instant: dv = {dv[i]*1e3:.2f} mV")
        break

# Also print dv at t = 2.0 ns
idx_2n = min(range(len(times)), key=lambda i: abs(times[i] - 2.0e-9))
print(f"At t = 2.0 ns ({times[idx_2n]*1e9:.3f} ns): dv = {dv[idx_2n]*1e3:.2f} mV")
