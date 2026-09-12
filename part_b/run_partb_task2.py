import subprocess
import os
import math

capacities = [
    ("256kB", 262144),
    ("512kB", 524288),
    ("1MB", 1048576),
    ("2MB", 2097152),
    ("4MB", 4194304),
    ("8MB", 8388608),
    ("16MB", 16777216),
]

# Read base config
with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/partb_task1.cfg") as f:
    base_lines = f.readlines()

results = []

for label, cap_bytes in capacities:
    cfg_lines = []
    for line in base_lines:
        if line.strip().startswith("-size (bytes)"):
            cfg_lines.append(f"-size (bytes) {cap_bytes}\n")
        else:
            cfg_lines.append(line)
            
    cfg_name = f"partb_sweep_{label}.cfg"
    with open(f"/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/{cfg_name}", "w") as f:
        f.writelines(cfg_lines)
        
    p = subprocess.run(["./cacti", "-infile", cfg_name], cwd="/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti", capture_output=True, text=True)
    out = p.stdout
    
    access_time = None
    cycle_time = None
    dyn_read_energy = None
    leakage = None
    area = None
    ndwl = None
    ndbl = None
    
    for l in out.splitlines():
        if "Access time (ns):" in l:
            access_time = float(l.split(":")[1].strip())
        elif "Cycle time (ns):" in l:
            cycle_time = float(l.split(":")[1].strip())
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
            
    log2_cap = math.log2(cap_bytes / 1024) # in kB: 256->8, 512->9, 1024->10, etc.
    results.append({
        "label": label,
        "bytes": cap_bytes,
        "log2_kB": log2_cap,
        "access_time_ns": access_time,
        "cycle_time_ns": cycle_time,
        "read_energy_pJ": dyn_read_energy,
        "bank_leakage_mW": leakage,
        "total_leakage_mW": leakage * 4 if leakage else None,
        "area_mm2": area,
        "Ndwl": ndwl,
        "Ndbl": ndbl
    })
    print(f"Cap: {label:6s} | log2(kB): {log2_cap:4.1f} | Access: {access_time:.4f} ns | DynE: {dyn_read_energy:.2f} pJ | Area: {area:.3f} mm2 | Ndwl={ndwl} Ndbl={ndbl}")

with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_b/task2_capacity_sweep.csv", "w") as f:
    f.write("label,bytes,log2_kB,access_time_ns,read_energy_pJ,bank_leakage_mW,total_leakage_mW,area_mm2,Ndwl,Ndbl\n")
    for r in results:
        f.write(f"{r['label']},{r['bytes']},{r['log2_kB']},{r['access_time_ns']},{r['read_energy_pJ']},{r['bank_leakage_mW']},{r['total_leakage_mW']},{r['area_mm2']},{r['Ndwl']},{r['Ndbl']}\n")

print("Saved task2_capacity_sweep.csv")
