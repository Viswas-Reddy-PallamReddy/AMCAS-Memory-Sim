import subprocess
import os
import shutil

sim_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/nvsim"
base_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_c"

# 1. Test case A: Only halve ResetCurrent to 100 uA in sample.cell
with open(os.path.join(base_dir, "sample.cell")) as f:
    lines = f.readlines()

case_a_lines = []
for line in lines:
    if line.strip().startswith("-ResetCurrent"):
        case_a_lines.append("-ResetCurrent (uA): 100\n")
    elif line.strip().startswith("-SetCurrent"):
        case_a_lines.append("-SetCurrent (uA): 100\n")
    else:
        case_a_lines.append(line)

with open(os.path.join(base_dir, "task4_case_a.cell"), "w") as f:
    f.writelines(case_a_lines)
shutil.copy(os.path.join(base_dir, "task4_case_a.cell"), os.path.join(sim_dir, "task4_case_a.cell"))

# Config for Case A
with open(os.path.join(base_dir, "STT_cache.cfg")) as f:
    cfg = f.readlines()
cfg_a = [l.replace("sample.cell", "task4_case_a.cell") for l in cfg]
with open(os.path.join(base_dir, "STT_task4_a.cfg"), "w") as f:
    f.writelines(cfg_a)
shutil.copy(os.path.join(base_dir, "STT_task4_a.cfg"), os.path.join(sim_dir, "STT_task4_a.cfg"))

# Run Case A
p_a = subprocess.run(["./nvsim", "STT_task4_a.cfg"], cwd=sim_dir, capture_output=True, text=True)
with open(os.path.join(base_dir, "nvsim_task4_a_out.txt"), "w") as f:
    f.write(p_a.stdout)

print("=== Case A (Only Reset/Set Current = 100 uA, CellArea=54 F^2, W_acc=6 F) ===")
for l in p_a.stdout.splitlines():
    if any(k in l for k in ["Cache Hit Latency", "Cache Write Latency", "Cache Hit Dynamic Energy", "Cache Write Dynamic Energy", "Total Area =", "Data Array Area", "Tag Array Area", "Cache Total Leakage Power"]):
        print(l)

# 2. Test case B: Halve ResetCurrent AND adjust AccessCMOSWidth and CellArea
# If I_reset drops by 2x, required W_access drops from 6F to 3F.
# In 1T-1MTJ cell layout, bitcell width W_cell = 3F or 4F, height H_cell ~ (W_access + margin).
# When W_access drops from 6F to 3F, Cell Area scales down from 54 F^2 to ~ 36 F^2 (or ~34.5 F^2 as in aggressive cell).
case_b_lines = []
for line in lines:
    if line.strip().startswith("-ResetCurrent"):
        case_b_lines.append("-ResetCurrent (uA): 100\n")
    elif line.strip().startswith("-SetCurrent"):
        case_b_lines.append("-SetCurrent (uA): 100\n")
    elif line.strip().startswith("-AccessCMOSWidth"):
        case_b_lines.append("-AccessCMOSWidth (F): 3\n")
    elif line.strip().startswith("-CellArea"):
        # Let's test with 36 F^2
        case_b_lines.append("-CellArea (F^2): 36\n")
    else:
        case_b_lines.append(line)

with open(os.path.join(base_dir, "task4_case_b.cell"), "w") as f:
    f.writelines(case_b_lines)
shutil.copy(os.path.join(base_dir, "task4_case_b.cell"), os.path.join(sim_dir, "task4_case_b.cell"))

cfg_b = [l.replace("sample.cell", "task4_case_b.cell") for l in cfg]
with open(os.path.join(base_dir, "STT_task4_b.cfg"), "w") as f:
    f.writelines(cfg_b)
shutil.copy(os.path.join(base_dir, "STT_task4_b.cfg"), os.path.join(sim_dir, "STT_task4_b.cfg"))

p_b = subprocess.run(["./nvsim", "STT_task4_b.cfg"], cwd=sim_dir, capture_output=True, text=True)
with open(os.path.join(base_dir, "nvsim_task4_b_out.txt"), "w") as f:
    f.write(p_b.stdout)

print("\n=== Case B (Reset/Set Current = 100 uA, AccessCMOSWidth = 3 F, CellArea = 36 F^2) ===")
for l in p_b.stdout.splitlines():
    if any(k in l for k in ["Cache Hit Latency", "Cache Write Latency", "Cache Hit Dynamic Energy", "Cache Write Dynamic Energy", "Total Area =", "Data Array Area", "Tag Array Area", "Cache Total Leakage Power"]):
        print(l)
