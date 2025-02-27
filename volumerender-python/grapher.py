import re
import pandas as pd
import matplotlib.pyplot as plt

# File path to memory profile log
memory_log_file = "memory_profile.txt"

try:
    # Read memory profile log
    with open(memory_log_file, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: File '{memory_log_file}' not found.")
    exit(1)

# Extract memory usage data
data = []
# Updated regex pattern to match memory usage with "MiB"
pattern = re.compile(r"\s*(\d+)\s+([\d.]+)\s+MiB\s+([\d.]+)\s+MiB\s+(\d+)\s+(.*)")

for line in lines:
    match = pattern.match(line)
    if match:
        try:
            line_num = int(match.group(1))
            mem_usage = float(match.group(2))  # Convert from MiB to float
            increment = float(match.group(3))  # Convert from MiB to float
            occurrences = int(match.group(4))
            code = match.group(5).strip()
            data.append((line_num, mem_usage, increment, occurrences, code))
        except ValueError:
            print(f"Skipping invalid line: {line.strip()}")

# Convert to DataFrame
if not data:
    print("Error: No valid memory profiling data found.")
    exit(1)

df = pd.DataFrame(data, columns=["Line", "Memory (MB)", "Increment (MB)", "Occurrences", "Code Line"])

# Sort by line number
df = df.sort_values(by="Line")

# Display the DataFrame
print(df)

# Save to CSV (optional)
csv_output_file = "memory_profile_results.csv"
df.to_csv(csv_output_file, index=False)
print(f"Memory profiling results saved to {csv_output_file}")

# Plot Memory Usage per Line
plt.figure(figsize=(12, 6))
plt.bar(df["Line"], df["Memory (MB)"], color="red", label="Memory Usage (MB)")
plt.xlabel("Line Number")
plt.ylabel("Memory Usage (MB)")
plt.title("Memory Usage per Line")
plt.xticks(df["Line"], rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend()
plt.savefig("memory_usage_plot.png")
plt.show()
print("Memory usage plot saved as 'memory_usage_plot.png'.")
