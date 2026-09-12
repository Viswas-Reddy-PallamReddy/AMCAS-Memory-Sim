import subprocess
import os
import shutil

# Copy sample.cell and STT_cache.cfg into simulators/nvsim to ensure nvsim finds everything
sim_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/nvsim"
shutil.copy("sample.cell", os.path.join(sim_dir, "sample.cell"))
shutil.copy("STT_cache.cfg", os.path.join(sim_dir, "STT_cache.cfg"))

print("Running NVSim on STT_cache.cfg...")
p = subprocess.run(["./nvsim", "STT_cache.cfg"], cwd=sim_dir, capture_output=True, text=True)

with open("nvsim_task1_out.txt", "w") as f:
    f.write(p.stdout)
    if p.stderr:
        f.write("\nSTDERR:\n" + p.stderr)

print(f"Exit code: {p.returncode}")
print("STDOUT SUMMARY:")
for line in p.stdout.splitlines():
    if any(k in line for k in ["Cache Hit Latency", "Cache Write Latency", "Cache Hit Dynamic Energy", "Cache Write Dynamic Energy", "Total Area =", "Cache Total Leakage Power", "Data Array Area", "Tag Array Area"]):
        print(line)
