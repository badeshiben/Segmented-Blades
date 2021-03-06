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

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass200.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass400.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass600.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass800.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1000.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1200.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1400.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1600.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1800.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass2000.00_DLC1.1_U4.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass200.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass400.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass600.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass800.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1000.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1200.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1400.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1600.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1800.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass2000.00_DLC1.1_U6.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass200.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass400.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass600.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass800.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1000.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1200.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1400.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1600.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1800.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass2000.00_DLC1.1_U8.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass200.00_DLC1.1_U10.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass400.00_DLC1.1_U10.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass600.00_DLC1.1_U10.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass800.00_DLC1.1_U10.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1000.00_DLC1.1_U10.fst &
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast mass1200.00_DLC1.1_U10.fst &
wait