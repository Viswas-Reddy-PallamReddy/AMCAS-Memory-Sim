import os

def parse_nvsim_full(filepath):
    with open(filepath) as f:
        content = f.read()
    res = {}
    for line in content.splitlines():
        line_str = line.strip()
        if "Total Area =" in line_str and "mm^2" in line_str and "total_area" not in res:
            res["total_area"] = line_str.split("=")[1].strip()
        elif "Data Array Area" in line_str and "data_area" not in res:
            res["data_area"] = line_str.split("=")[1].strip()
        elif "Tag Array Area" in line_str and "tag_area" not in res:
            res["tag_area"] = line_str.split("=")[1].strip()
        elif "Cache Hit Latency" in line_str:
            res["read_lat"] = line_str.split("=")[1].strip()
        elif "Cache Write Latency" in line_str:
            res["write_lat"] = line_str.split("=")[1].strip()
        elif "Cache Hit Dynamic Energy" in line_str:
            res["read_energy"] = line_str.split("=")[1].strip()
        elif "Cache Write Dynamic Energy" in line_str:
            res["write_energy"] = line_str.split("=")[1].strip()
        elif "Cache Total Leakage Power" in line_str:
            res["leakage"] = line_str.split("=")[1].strip()
        elif "Senseamp Latency" in line_str and "sa_lat" not in res:
            res["sa_lat"] = line_str.split("=")[1].strip()
        elif "Bitline Latency" in line_str and "bl_lat" not in res:
            res["bl_lat"] = line_str.split("=")[1].strip()
        elif "Bitline & Cell Read Energy" in line_str and "bl_read_energy" not in res:
            res["bl_read_energy"] = line_str.split("=")[1].strip()
        elif "Bitline & Cell Write Energy" in line_str and "bl_write_energy" not in res:
            res["bl_write_energy"] = line_str.split("=")[1].strip()
        elif "Bank Organization:" in line_str and "bank_org" not in res:
            res["bank_org"] = line_str.split(":")[1].strip()
        elif "Mat Organization:" in line_str and "mat_org" not in res:
            res["mat_org"] = line_str.split(":")[1].strip()
        elif "Subarray Size" in line_str and "sub_size" not in res:
            res["sub_size"] = line_str.split(":")[1].strip()
    return res

base_dir = "/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_c"
t1 = parse_nvsim_full(f"{base_dir}/nvsim_task1_out.txt")
t3 = parse_nvsim_full(f"{base_dir}/nvsim_task3_out.txt")
t4a = parse_nvsim_full(f"{base_dir}/nvsim_task4_a_out.txt")
t4b = parse_nvsim_full(f"{base_dir}/nvsim_task4_b_out.txt")

# Part B SRAM baseline:
sram = {
    "read_lat": "2.902 ns",
    "write_lat": "2.652 ns (cycle time)",
    "read_energy": "0.793 nJ (792.89 pJ)",
    "write_energy": "0.793 nJ (approx read/write symmetric)",
    "leakage": "2250.53 mW (2.25 W)",
    "total_area": "11.474 mm^2",
    "data_area": "10.271 mm^2",
}

print("==========================================================================================================")
print(f"{'Metric':30s} | {'SRAM (Part B)':20s} | {'STT Task 1 (Baseline)':22s} | {'STT Task 3 (TMR 200%)':22s} | {'STT Task 4A (100uA only)':24s} | {'STT Task 4B (100uA + 36F2)':24s}")
print("==========================================================================================================")
keys = [
    ("Read Latency (Cache Hit)", "read_lat"),
    ("Write Latency", "write_lat"),
    ("Read Dynamic Energy", "read_energy"),
    ("Write Dynamic Energy", "write_energy"),
    ("Total Leakage Power", "leakage"),
    ("Total Cache Area", "total_area"),
    ("Data Array Area", "data_area"),
    ("Tag Array Area", "tag_area"),
    ("Senseamp Latency", "sa_lat"),
    ("Bitline Latency", "bl_lat"),
    ("Bitline & Cell Read Energy", "bl_read_energy"),
    ("Bitline & Cell Write Energy", "bl_write_energy"),
    ("Subarray Size", "sub_size"),
    ("Mat Organization", "mat_org"),
    ("Bank Organization", "bank_org"),
]

for label, k in keys:
    v_sram = sram.get(k, "-")
    v1 = t1.get(k, "-")
    v3 = t3.get(k, "-")
    v4a = t4a.get(k, "-")
    v4b = t4b.get(k, "-")
    print(f"{label:30s} | {v_sram:20s} | {v1:22s} | {v3:22s} | {v4a:24s} | {v4b:24s}")
