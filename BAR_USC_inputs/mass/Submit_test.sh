#! /bin/bash
#SBATCH --job-name=TESTING                     # Job name
#SBATCH --time 0:30:00
#SBATCH -p debug
#SBATCH -A bar
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks-per-node=36                    # Number of processors per node
#SBATCH --mail-user benjamin.anderson@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH -o slurm-%x-%j.log                      # Output

module purge
ml comp-intel mkl

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast test.fst
wait
