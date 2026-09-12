import subprocess

def run_cacti(name, opt_tag, weights, dev):
    with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/partb_task1.cfg") as f:
        base_lines = f.readlines()
    cfg_lines = []
    for line in base_lines:
        l_strip = line.strip()
        if l_strip.startswith("-Optimize ED or ED^2"):
            cfg_lines.append(f'-Optimize ED or ED^2 (ED, ED^2, NONE): "{opt_tag}"\n')
        elif l_strip.startswith("-design objective (weight"):
            cfg_lines.append(f'-design objective (weight delay, dynamic power, leakage power, cycle time, area) {weights}\n')
        elif l_strip.startswith("-deviate (delay,"):
            cfg_lines.append(f'-deviate (delay, dynamic power, leakage power, cycle time, area) {dev}\n')
        else:
            cfg_lines.append(line)
            
    fname = f"test_{name}.cfg"
    with open(f"/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/{fname}", "w") as f:
        f.writelines(cfg_lines)
        
    p = subprocess.run(["./cacti", "-infile", fname], cwd="/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti", capture_output=True, text=True)
    out = p.stdout
    
    t_acc, e_dyn, leak, area, ndwl, ndbl, nspd = None, None, None, None, None, None, None
    for l in out.splitlines():
        if "Access time (ns):" in l: t_acc = float(l.split(":")[1].strip())
        elif "Total dynamic read energy per access (nJ):" in l: e_dyn = float(l.split(":")[1].strip()) * 1000
        elif "Total leakage power of a bank (mW):" in l: leak = float(l.split(":")[1].strip())
        elif "Cache height x width (mm):" in l:
            dims = l.split(":")[1].strip().split("x")
            area = float(dims[0].strip()) * float(dims[1].strip())
        elif "Best Ndwl :" in l: ndwl = int(l.split(":")[1].strip())
        elif "Best Ndbl :" in l: ndbl = int(l.split(":")[1].strip())
        elif "Best Nspd :" in l: nspd = float(l.split(":")[1].strip())
    print(f"{name:20s} | Ndwl={ndwl} Ndbl={ndbl} Nspd={nspd} | Delay={t_acc:.4f}ns | DynE={e_dyn:.2f}pJ | Area={area:.3f}mm2")

print("--- Standard dev (20:100000:...) ---")
run_cacti("Pure Delay (std dev)", "NONE", "100:0:0:0:0", "20:100000:100000:100000:100000")
run_cacti("Pure Area (std dev)", "NONE", "0:0:0:0:100", "20:100000:100000:100000:100000")
run_cacti("ED2P (std dev)", "ED^2", "0:0:0:100:0", "20:100000:100000:100000:100000")

print("\n--- Relaxed dev (100000:100000:...) ---")
run_cacti("Pure Delay (rel dev)", "NONE", "100:0:0:0:0", "100000:100000:100000:100000:100000")
run_cacti("Pure Area (rel dev)", "NONE", "0:0:0:0:100", "100000:100000:100000:100000:100000")
run_cacti("ED2P (rel dev)", "ED^2", "0:0:0:100:0", "100000:100000:100000:100000:100000")
