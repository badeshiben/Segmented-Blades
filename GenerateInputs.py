import numpy as np
import os
import pandas as pd
import fastlib
import weio
import pyFAST.case_generation.case_gen as case_gen
from create_studies import study1, study2, study3, study4


def genericStudy(study, ref_dir, work_dir, main_file):
    """ Generate OpenFAST inputs for segmented blade sensitivity study

    INPUTS:
       - study                            : dictionary containing:
            Param                         : Varied parameter name [str]
            WS                            : lists of wind speeds [m/s]
            RPM                           : list of RPMs
            pitch                         : list of pitches [deg]
            DTfvw                         : array of DTfvw
            nNWPanel                      : array of nNWPanel
            WakeLength                    : array of WakeLength
            WakeRegFactor                 : array of WakeRegFactor
            WingRegFactor                 : array of WingRegFactor
            CoreSpreadEddyVisc            : array of CoreSpreadEddyVisc
       - ref_dir                          : Folder where the fast input files are located (will be copied)
       - main_file                        : Main file in ref_dir, used as a template
       - work_dir                         : Output folder (will be created)


    This script uses a reference directory (`ref_dir`) which contains a reference input file (.fst)
    1) The reference directory is copied to a working directory (`work_dir`).
    2) All the fast input files are generated in this directory based on a list of dictionaries (`PARAMS`).
    For each dictionary in this list:
       - The keys are "path" to a input parameter, e.g. `EDFile|RotSpeed`  or `FAST|TMax`.
         These should correspond to the variables used in the FAST inputs files.
       - The values are the values corresponding to this parameter
    For instance:
         PARAMS[0]['EDFile|RotSpeed']       = 5
         PARAMS[0]['InflowFile|HWindSpeed'] = 10

    Optional:
        3) The simulations are run, successively distributed on `nCores` CPUs.
        4) The output files are read, and averaged based on a method (e.g. average over a set of periods,
            see averagePostPro in fastlib for the different averaging methods).
           A pandas DataFrame is returned
    """
    # --- The parameters we will change

    # --- Defining a "basic dictionary", all simulations will have these parameters
    BaseDict = {'TMax': 720, 'DT': 2e-4, 'DT_Out': 0.1}  # NOTE: for other parametric studies these could be parameters
    # --- Defining the parametric study, parameters that changes (list of dictionnaries with keys as FAST parameters)
    PARAMS=[]

    for i in range(0, study['num']):
        ed = study['EDmat'][:, :, i]
        bd = study['BDmat'][:, :, i]
        p = BaseDict.copy()
        p['EDFile|BldFile1|BldProp'] = study['EDmat'][:,:,i]
        p['BDBldFile(1)|BldFile|BeamProperties'] = study['BDmat'][:, :, i]
        p['BDBldFile(2)|BldFile|BeamProperties'] = study['BDmat'][:, :, i]
        p['BDBldFile(3)|BldFile|BeamProperties'] = study['BDmat'][:, :, i]
        p['__name__'] = study['parameter']+'{:.2f}'.format(study['values'][i])
        PARAMS.append(p)


    fastfiles = case_gen.templateReplace(PARAMS, ref_dir, outputDir=work_dir, removeRefSubFiles=True,
                                         main_file=main_file, oneSimPerDir=False)

    return fastfiles

def divide_chunks(l, n):
    """divides list l into chunks of length n"""
    for i in range(0, len(l), n):
        yield fastfiles[i:i + n]

def createSubmit(fastfiles, FAST_EXE, npf):
    """creates submission scripts from fast filenames and FAST_EXE path. Up to n files per script
    FAST_EXE: absolute path to FAST executable [str]
    fastfiles: list of FAST file names [str]
    npf: number of runs per submit script
    """
    nfiles = len(fastfiles)

    chunks = list(divide_chunks(fastfiles, npf))
    #one file per submit script
    for chunk in chunks:
        fname = chunk[0].replace(work_dir, '')
        name = fname[:-4]
        f = open(work_dir + "Submit_" + name + ".sh", "w")
        f.write('#! /bin/bash\n')
        f.write('#SBATCH --job-name=SegBlade                     # Job name\n')
        f.write('#SBATCH --time 16:00:00\n')
        f.write('#SBATCH -A bar\n')
        f.write('#SBATCH --nodes=1                               # Number of nodes\n')
        f.write('#SBATCH --ntasks-per-node=36                    # Number of processors per node\n')
        f.write('#SBATCH --mail-user benjamin.anderson@nrel.gov\n')
        f.write('#SBATCH --mail-type BEGIN,END,FAIL\n')
        f.write('#SBATCH -o slurm-%x-%j.log                      # Output\n')
        f.write('\n')
        f.write('module purge\n')
        f.write('ml conda comp-intel intel-mpi mkl\n')
        f.write('module unload gcc\n')
        f.write('\n')
        f.write(FAST_EXE + ' ' + fname + '\n')
        f.write('wait')
        f.close()

if __name__=='__main__':
    # --- "Global" Parameters for this script
    study = study4
    ref_dir          = 'BAR_USC_template/'  # Folder where the fast input files are located (will be copied)
    main_file        = 'BAR_USC.fst'    # Main file in ref_dir, used as a template
    work_dir         = 'BAR_USC_inputs/'+study['parameter']+'/'          # Output folder (will be created)
    FAST_EXE = '/home/banderso2/BAR/segmented_blades/openfast/build/glue-codes/openfast/openfast'
    npf = 1  # number of FAST runs per submission script
    # --- Generate inputs files
    fastfiles = genericStudy(study, ref_dir, work_dir, main_file)
    createSubmit(fastfiles, FAST_EXE, npf)




