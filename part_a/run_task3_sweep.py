import subprocess
import os

vdd_values = [round(1.10 - i * 0.05, 3) for i in range(11)]  # 1.1 down to 0.6
print(f"VDD values to test: {vdd_values}")

results = []

for vdd in vdd_values:
    netlist = f"""* AMCAS Assignment 1 - Part A Task 3 Sweep VDD={vdd}
.include 45nm_bulk.txt
.param VDD={vdd} VBL={vdd}
Vdd vdd 0 'VDD'
Vwl wl 0 PWL(0 0 1n 0 1.05n 'VDD')
MP1 qb q vdd vdd pmos W=0.15u L=0.045u
MN1 qb q 0 0 nmos W=0.20u L=0.045u
MP2 q qb vdd vdd pmos W=0.15u L=0.045u
MN2 q qb 0 0 nmos W=0.20u L=0.045u
MA1 bl wl q 0 nmos W=0.16u L=0.045u
MA2 blb wl qb 0 nmos W=0.16u L=0.045u
Cbl bl 0 180f IC='VBL'
Cblb blb 0 180f IC='VBL'
.ic v(q)=0 v(qb)='VDD'
.control
 tran 5p 4n uic
 let diff = v(blb) - v(bl)
 meas tran dv FIND diff AT=2.0n
 meas tran qmax MAX v(q) FROM=1n TO=4n
 quit
.endc
.end
"""
    with open("temp_sweep.cir", "w") as f:
        f.write(netlist)
        
    p = subprocess.run(["ngspice", "-b", "temp_sweep.cir"], capture_output=True, text=True)
    out = p.stdout
    
    dv = None
    qmax = None
    for line in out.splitlines():
        if "dv  " in line or line.strip().startswith("dv =") or "dv                  =" in line:
            parts = line.split("=")
            if len(parts) >= 2:
                dv = float(parts[1].strip().split()[0])
        if "qmax" in line and "=" in line:
            parts = line.split("=")
            if len(parts) >= 2:
                qmax = float(parts[1].strip().split()[0])
                
    results.append((vdd, dv, qmax))
    print(f"VDD = {vdd:.2f} V | DeltaV = {dv*1000 if dv else 0:.2f} mV | qmax = {qmax*1000 if qmax else 0:.2f} mV")

with open("task3_python_results.csv", "w") as f:
    f.write("vdd,dv_mv,qmax_mv\n")
    for vdd, dv, qmax in results:
        f.write(f"{vdd:.3f},{dv*1000 if dv else 0:.4f},{qmax*1000 if qmax else 0:.4f}\n")

print("Done! Saved to task3_python_results.csv")
