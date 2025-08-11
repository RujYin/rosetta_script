import csv

# Step 1: Read iptm file with ranks assigned as you go
iptm_dict = {}
with open("Protenix_ave_iptm_chain2To0_1.txt") as f:
    for i, line in enumerate(f, start=1):
        name, val = line.strip().split()
        iptm_dict[name] = (float(val), i)  # (value, rank)

# Step 2: Read and update combined_results.csv
rows = []
with open("combined_results.csv", newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["name"]
        iptm_data = iptm_dict.get(name, (None, ""))
        row["conf_score"] = iptm_data[0]
        row["conf_score_rank"] = iptm_data[1]
        rows.append(row)

# Step 3: Write updated CSV
fieldnames = list(rows[0].keys())
with open("combined_results_with_iptm.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Saved combined_results_with_iptm.csv")
