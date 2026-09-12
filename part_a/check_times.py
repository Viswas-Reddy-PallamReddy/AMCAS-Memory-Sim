import subprocess

vdd_values = [round(1.10 - i * 0.05, 3) for i in range(11)]  # 1.1 down to 0.6
print("VDD Sweep for Delta V at different timepoints:")
print("VDD (V) | dv(2.0ns) [mV] | dv(1.20ns) [mV] | dv(1.15ns) [mV] | dv(1.10ns) [mV]")
print("-" * 65)

for vdd in vdd_values:
    netlist = f"""* Task 3 multi-time meas VDD={vdd}
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
 meas tran dv_2000 FIND diff AT=2.0n
 meas tran dv_1200 FIND diff AT=1.20n
 meas tran dv_1150 FIND diff AT=1.15n
 meas tran dv_1100 FIND diff AT=1.10n
 quit
.endc
.end
"""
    with open("temp_multi.cir", "w") as f:
        f.write(netlist)
    p = subprocess.run(["ngspice", "-b", "temp_multi.cir"], capture_output=True, text=True)
    out = p.stdout
    dvs = {}
    for line in out.splitlines():
        for key in ["dv_2000", "dv_1200", "dv_1150", "dv_1100"]:
            if key in line and "=" in line:
                dvs[key] = float(line.split("=")[1].strip().split()[0]) * 1000
    print(f"{vdd:7.2f} | {dvs.get('dv_2000', 0):14.2f} | {dvs.get('dv_1200', 0):15.2f} | {dvs.get('dv_1150', 0):15.2f} | {dvs.get('dv_1100', 0):15.2f}")
