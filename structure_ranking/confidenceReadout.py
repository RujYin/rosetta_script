import os
import json
import re

results = []

# Regex pattern to extract name like NAME_sample_3
pattern = re.compile(r"(.+)_summary_confidence_(sample_\d+)\.json$")

output_path = "./scripts_8VY4/output"
# Walk through the directory
for root, dirs, files in os.walk(output_path):
    for file in files:
        if file.endswith(".json") and "summary_confidence" in file:
            match = pattern.match(file)
            if not match:
                continue

            base, sample = match.groups()
            name = f"{base}_{sample}"
            filepath = os.path.join(root, file)

            try:
                with open(filepath) as f:
                    data = json.load(f)

                # Extract and average values chain_pair_iptm[2][0] and [2][1]
                v1 = data["chain_pair_iptm"][2][0]
                v2 = data["chain_pair_iptm"][2][1]
                avg = (v1 + v2) / 2

                results.append((name, avg))

            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

# Sort by average descending
results.sort(key=lambda x: x[1], reverse=True)

# Write to file
with open(f"{output_path}/Protenix_ave_iptm_chain2To0_1.txt", "w") as out:
    for name, value in results:
        out.write(f"{name}\t{value:.6f}\n")

