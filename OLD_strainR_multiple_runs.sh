#!/bin/bash
#SBATCH --output=SR.out
#SBATCH --error=SR.err
#SBATCH --mem=64G
#SBATCH --partition=scavenger
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-use=kdm65@duke.edu
module load R/4.0.3-rhel8
module load BBMap/38.63
module load Jellyfish/2.3.0
module load samtools/1.11-rhel8
module load Git-LFS/2.9.2
cd test_IBD_strainR_5
mkdir results
for f in *_1.fastq.gz; \
do SAMPLE=${f%%_*}; \
FORWARD="/work/kdm65/test_IBD_strainR_5/${SAMPLE}_1.fastq.gz"; \
REVERSE="/work/kdm65/test_IBD_strainR_5/${SAMPLE}_2.fastq.gz"; \
Rscript /work/kdm65/StrainR/StrainR.R \
--forward ${FORWARD} \
--reverse ${REVERSE} \
--reference /work/kdm65/AmDB-apr2021 \
--threads 2 \
--mem 64 \
--outdir results \
--outprefix ${SAMPLE} \
; done
