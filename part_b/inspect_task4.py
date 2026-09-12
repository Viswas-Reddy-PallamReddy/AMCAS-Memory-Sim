# Let's inspect the exact values in CACTI for Task 1
# Subarray size: 
# num_rows = 512 (or 256?), cell height, wire R, wire C
with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_b/cacti_task1_out.txt") as f:
    text = f.read()

# Let's find relevant lines
for line in text.splitlines():
    if any(k in line for k in ["Subarray Height", "Subarray Length", "Bitline delay", "Repeater", "Wire width", "Area efficiency"]):
        print(line)
