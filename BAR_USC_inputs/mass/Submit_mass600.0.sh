#! /bin/bash
#SBATCH --job-name=FVWcheck                     # Job name
#SBATCH --time 16:00:00
#SBATCH -A bar
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks-per-node=36                    # Number of processors per node
#SBATCH --mail-user benjamin.anderson@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH -o slurm-%x-%j.log                      # Output

module purge
ml comp-intel mkl

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass600.0.fst
wait