#!/bin/bash
#SBATCH --output=SR.out
#SBATCH --error=SR.err
#SBATCH --mem=32G
#SBATCH --partition=scavenger
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-use=kdm65@duke.edu
singularity exec \
--home /work/kdm65/:/home \
smeg.sif smeg growth_est \
-o smeg_results \
-r IBDMDB_metagenomics_1plus/forward_reads \
-s AkkBigger_SMEG/F.0.9 \
-p 6 -e -x fastq.gz
