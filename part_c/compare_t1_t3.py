# Compare Task 1 vs Task 3 in NVSim
def extract_metrics(fname):
    with open(fname) as f:
        text = f.read()
    metrics = {}
    for line in text.splitlines():
        if "Total Area =" in line and "mm^2" in line and "total_area" not in metrics:
            metrics["total_area"] = line.split("=")[1].strip()
        elif "Data Array Area" in line and "data_area" not in metrics:
            metrics["data_area"] = line.split("=")[1].strip()
        elif "Cache Hit Latency" in line:
            metrics["read_lat"] = line.split("=")[1].strip()
        elif "Cache Write Latency" in line:
            metrics["write_lat"] = line.split("=")[1].strip()
        elif "Cache Hit Dynamic Energy" in line:
            metrics["read_energy"] = line.split("=")[1].strip()
        elif "Cache Write Dynamic Energy" in line:
            metrics["write_energy"] = line.split("=")[1].strip()
        elif "Cache Total Leakage Power" in line:
            metrics["leakage"] = line.split("=")[1].strip()
        elif "Senseamp Latency" in line and "sa_latency" not in metrics:
            metrics["sa_latency"] = line.split("=")[1].strip()
        elif "Bitline Latency" in line and "bl_latency" not in metrics:
            metrics["bl_latency"] = line.split("=")[1].strip()
    return metrics

base_path = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_c"
m1 = extract_metrics(f"{base_path}/nvsim_task1_out.txt")
m3 = extract_metrics(f"{base_path}/nvsim_task3_out.txt")

print(f"{'Metric':25s} | {'Task 1 (TMR 100%)':22s} | {'Task 3 (TMR 200%)':22s}")
print("-" * 75)
for k in ["read_lat", "sa_latency", "bl_latency", "write_lat", "read_energy", "write_energy", "leakage", "total_area", "data_area"]:
    print(f"{k:25s} | {m1.get(k, 'N/A'):22s} | {m3.get(k, 'N/A'):22s}")
