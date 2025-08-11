# Merge the lrmsd and score values


def load_lrmsd_file(filename, suffix_to_strip):
    data = []
    with open(filename) as f:
        for line in f:
            path, val = line.strip().split()
            name = path.split("/")[-1].replace(suffix_to_strip, "")
            data.append((name, float(val)))
    return data

def rank_list(values):
    sorted_vals = sorted(set(values))
    return {v: i + 1 for i, v in enumerate(sorted_vals)}

# Load lrmsd_before
before_data = load_lrmsd_file("brefore_lrmsd.txt", ".cif")
before_ranks = rank_list([x[1] for x in before_data])
before_dict = {name: (val, before_ranks[val]) for name, val in before_data}

# Load lrmsd_after
after_data = load_lrmsd_file("refined_lrmsd.txt", "_0001.pdb")
after_ranks = rank_list([x[1] for x in after_data])
after_dict = {name: (val, after_ranks[val]) for name, val in after_data}

# Load score.sc
score_dict = {}
score_values = []

with open("energy_scores.sc") as f:
    for line in f:
        if line.startswith("SCORE:") and "total_score" not in line:
            parts = line.strip().split()
            score = float(parts[1])
            full_name = parts[-1]
            name = full_name.replace("_0001", "")
            score_dict[name] = score
            score_values.append(score)

score_ranks = rank_list(score_values)

# Merge and write output
merged = []
for name in set(before_dict) & set(after_dict) & set(score_dict):
    b_val, b_rank = before_dict[name]
    a_val, a_rank = after_dict[name]
    s_val = score_dict[name]
    s_rank = score_ranks[s_val]
    merged.append((name, b_val, b_rank, a_val, a_rank, s_val, s_rank))

# Sort by lrmsd_before (index 1)
merged.sort(key=lambda x: x[1])

with open("combined_results.csv", "w") as out:
    out.write("name,lrmsd_before,lrmsd_before_rank,lrmsd_after,lrmsd_after_rank,total_score,score_rank\n")
    for row in merged:
        out.write(",".join(str(x) for x in row) + "\n")
