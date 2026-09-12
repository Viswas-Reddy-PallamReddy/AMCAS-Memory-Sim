import subprocess
import os

# Read the working cache.cfg from cacti directory
with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/cache.cfg") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    l_strip = line.strip()
    if l_strip.startswith("-size (bytes)"):
        new_lines.append("-size (bytes) 2097152\n")
    elif l_strip.startswith("-block size (bytes)"):
        new_lines.append("-block size (bytes) 64\n")
    elif l_strip.startswith("-associativity"):
        new_lines.append("-associativity 8\n")
    elif l_strip.startswith("-read-write port"):
        new_lines.append("-read-write port 1\n")
    elif l_strip.startswith("-UCA bank count"):
        new_lines.append("-UCA bank count 4\n")
    elif l_strip.startswith("-technology (u)"):
        new_lines.append("-technology (u) 0.045\n")
    elif l_strip.startswith("-operating temperature (K)"):
        new_lines.append("-operating temperature (K) 350\n")
    elif l_strip.startswith("-cache type"):
        new_lines.append('-cache type "cache"\n')
    elif l_strip.startswith("-Data array cell type"):
        new_lines.append('-Data array cell type - "itrs-hp"\n')
    elif l_strip.startswith("-Data array peripheral type"):
        new_lines.append('-Data array peripheral type - "itrs-hp"\n')
    elif l_strip.startswith("-Tag array cell type"):
        new_lines.append('-Tag array cell type - "itrs-hp"\n')
    elif l_strip.startswith("-Tag array peripheral type"):
        new_lines.append('-Tag array peripheral type - "itrs-hp"\n')
    elif l_strip.startswith("-Optimize ED or ED^2"):
        new_lines.append('-Optimize ED or ED^2 (ED, ED^2, NONE): "ED^2"\n')
    elif l_strip.startswith("-design objective"):
        new_lines.append('-design objective (weight delay, dynamic power, leakage power, cycle time, area) 0:0:0:100:0\n')
    else:
        new_lines.append(line)

target_cfg = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti/partb_task1.cfg"
with open(target_cfg, "w") as f:
    f.writelines(new_lines)

print("Saved partb_task1.cfg. Running CACTI...")
p = subprocess.run(["./cacti", "-infile", "partb_task1.cfg"], cwd="/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti", capture_output=True, text=True)
print(f"Exit code: {p.returncode}")
print("STDOUT:")
print(p.stdout[:2000])
if len(p.stdout) > 2000:
    print("...\n" + p.stdout[-2000:])
if p.stderr:
    print("STDERR:")
    print(p.stderr)
