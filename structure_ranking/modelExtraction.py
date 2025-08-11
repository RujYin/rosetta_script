# Extract all the T311 model and check the eligibility of them

import os
from collections import defaultdict
import csv

input_pdb = "Target311.pdb"
output_dir = "checked_models"
abnormal_dir = os.path.join(output_dir, "abnormal")
normal_dir = os.path.join(output_dir, "normal")

os.makedirs(abnormal_dir, exist_ok=True)
os.makedirs(normal_dir, exist_ok=True)

def count_unique_residues(lines):
    """Return count of unique (chain, res_id) from ATOM/HETATM lines."""
    residues = set()
    for line in lines:
        if line.startswith(("ATOM", "HETATM")):
            chain = line[21]
            resseq = line[22:26].strip()
            resname = line[17:20].strip()
            residues.add((chain, resseq, resname))
    return residues

def extract_chain(lines, target_chain_ids):
    return [l for l in lines if l.startswith(("ATOM", "HETATM")) and l[21] in target_chain_ids]

def fix_chain_C_residues(lines):
    """Fix chain P→C, rename NH2→GLY NT at res_id=10 → res_id=9, and sort by res_id."""
    residue_atoms = defaultdict(list)
    for line in lines:
        if not line.startswith(("ATOM", "HETATM")):
            continue

        chain_id = line[21]
        resname = line[17:20].strip()
        resseq = int(line[22:26].strip())

        # Force chain ID to C
        if chain_id == 'P':
            line = line[:21] + 'C' + line[22:]
            chain_id = 'C'

        # NH2 → GLY with NT atom and res_id 9
        if resname == "NH2" and resseq == 10:
            line = line[:12] + " NT " + line[16:]
            line = line[:17] + "GLY" + line[20:]
            line = line[:22] + "   9" + line[26:]
            resseq = 9  # For sorting

        residue_atoms[resseq].append(line)

    # Sort by residue ID and flatten
    sorted_lines = []
    for res_id in sorted(residue_atoms):
        sorted_lines.extend(residue_atoms[res_id])

    # Count unique residues
    unique_residues = {int(rid) for rid in residue_atoms}
    return sorted_lines, len(unique_residues)

abnormal_log = []
def reorder_and_fix_model(model_lines, model_index):
    """Reorder chains H→L→C, fix C chain and verify residue counts."""
    chains = {"H": [], "L": [], "C": [], "P": []}
    others = []

    for line in model_lines:
        if line.startswith(("ATOM", "HETATM")):
            chain_id = line[21]
            if chain_id in chains:
                chains[chain_id].append(line)
            else:
                others.append(line)
        elif not line.startswith("MODEL") and not line.startswith("ENDMDL"):
            others.append(line)

    # Fix chain C
    chain_c_raw = chains["C"] + chains["P"]
    chain_c_fixed, c_res_count = fix_chain_C_residues(chain_c_raw)

    # Count H/L residues
    h_residues = count_unique_residues(chains["H"])
    l_residues = count_unique_residues(chains["L"])
    h_count = len(h_residues)
    l_count = len(l_residues)

    # Check abnormal
    is_abnormal = (
        c_res_count != 9 or
        h_count != 224 or
        l_count != 219
    )

    # Write final output
    output = []
    output.append(f"MODEL     {model_index}\n")
    if chains["H"]:
        output.extend(chains["H"])
        output.append("TER\n")
    if chains["L"]:
        output.extend(chains["L"])
        output.append("TER\n")
    if chain_c_fixed:
        output.extend(chain_c_fixed)
        output.append("TER\n")
    output.append("ENDMDL\n")

    return output, is_abnormal, c_res_count, h_count, l_count

# Process models
with open(input_pdb, 'r') as infile:
    model_lines = []
    model_index = 0
    inside_model = False

    for line in infile:
        if line.startswith("MODEL"):
            inside_model = True
            model_lines = [line]
        elif line.startswith("ENDMDL"):
            model_lines.append(line)
            

            rewritten, is_abnormal, c_count, h_count, l_count = reorder_and_fix_model(model_lines, model_index)

            fname = f"Target311_model{model_index:04d}.pdb"
            out_path = os.path.join(abnormal_dir if is_abnormal else normal_dir, fname)
            with open(out_path, 'w') as out:
                out.writelines(rewritten)

            if is_abnormal:
                abnormal_log.append((f"Target311_model{model_index:04d}", c_count, h_count, l_count))

            inside_model = False

            model_index += 1
        elif inside_model:
            model_lines.append(line)

# Save abnormal list to CSV
with open(os.path.join(output_dir, "abnormal_models.csv"), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["model", "C_residue_count", "H_residue_count", "L_residue_count"])
    writer.writerows(abnormal_log)

print("✅ Rewriting complete.")
print(f"→ Normal models saved in: {normal_dir}")
print(f"→ Abnormal models saved in: {abnormal_dir}")
print(f"→ Abnormal model summary: {os.path.join(output_dir, 'abnormal_models.csv')}")