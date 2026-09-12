import subprocess

objectives = [
    ("delay", "NONE", "100:0:0:0:0"),
    ("area", "NONE", "0:0:0:0:100"),
    ("ED2P", "ED^2", "0:0:0:100:0"),
]

with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/partb_task1.cfg") as f:
    base_lines = f.readlines()

results = []

for name, opt_tag, weights in objectives:
    cfg_lines = []
    for line in base_lines:
        l_strip = line.strip()
        if l_strip.startswith("-Optimize ED or ED^2"):
            cfg_lines.append(f'-Optimize ED or ED^2 (ED, ED^2, NONE): "{opt_tag}"\n')
        elif l_strip.startswith("-design objective (weight"):
            cfg_lines.append(f'-design objective (weight delay, dynamic power, leakage power, cycle time, area) {weights}\n')
        elif l_strip.startswith("-deviate (delay,"):
            cfg_lines.append('-deviate (delay, dynamic power, leakage power, cycle time, area) 100000:100000:100000:100000:100000\n')
        else:
            cfg_lines.append(line)
            
    cfg_file = f"partb_obj_{name}.cfg"
    with open(f"/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/{cfg_file}", "w") as f:
        f.writelines(cfg_lines)
        
    p = subprocess.run(["./cacti", "-infile", cfg_file], cwd="/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti", capture_output=True, text=True)
    out = p.stdout
    
    access_time = None
    dyn_read_energy = None
    leakage = None
    area = None
    ndwl = None
    ndbl = None
    nspd = None
    
    for l in out.splitlines():
        if "Access time (ns):" in l:
            access_time = float(l.split(":")[1].strip())
        elif "Total dynamic read energy per access (nJ):" in l:
            dyn_read_energy = float(l.split(":")[1].strip()) * 1000 # pJ
        elif "Total leakage power of a bank (mW):" in l:
            leakage = float(l.split(":")[1].strip())
        elif "Cache height x width (mm):" in l:
            dims = l.split(":")[1].strip().split("x")
            area = float(dims[0].strip()) * float(dims[1].strip())
        elif "Best Ndwl :" in l:
            ndwl = int(l.split(":")[1].strip())
        elif "Best Ndbl :" in l:
            ndbl = int(l.split(":")[1].strip())
        elif "Best Nspd :" in l:
            nspd = float(l.split(":")[1].strip())
            
    results.append({
        "objective": name,
        "access_time_ns": access_time,
        "dyn_read_energy_pJ": dyn_read_energy,
        "bank_leakage_mW": leakage,
        "area_mm2": area,
        "Ndwl": ndwl,
        "Ndbl": ndbl,
        "Nspd": nspd
    })
    print(f"Objective: {name:8s} | (Ndwl, Ndbl, Nspd) = ({ndwl}, {ndbl}, {nspd}) | Access: {access_time:.4f} ns | DynE: {dyn_read_energy:.2f} pJ | Area: {area:.4f} mm2")

with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_b/task3_objectives.csv", "w") as f:
    f.write("objective,Ndwl,Ndbl,Nspd,access_time_ns,dyn_read_energy_pJ,bank_leakage_mW,area_mm2\n")
    for r in results:
        f.write(f"{r['objective']},{r['Ndwl']},{r['Ndbl']},{r['Nspd']},{r['access_time_ns']},{r['dyn_read_energy_pJ']},{r['bank_leakage_mW']},{r['area_mm2']}\n")

print("Saved task3_objectives.csv")
