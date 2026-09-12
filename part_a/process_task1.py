import sys

with open("read_task1.csv") as f:
    lines = [line.strip().split() for line in f if line.strip()]

header_or_data = []
for l in lines:
    try:
        vals = [float(x) for x in l]
        header_or_data.append(vals)
    except ValueError:
        continue

# ngspice wrdata format:
# col 0: time (for v(bl)), col 1: v(bl)
# col 2: time (for v(blb)), col 3: v(blb)
# col 4: time (for v(q)), col 5: v(q)
# col 6: time (for v(qb)), col 7: v(qb)
times = [row[0] for row in header_or_data]
v_bl = [row[1] for row in header_or_data]
v_blb = [row[3] for row in header_or_data]
v_q = [row[5] for row in header_or_data]
v_qb = [row[7] for row in header_or_data]

# Find at t = 2.0ns
target_t = 2.0e-9
best_idx = min(range(len(times)), key=lambda i: abs(times[i] - target_t))

print(f"Total points: {len(times)}")
print(f"Closest time: {times[best_idx]*1e9:.4f} ns")
print(f"v(bl)  = {v_bl[best_idx]:.6f} V")
print(f"v(blb) = {v_blb[best_idx]:.6f} V")
dv = v_blb[best_idx] - v_bl[best_idx]
print(f"Delta V(BLB, BL) = {dv*1e3:.3f} mV ({dv:.6f} V)")
print(f"v(q)   = {v_q[best_idx]:.6f} V")
print(f"v(qb)  = {v_qb[best_idx]:.6f} V")

# Find q_max from 1ns to 4ns
q_during_read = [v_q[i] for i in range(len(times)) if times[i] >= 1.0e-9]
print(f"Max v(q) during read = {max(q_during_read):.6f} V")
