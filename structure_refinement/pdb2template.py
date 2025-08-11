def adjust_pdb(input_pdb, output_pdb):
    """
    Adjust a PDB file based on the specified requirements:
    - Change chain A to chain H, chain B to chain L.
    - In chain C, change the chain name of the first residue PCA to 'P' without adjusting the residue number.
    - Remove all hydrogen atoms (H).
    - Change any HETATM to ATOM.
    - Change the last atom in chain C from NT GLY 9 to N NH2 10.
    - Reassign atom serial numbers after removing hydrogens.
    """
    with open(input_pdb, "r") as f:
        lines = f.readlines()

    adjusted_lines = []
    for line in lines:
        if line.startswith(("ATOM", "HETATM")):
            # Change HETATM to ATOM
            if line.startswith("HETATM"):
                line = "ATOM  " + line[6:]

            # Remove hydrogen atoms (atom_type is H)
            atom_name = line.strip()[-1]
            if atom_name.startswith("H"):
                continue

            # Remove OXT atoms
            if "OXT" in line:
                continue

            # Adjust chain names
            chain = line[21]
            if chain == "A":
                line = line[:21] + "H" + line[22:]
            elif chain == "B":
                line = line[:21] + "L" + line[22:]
            elif chain == "C":
                # Change PCA chain name to 'P'
                residue_name = line[17:20].strip()
                residue_number = line[22:26].strip()
                if residue_name == "PCA" and residue_number == "1":
                    line = line[:21] + "P" + line[22:]

            # Adjust the last atom in chain C
            if "NT  GLY" in line and line[21] == "C":
                line = line.replace("NT  GLY C   9", "N   NH2 C  10")

            adjusted_lines.append(line)
        else:
            adjusted_lines.append(line)

    # Reassign atom serial numbers
    atom_serial = 1
    renumbered_lines = []
    for line in adjusted_lines:
        if line.startswith("ATOM"):
            # Replace atom serial number (columns 6-11)
            line = line[:6] + f"{atom_serial:5d}" + line[11:]
            atom_serial += 1
        elif line.startswith("TER"):
            line = line[:5] + f"{atom_serial:5d}" + line[11:]
            atom_serial += 1  # Increment serial number for TER lines
        renumbered_lines.append(line)

    # Write the adjusted lines to the output file
    with open(output_pdb, "w") as f:
        f.writelines(renumbered_lines)

# Example usage

input_pdb = "./selection/T311_cycle19_seed114_seed_114_sample_4_0001.pdb"
output_pdb = "./selection/T311_cycle19_seed114_seed_114_sample_4.brk"
adjust_pdb(input_pdb, output_pdb)
print(f"Adjusted PDB file saved to {output_pdb}")