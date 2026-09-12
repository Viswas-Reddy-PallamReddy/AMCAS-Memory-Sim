import subprocess

netlist = """* AMCAS Central Question: VDD=0.7V, Temp=85C
.include 45nm_bulk.txt
.param VDD=0.7 VBL=0.7
.temp 85
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
 wrdata read_central_q.csv v(bl) v(blb) v(q) v(qb)
 quit
.endc
.end
"""

with open("central_q.cir", "w") as f:
    f.write(netlist)

p = subprocess.run(["ngspice", "-b", "central_q.cir"], capture_output=True, text=True)
print(p.stdout)
