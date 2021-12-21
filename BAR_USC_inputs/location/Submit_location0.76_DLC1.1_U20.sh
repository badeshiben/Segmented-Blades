#! /bin/bash
#SBATCH --job-name=SegBlade                     # Job name
#SBATCH --time 16:00:00
#SBATCH -A bar
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks-per-node=36                    # Number of processors per node
#SBATCH --mail-user benjamin.anderson@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH -o slurm-%x-%j.log                      # Output

module purge
ml conda comp-intel intel-mpi mkl
module unload gcc

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.76_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.79_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.21_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.24_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.28_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.31_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.34_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.38_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.41_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.45_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.48_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.52_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.55_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.59_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.62_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.66_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.69_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.72_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.76_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.79_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.21_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.24_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.28_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.31_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.34_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.38_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.41_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.45_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.48_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.52_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.55_DLC1.1_U24.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast location0.59_DLC1.1_U24.fst
&
wait