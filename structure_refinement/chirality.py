# determine the chiraty (L or D) of generated PCA structure


from Bio.PDB import MMCIFParser
import numpy as np
import argparse

def get_chirality(v1, v2, v3):
    return np.sign(np.dot(np.cross(v1, v2), v3))

def is_L_amino_acid(residue):
    try:
        ca = residue['CA'].get_vector()
        n  = residue['N'].get_vector()
        c  = residue['C'].get_vector()
        cb = residue['CB'].get_vector()
    except KeyError:
        return None  # Missing atoms (e.g., glycine or incomplete structure)

    v1 = n - ca
    v2 = c - ca
    v3 = cb - ca
    chiral_sign = get_chirality(v1.get_array(), v2.get_array(), v3.get_array())
    return 'L' if chiral_sign > 0 else 'D'


if __name__ == "__main__":

    parser_arg = argparse.ArgumentParser(description="Check chirality of residue 1 in chain C of a mmCIF file.")
    parser_arg.add_argument("cif_file", help="Path to the mmCIF file")
    args = parser_arg.parse_args()

    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("protein", args.cif_file)

    for model in structure:
        chain = model['C']
        for residue in chain:
            if residue.id[1] == 1:
                result = is_L_amino_acid(residue)
                if result is None:
                    print("Residue 1 in chain C is glycine or incomplete.")
                else:
                    print(f"Residue 1 in chain C is a {result}-amino acid.")
                break
        
        chain = model['A']
        for residue in chain:
            if residue.id[1] == 1:
                result = is_L_amino_acid(residue)
                if result is None:
                    print("Residue 1 in chain A is glycine or incomplete.")
                else:
                    print(f"Residue 1 in chain A is a {result}-amino acid.")
                break