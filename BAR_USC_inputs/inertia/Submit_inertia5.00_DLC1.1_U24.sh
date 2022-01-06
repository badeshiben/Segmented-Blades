#! /bin/bash
#SBATCH --job-name=SegBlade                     # Job name
#SBATCH --time 12:00:00
#SBATCH -A bar
#SBATCH -p standard
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks-per-node=36                    # Number of processors per node
#SBATCH --mail-user benjamin.anderson@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH -o slurm-%x-%j.log                      # Output

module purge
ml conda comp-intel intel-mpi mkl
module unload gcc

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.00_DLC1.1_U24.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.50_DLC1.1_U24.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia1.00_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia1.50_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia2.00_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia2.50_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia3.00_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia3.50_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia4.00_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia4.50_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.00_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.50_DLC1.1_U25.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia1.00_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia1.50_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia2.00_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia2.50_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia3.00_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia3.50_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia4.00_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia4.50_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.00_DLC1.3_U23.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast inertia5.50_DLC1.3_U23.fst &
wait