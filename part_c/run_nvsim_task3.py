import subprocess
import os
import shutil

sim_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/nvsim"

# Create task3_tmr.cell with Ron = 4000, Roff = 12000
with open("sample.cell") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip().startswith("-ResistanceOn"):
        new_lines.append("-ResistanceOn (ohm): 4000\n")
    elif line.strip().startswith("-ResistanceOff"):
        new_lines.append("-ResistanceOff (ohm): 12000\n")
    else:
        new_lines.append(line)

with open("task3_tmr.cell", "w") as f:
    f.writelines(new_lines)

shutil.copy("task3_tmr.cell", os.path.join(sim_dir, "task3_tmr.cell"))

# Create config pointing to task3_tmr.cell
with open("STT_cache.cfg") as f:
    cfg_lines = f.readlines()

new_cfg = []
for line in cfg_lines:
    if line.strip().startswith("-MemoryCellInputFile:"):
        new_cfg.append("-MemoryCellInputFile: task3_tmr.cell\n")
    else:
        new_cfg.append(line)

with open("STT_cache_tmr.cfg", "w") as f:
    f.writelines(new_cfg)

shutil.copy("STT_cache_tmr.cfg", os.path.join(sim_dir, "STT_cache_tmr.cfg"))

print("Running NVSim for Task 3 (TMR 200%)...")
p = subprocess.run(["./nvsim", "STT_cache_tmr.cfg"], cwd=sim_dir, capture_output=True, text=True)

with open("nvsim_task3_out.txt", "w") as f:
    f.write(p.stdout)

print(f"Exit code: {p.returncode}")
for line in p.stdout.splitlines():
    if any(k in line for k in ["Cache Hit Latency", "Cache Write Latency", "Cache Hit Dynamic Energy", "Cache Write Dynamic Energy", "Total Area =", "Cache Total Leakage Power", "Senseamp Latency", "Bitline & Cell Read Energy"]):
        print(line)
