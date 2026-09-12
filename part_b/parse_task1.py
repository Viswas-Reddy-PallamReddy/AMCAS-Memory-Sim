import subprocess

p = subprocess.run(["./cacti", "-infile", "partb_task1.cfg"], cwd="/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/simulators/cacti", capture_output=True, text=True)

with open("/mnt/c/Users/Viswas/OneDrive/Desktop/4_1/AMCAS/assignment1_work/part_b/cacti_task1_out.txt", "w") as f:
    f.write(p.stdout)

print("Saved output to cacti_task1_out.txt")

# Let's extract key metrics
lines = p.stdout.splitlines()
recording = False
for l in lines:
    if "Uniform Cache Access SRAM Model" in l:
        recording = True
    if recording:
        if "top 3 best memory configurations" in l:
            break
        print(l)
