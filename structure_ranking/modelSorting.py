# Sort and rewrite the model based on their score ranking

import re

# === Step 1: Load CSV into a dictionary ===
csv_file = "scoring_predicted_ranking.csv"
ranking = {}

with open(csv_file, "r") as f:
    next(f)  # skip header
    for line in f:
        parts = line.strip().split(",")
        if len(parts) == 2:
            name, rank = parts
            ranking[name] = int(rank)

# === Step 2: Read PDB and extract REMARK 9 block ===
pdb_file = "Target311.pdb"
output_file = "Target311_reordered.pdb"

with open(pdb_file, "r") as f:
    lines = f.readlines()

header = []
remark_lines = []
rest = []

# Assume REMARK 9 block is contiguous and starts from line 34
state = "header"
for line in lines:
    if state == "header" and not line.startswith("REMARK   9"):
        header.append(line)
    elif line.startswith("REMARK   9"):
        state = "remark"
        remark_lines.append(line)
    else:
        if state == "remark":
            state = "rest"
        rest.append(line)

# === Step 3: Classify REMARK 9 lines into ranked and unranked ===
ranked_dict = {}
unranked = []

for line in remark_lines:
    match = re.search(r"REMARK\s+9\s+MODEL\s+(\d+)", line)
    if match:
        num = int(match.group(1))
        key = f"Target311_model{num:04d}_0001"
        if key in ranking:
            ranked_dict[line] = ranking[key]
        else:
            unranked.append(line)
    else:
        unranked.append(line)
print(f"Found {len(ranked_dict)} ranked models and {len(unranked)} unranked models.")
# === Step 4: Sort ranked lines by rank ===
sorted_ranked = sorted(ranked_dict.items(), key=lambda x: x[1])
sorted_lines = [item[0] for item in sorted_ranked]

# === Step 5: Write new PDB ===
with open(output_file, "w") as f:
    f.writelines(header)
    f.writelines(sorted_lines)
    f.writelines(unranked)
    f.writelines(rest)

print(f"✅ Reordered PDB saved to: {output_file}")
