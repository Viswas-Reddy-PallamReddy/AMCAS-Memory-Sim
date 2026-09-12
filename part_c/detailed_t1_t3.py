with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_c/nvsim_task1_out.txt") as f:
    t1 = f.read()
with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_c/nvsim_task3_out.txt") as f:
    t3 = f.read()

def get_sub_metrics(text):
    res = {}
    for line in text.splitlines():
        if "Bitline & Cell Read Energy" in line:
            res["bl_cell_read_energy"] = line.split("=")[1].strip()
        elif "Bitline Latency" in line:
            res["bl_lat"] = line.split("=")[1].strip()
        elif "Senseamp Dynamic Energy" in line:
            res["sa_energy"] = line.split("=")[1].strip()
        elif "Row Decoder Latency" in line:
            res["row_dec_lat"] = line.split("=")[1].strip()
        elif "Bitline & Cell Write Energy" in line:
            res["bl_cell_write_energy"] = line.split("=")[1].strip()
    return res

print("Task 1:", get_sub_metrics(t1))
print("Task 3:", get_sub_metrics(t3))
