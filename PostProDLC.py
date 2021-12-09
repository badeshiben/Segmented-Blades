import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fastlib
import weio
from create_studies import study1, study2, study3, study4
import re
from prettyplotlib.utils import remove_chartjunk
import matplotlib.pylab as pl


colors=pl.cm.tab20b(np.linspace(0,1,10))
plt.rc("font",family="serif")
plt.rc("font",size=14)

""" PLOTTING MEAN QUANTITIES """
####################################################################################################################

def plot_sensitivity(dfPlot, param, plot):
    """
    Parameters
    ----------
    dfPlot:     dataframe to plot
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    Plots max tip deflection and average power vs. varied parameter

    """
    fig, ax1 = plt.subplots(1, figsize=(8.5, 11))  # (6.4,4.8)
    color = 'tab:red'
    ax1.plot(dfPlot[param], dfPlot['Deflection'], '-o', color=color)  #, output channel is something like 'TipTDxr' label='max out of plane blade tip deflection')
    ax1.grid()
    if param == 'mass':
        ax1.set_xlabel('Joint ' + param + ' [kg]')
    elif param == 'location':
        ax1.set_xlabel('Joint ' + param + ' [span]')
    else:
        ax1.set_xlabel('Joint ' + param + ' multiplier')
    ax1.set_ylabel('Tip deflection [m]', color=color)
    ax1.tick_params(direction='in', axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.plot(dfPlot[param], dfPlot['GenPwr_[kW]'], '-o', color=color) #, label='average power output [kW]')
    ax2.set_ylabel('Average power [kW]', color=color)
    ax2.tick_params(direction='in', axis='y', labelcolor=color)

    remove_chartjunk(ax1, ['top', 'right'])
    # ax1.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/" + param+".pdf"
        plt.savefig(plot_name, bbox_inches='tight')



""" RUN RESOLUTION STUDY """
def run_study(param, values):
    """ run a sensitivity study on segmentation joint parameters (mass, inertia, stiffness)
    Parameters
    ----------
    param:                 parameter varied, [str] (mass, inertia, stiffness)
    values:                list of values of parameter [1D list]
    DLC:                   1D list of DLCs run [str]
    Returns
    -------
    plots of tip deflection, blade root moment, and power production sensitivity to parameter variation.
    """
    cwd = os.getcwd()
    work_dir = 'BAR_USC_inputs/' + param + '/'
    postpro_dir = './PostPro/'  # + param + '/'
    # create csvs
    if not os.path.isdir(cwd + postpro_dir[1:]):
        os.mkdir(cwd + postpro_dir[1:])
    # find average power output at rated conditions
    ratedFiles=[]
    for val in values:
        for DLC in DLCs:
            case     =param+'{:.2f}'.format(val)+'DLC'+DLC
            filename = os.path.join(work_dir, case + '.outb')
            ratedFiles.append(filename)
    print(ratedFiles)
    dfAvg = fastlib.averagePostPro(ratedFiles, avgMethod='constantwindow', avgParam=None, ColMap={'WS_[m/s]':'Wind1VelX_[m/s]'})
    dfAvg.insert(0, param, values)
    dfPlot=dfAvg[[param, 'GenPwr_[kW]']]

    # find extreme out of plane tip deflection in extreme conditions
    maxTipDefl=[]
    for val in values:
        case     =param+'{:.2f}'.format(val)+'DLC1.3_U23'
        filename = os.path.join(work_dir, case + '.outb')
        dfTs = weio.FASTOutFile(filename).toDataFrame()
        tipDeflection1 = dfTs['B1TipTDxr_[m]']
        tipDeflection2 = dfTs['B2TipTDxr_[m]']
        tipDeflection3 = dfTs['B3TipTDxr_[m]']
        maxTipDefl.append(max(max(tipDeflection1), max(tipDeflection1), max(tipDeflection1)))
        #header = dfTs.head()
    dfPlot['Deflection'] = maxTipDefl


    plot_sensitivity(dfPlot, param, 2)

if __name__ == "__main__":

    study = study3
    run_study(param=study['parameter'], values=study['values'], DLCs=study['DLC'])





