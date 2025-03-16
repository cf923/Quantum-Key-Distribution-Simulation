import subprocess
import matplotlib.pyplot as plt

process = subprocess.run(['./statistics'], capture_output=True, text=True, check=True)
output_lines = process.stdout.strip().split('\n')
floats = []
for line in output_lines:
    if line.strip():
        floats.extend(map(float, line.split()))
plt.plot(range(len(floats)), floats)