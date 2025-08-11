## Run Rosetta for scoring of protein-peptide binding with PTMs -PCA and -NH2


## installation
On grace hprc, load the software.
```
module load Rosetta/3.14-mpi
```

## usage
The steps are divided into structure refinement and structure ranking

### structure refinement
Use protenix generated .cif file to refine and merge
Filter the correct chirality (L) of PCA
```
python /structure_refinement/chirality.py
```

Convert to pdb file, and do modification so that terminated N is merged into last residue GLY and named as NT
```
python /structure_refinement/cif2pdb.py
```

Refine structure by Rosetta and extract energy

python structure_refinement/energy_extract.py

Convert generated pdb to targeted template .brk file
```
python /structure_refinement/pdb2template.py
```

### structure ranking

Extract models and filter the eligible models from the merged file
```
python structure_ranking/modelExtraction.py
```

Use Rosetta to calculate the energy score of each model
```
bash run.sh
```

Merge energy_score by Rosetta, confidence_score by Protenix, and cluster id.  And then sort all models

```
python structure_ranking/mergeScore.py
python structure_ranking/modelSorting.py
```

8VY4 validation
```
python structure_ranking/confidenceReadout.py
python structure_ranking/updating_iptm.py
python structure_ranking/merge_lrmsd_Value.py
python structure_ranking/statistics.py
```
