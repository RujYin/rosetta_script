#!/bin/bash
##module load GCC/13.2.0 OpenMPI/4.1.6 Rosetta/3.14-mpi
cif_dir="/scratch/user/yihaoy/NH2/checked_models/normal"
#output_dir="/scratch/user/yihaoy/NH2/checked_models/output"
#    -flexPepDocking:flexpep_score_only -ex1 -ex2aro -use_input_sc \
output_dir="/scratch/user/yihaoy/NH2/checked_models/refine_output"
pdb_files=("${cif_dir}"/*.pdb)
total=${#pdb_files[@]}
count=0

for pdb_file in "${pdb_files[@]}"; do
    ((count++))
    cif_path="${pdb_file%.pdb}"
    name="$(basename "${cif_path}")"
    percent=$((count * 100 / total))
    echo "Processing: $name.pdb ($count/$total, ${percent}%)"
    FlexPepDocking.mpi.linuxgccrelease -database /sw/eb/sw/Rosetta/3.14-foss-2023b-mpi/database/ \
    -s "${cif_path}.pdb" -overwrite \
    -flexPepDocking:receptor_chain HL \
    -flexPepDocking:peptide_chain C \
    -in:file:extra_res_fa PCA.params \
    -flexPepDocking:pep_refine -ex1 -ex2aro -use_input_sc \
    -score:weights ref2015 -out:path:all "${output_dir}"
done
