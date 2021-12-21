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

/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness1.50_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.00_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.50_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.00_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.50_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness4.00_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness4.50_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness5.00_DLC1.1_U18.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.20_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.40_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.60_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.80_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness1.00_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness1.50_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.00_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.50_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.00_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.50_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness4.00_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness4.50_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness5.00_DLC1.1_U20.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.20_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.40_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.60_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness0.80_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness1.00_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness1.50_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.00_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness2.50_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.00_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness3.50_DLC1.1_U22.fst
&
/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast stiffness4.00_DLC1.1_U22.fst
&
wait