import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fastlib
import weio
from create_studies import study1, study2, study3, study4, study5
import re
from prettyplotlib.utils import remove_chartjunk
import matplotlib.pylab as pl
import pyFAST.input_output as io
import fatpack
import textwrap

colors=pl.cm.tab20b(np.linspace(0,1,10))
plt.rc("font", family="serif")
plt.rc("font", size=8)
plt.rc("lines", lw=1)
plt.rc("lines", markersize=4)

""" PLOTTING MEAN QUANTITIES """
####################################################################################################################

def plot_sensitivity_raw(dfPlot, param, plot):
    """
    Parameters
    ----------
    dfPlot:     dataframe to plot
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    Plots raw max tip deflection, average power, BRMs, TBMs vs. varied parameter

    """
    ax1 = plt.subplot(311)  #, figsize=(8.5, 11))  # (6.4,4.8)
    color = 'tab:orange'
    ax1.plot(dfPlot[param], dfPlot['Tip Deflection'], '-o', color=color)  # output channel is something like 'TipTDxr' label='max out of plane blade tip deflection')
    ax1.grid()
    ax1.set_ylabel('Tip deflection [m]', color=color)
    ax1.tick_params(direction='in', axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.plot(dfPlot[param], dfPlot['Average Power']*8760/1e6, '-o', color=color)  # label='average power output [kW]')
    ax2.set_ylabel('Average power [kW]', color=color)
    ax2.tick_params(direction='in', axis='y', labelcolor=color)

    ax3 = plt.subplot(312)  #, figsize=(8.5, 11))
    ax3.grid()
    color = 'tab:green'
    label = 'Blade root flap moment DEL [kN-m]'
    label = textwrap.fill(label, width=20)
    ax3.plot(dfPlot[param], dfPlot['Blade root flap moment DEL']/1000, '-o', color=color)  # label='average power output [kW]')
    ax3.set_ylabel(label, color=color)
    ax3.tick_params(direction='in', axis='y', labelcolor=color)

    ax4 = ax3.twinx()
    color = 'tab:red'
    label = 'Blade root edge moment DEL [kN-m]'
    label = textwrap.fill(label, width=20)
    ax4.plot(dfPlot[param], dfPlot['Blade root edge moment DEL'] / 1000, '-o', color=color)  # label='average power output [kW]')
    ax4.set_ylabel(label, color=color)
    ax4.tick_params(direction='in', axis='y', labelcolor=color)

    ax5 = plt.subplot(313)  # , figsize=(8.5, 11))
    ax5.grid()
    color = 'tab:purple'
    label = 'Tower base fore-aft moment DEL [kN-m]'
    label = textwrap.fill(label, width=20)
    ax5.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o',
             color=color)  # label='average power output [kW]')
    ax5.set_ylabel(label, color=color)
    ax5.tick_params(direction='in', axis='y', labelcolor=color)

    ax6 = ax5.twinx()
    color = 'tab:gray'
    label = 'Tower base side-side moment DEL [kN-m]'
    label = textwrap.fill(label, width=20)
    ax6.plot(dfPlot[param], dfPlot['Tower base side-side moment DEL'] / 1000, '-o', color=color)  # label='average power output [kW]')
    ax6.set_ylabel(label, color=color)
    ax6.tick_params(direction='in', axis='y', labelcolor=color)

    if param == 'mass':
        ax5.set_xlabel('Joint ' + param + ' [kg]')
    elif param == 'location':
        ax5.set_xlabel('Joint ' + param + ' [span]')
    else:
        ax5.set_xlabel('Joint ' + param + ' multiplier')

    # ax4.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o', color=color)  # label='average power output [kW]')
    # ax4.set_ylabel('Tower base fore-aft moment DEL [kN-m]', color=color)
    # ax4.tick_params(direction='in', axis='y', labelcolor=color)


    remove_chartjunk(ax1, ['top', 'right'])
    # ax1.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/" + param+".pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def plot_sensitivity_norm_mass(dfPlot, param, plot):
    """
    Parameters
    ----------
    dfPlot:     dataframe to plot
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    Plots normalized max tip deflection, average power, BRMs, TBMs vs. varied parameter

    """
    fig, ax = plt.subplots(3, 1, sharey=False, sharex=True, figsize=(3, 5))
    # fig.set_size_inches(4, 10)# , figsize=(8.5, 11))  # (6.4,4.8)
    color = 'tab:orange'
    # ax[0].grid()
    ax[0].plot(dfPlot[param], dfPlot['Tip Deflection']/dfPlot['Tip Deflection'][0], '-o',
             color=color)  # output channel is something like 'TipTDxr' label='max out of plane blade tip deflection')
    ax[0].grid()
    ax[0].set_ylabel('Tip deflection', color=color)
    ax[0].set_ylim(0.905, 1.005)
    ax[0].tick_params(direction='in', axis='y', labelcolor=color)

    ax2 = ax[0].twinx()
    ax2.axes.yaxis.set_visible(False)
    # color = 'tab:blue'
    # ax2.plot(dfPlot[param], dfPlot['Average Power']/dfPlot['Average Power'][0], '-o',
    #          color=color)  # label='average power output [kW]')
    # ax2.set_ylabel('AEP', color=color)
    # ax2.tick_params(direction='in', axis='y', labelcolor=color)

    ax[1].grid()
    color = 'tab:green'
    label = 'Blade root flap moment DEL'
    label = textwrap.fill(label, width=20)
    ax[1].plot(dfPlot[param], dfPlot['Blade root flap moment DEL']/dfPlot['Blade root flap moment DEL'][0], '-o',
               color=color)
    ax[1].set_ylabel(label, color=color)
    ax[1].set_ylim(0.995, 1.095)
    ax[1].tick_params(direction='in', axis='y', labelcolor=color)

    ax3 = ax[1].twinx()
    color = 'tab:red'
    label = 'Blade root edge moment DEL'
    label = textwrap.fill(label, width=20)
    ax3.plot(dfPlot[param], dfPlot['Blade root edge moment DEL']/dfPlot['Blade root edge moment DEL'][0], '-o',
             color=color)  # label='average power output [kW]')
    ax3.set_ylabel(label, color=color)
    ax3.set_ylim(0.995, 1.095)
    ax3.tick_params(direction='in', axis='y', labelcolor=color)

    ax[2].grid()
    color = 'tab:purple'
    label = 'Tower base fore-aft moment DEL'
    label = textwrap.fill(label, width=20)
    ax[2].plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL']/dfPlot['Tower base fore-aft moment DEL'][0], '-o',
               color=color)  # label='average power output [kW]')
    ax[2].set_ylabel(label, color=color)
    ax[2].set_ylim(0.995, 1.095)
    ax[2].tick_params(direction='in', axis='y', labelcolor=color)

    ax6 = ax[2].twinx()
    color = 'tab:gray'
    label = 'Tower base side-side moment DEL'
    label = textwrap.fill(label, width=20)
    ax6.plot(dfPlot[param], dfPlot['Tower base side-side moment DEL']/dfPlot['Tower base side-side moment DEL'][0], '-o',
             color=color)  # label='average power output [kW]')
    ax6.set_ylabel(label, color=color)
    ax6.set_ylim(0.905, 1.005)
    ax6.tick_params(direction='in', axis='y', labelcolor=color)


    if param == 'mass':
        ax[2].set_xlabel('Joint ' + param + ' [kg]')
    elif param == 'location':
        ax[2].set_xlabel('Joint ' + param + ' [span]')
    else:
        ax[2].set_xlabel('Joint ' + param + ' multiplier')

    # ax4.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o', color=color)  # label='average power output [kW]')
    # ax4.set_ylabel('Tower base fore-aft moment DEL [kN-m]', color=color)
    # ax4.tick_params(direction='in', axis='y', labelcolor=color)

    remove_chartjunk(ax[0], ['top', 'right'])
    # ax1.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/normalized/" + param + "_norm.pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def plot_sensitivity_norm_stiffness(dfPlot, param, plot):
    """
    Parameters
    ----------
    dfPlot:     dataframe to plot
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    Plots normalized max tip deflection, average power, BRMs, TBMs vs. varied parameter

    """
    fig, ax = plt.subplots(2, 1, sharey=False, sharex=True, figsize=(3, 3.4))
    # fig.set_size_inches(4, 10)# , figsize=(8.5, 11))  # (6.4,4.8)
    color = 'tab:orange'
    ax[0].plot(dfPlot[param], dfPlot['Tip Deflection']/dfPlot['Tip Deflection'][0], '-o',
             color=color)  # output channel is something like 'TipTDxr' label='max out of plane blade tip deflection')
    ax[0].grid()
    ax[0].set_ylabel('Tip deflection', color=color)
    ax[0].set_ylim(0.905, 1.005)
    ax[0].tick_params(direction='in', axis='y', labelcolor=color)

    # ax2 = ax[0].twinx()
    # color = 'tab:blue'
    # ax2.plot(dfPlot[param], dfPlot['Average Power']/dfPlot['Average Power'][0], '-o',
    #          color=color)  # label='average power output [kW]')
    # ax2.set_ylabel('AEP', color=color)
    # ax2.tick_params(direction='in', axis='y', labelcolor=color)

    ax2 = ax[0].twinx()
    color = 'tab:green'
    label = 'Blade root flap moment DEL'
    label = textwrap.fill(label, width=20)
    ax2.plot(dfPlot[param], dfPlot['Blade root flap moment DEL']/dfPlot['Blade root flap moment DEL'][0], '-o',
               color=color)
    ax2.set_ylabel(label, color=color)
    ax2.set_ylim(0.995, 1.095)
    ax2.tick_params(direction='in', axis='y', labelcolor=color)

    # ax3 = ax[1].twinx()
    # color = 'tab:red'
    # label = 'Blade root edge moment DEL'
    # label = textwrap.fill(label, width=20)
    # ax3.plot(dfPlot[param], dfPlot['Blade root edge moment DEL']/dfPlot['Blade root edge moment DEL'][0], '-o',
    #          color=color)  # label='average power output [kW]')
    # ax3.set_ylabel(label, color=color)
    # ax3.set_ylim(0.995, 1.095)
    # ax3.tick_params(direction='in', axis='y', labelcolor=color)

    ax[1].grid()
    color = 'tab:purple'
    label = 'Tower base fore-aft moment DEL'
    label = textwrap.fill(label, width=20)
    ax[1].plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL']/dfPlot['Tower base fore-aft moment DEL'][0], '-o',
               color=color)  # label='average power output [kW]')
    ax[1].set_ylabel(label, color=color)
    ax[1].set_ylim(0.995, 1.095)
    ax[1].tick_params(direction='in', axis='y', labelcolor=color)

    ax6 = ax[1].twinx()
    color = 'tab:gray'
    label = 'Tower base side-side moment DEL'
    label = textwrap.fill(label, width=20)
    ax6.plot(dfPlot[param], dfPlot['Tower base side-side moment DEL']/dfPlot['Tower base side-side moment DEL'][0], '-o',
             color=color)  # label='average power output [kW]')
    ax6.set_ylabel(label, color=color)
    ax6.set_ylim(0.995, 1.095)
    ax6.tick_params(direction='in', axis='y', labelcolor=color)
    ax[1].set_xlabel('Joint ' + param + ' multiplier')

    # ax4.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o', color=color)  # label='average power output [kW]')
    # ax4.set_ylabel('Tower base fore-aft moment DEL [kN-m]', color=color)
    # ax4.tick_params(direction='in', axis='y', labelcolor=color)

    remove_chartjunk(ax[0], ['top', 'right'])
    # ax1.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/normalized/" + param + "_norm.pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def plot_sensitivity_norm_location(dfPlot, param, plot):
    """
    Parameters
    ----------
    dfPlot:     dataframe to plot
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    Plots normalized max tip deflection, average power, BRMs, TBMs vs. varied parameter

    """
    fig, ax = plt.subplots(3, 1, sharey=False, sharex=True, figsize=(3, 5))
    # fig.set_size_inches(4, 10)# , figsize=(8.5, 11))  # (6.4,4.8)
    color = 'tab:orange'
    ax[0].plot(dfPlot[param], dfPlot['Tip Deflection'] / dfPlot['Tip Deflection'][0], '-o',
               color=color)  # output channel is something like 'TipTDxr' label='max out of plane blade tip deflection')
    ax[0].grid()
    ax[0].set_ylabel('Tip deflection', color=color)
    ax[0].set_ylim(0.92, 1.02)
    ax[0].tick_params(direction='in', axis='y', labelcolor=color)

    ax2 = ax[0].twinx()
    ax2.axes.yaxis.set_visible(False)
    # color = 'tab:blue'
    # ax2.plot(dfPlot[param], dfPlot['Average Power']/dfPlot['Average Power'][0], '-o',
    #          color=color)  # label='average power output [kW]')
    # ax2.set_ylabel('AEP', color=color)
    # ax2.tick_params(direction='in', axis='y', labelcolor=color)

    ax[1].grid()
    color = 'tab:green'
    label = 'Blade root flap moment DEL'
    label = textwrap.fill(label, width=20)
    ax[1].plot(dfPlot[param], dfPlot['Blade root flap moment DEL'] / dfPlot['Blade root flap moment DEL'][0],
               '-o',
               color=color)
    ax[1].set_ylabel(label, color=color)
    ax[1].set_ylim(0.96, 1.06)
    ax[1].tick_params(direction='in', axis='y', labelcolor=color)
    # ax[1].xticks([0.96, 0.98, 1.00, 1.02, 1.04])

    ax3 = ax[1].twinx()
    color = 'tab:red'
    label = 'Blade root edge moment DEL'
    label = textwrap.fill(label, width=20)
    ax3.plot(dfPlot[param], dfPlot['Blade root edge moment DEL'] / dfPlot['Blade root edge moment DEL'][0],
             '-o',
             color=color)  # label='average power output [kW]')
    ax3.set_ylabel(label, color=color)
    ax3.set_ylim(0.96, 1.06)
    ax3.tick_params(direction='in', axis='y', labelcolor=color)

    ax[2].grid()
    color = 'tab:purple'
    label = 'Tower base fore-aft moment DEL'
    label = textwrap.fill(label, width=20)
    ax[2].plot(dfPlot[param],
               dfPlot['Tower base fore-aft moment DEL'] / dfPlot['Tower base fore-aft moment DEL'][0], '-o',
               color=color)  # label='average power output [kW]')
    ax[2].set_ylabel(label, color=color)
    ax[2].set_ylim(0.985, 1.095)
    ax[2].tick_params(direction='in', axis='y', labelcolor=color)

    ax6 = ax[2].twinx()
    color = 'tab:gray'
    label = 'Tower base side-side moment DEL'
    label = textwrap.fill(label, width=20)
    ax6.plot(dfPlot[param],
             dfPlot['Tower base side-side moment DEL'] / dfPlot['Tower base side-side moment DEL'][0], '-o',
             color=color)  # label='average power output [kW]')
    ax6.set_ylabel(label, color=color)
    ax6.set_ylim(0.985, 1.095)
    ax6.tick_params(direction='in', axis='y', labelcolor=color)

    if param == 'mass':
        ax[2].set_xlabel('Joint ' + param + ' [kg]')
    elif param == 'location':
        ax[2].set_xlabel('Joint ' + param + ' [span]')
    else:
        ax[2].set_xlabel('Joint ' + param + ' multiplier')

    # ax4.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o', color=color)  # label='average power output [kW]')
    # ax4.set_ylabel('Tower base fore-aft moment DEL [kN-m]', color=color)
    # ax4.tick_params(direction='in', axis='y', labelcolor=color)

    remove_chartjunk(ax[0], ['top', 'right'])
    # ax1.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/normalized/" + param + "_norm.pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def prob_WindDist(turbine_class, windspeed, disttype="pdf"):
    """
    Generates the probability of a windspeed given the cumulative
    distribution or probability density function of a Weibull distribution
    per IEC 61400.
    NOTE: This uses the range of wind speeds simulated over, so if the
    simulated wind speed range is not indicative of operation range, using
    this cdf to calculate AEP is invalid
    Parameters
    ----------
    windspeed : float or list-like
        wind speed(s) to calculate probability of
    disttype : str, optional
        type of probability, currently supports CDF or PDF
    Returns
    -------
    p_bin : list
        list containing probabilities per wind speed bin
    """

    if turbine_class in [1, "I"]:
        Vavg = 50 * 0.2

    elif turbine_class in [2, "II"]:
        Vavg = 42.5 * 0.2

    elif turbine_class in [3, "III"]:
        Vavg = 37.5 * 0.2

    # Define parameters
    k = 2  # Weibull shape parameter
    c = (2 * Vavg) / np.sqrt(np.pi)  # Weibull scale parameter

    if disttype.lower() == "cdf":
        # Calculate probability of wind speed based on WeibulCDF
        wind_prob = 1 - np.exp(-(windspeed / c) ** k)

    elif disttype.lower() == "pdf":
        # Calculate probability of wind speed based on WeibulPDF
        wind_prob = (
                (k / c)
                * (windspeed / c) ** (k - 1)
                * np.exp(-(windspeed / c) ** k)
        )

    else:
        raise ValueError(
            f"The {disttype} probability distribution type is invalid"
        )

    return wind_prob

def compute_del(ts, slope, elapsed, **kwargs):
    """
    Computes damage equivalent load of input `ts`.
    Parameters
    ----------
    ts : np.array
        Time series to calculate DEL for.
    slope : int | float
        Slope of the fatigue curve.
    elapsed : int | float
        Elapsed time of the time series.
    rainflow_bins : int
        Number of bins used in rainflow analysis.
        Default: 100
    """

    bins = kwargs.get("rainflow_bins", 100)

    ranges = fatpack.find_rainflow_ranges(ts)
    Nrf, Srf = fatpack.find_range_count(ranges, 100)
    DELs = Srf ** slope * Nrf / elapsed
    DEL = DELs.sum() ** (1 / slope)

    return DEL

""" RUN RESOLUTION STUDY """
def run_study(param, values, DLCs):
    """ run a sensitivity study on segmentation joint parameters (mass, inertia, stiffness)
    Parameters
    ----------
    param:                 parameter varied, [str] (mass, inertia, stiffness)
    values:                list of values of parameter [1D list]
    DLCs:                   1D list of DLCs run [str]
    Returns
    -------
    plots of tip deflection, blade root moment, and power production sensitivity to parameter variation.
    """
    DLC11 = DLCs[:-1]
    cwd = os.getcwd()
    work_dir = 'BAR_USC_inputs/' + param + '/'
    postpro_dir = './PostPro/'  # + param + '/'
    # create csvs
    if not os.path.isdir(cwd + postpro_dir[1:]):
        os.mkdir(cwd + postpro_dir[1:])

    # find average power output at rated conditions
    pwr = np.empty([len(DLC11), len(values)])  #[DLC1.1 x Values] array. kinda hacky, but can't use DLC 1.3 for this. Sorry.
    DEL_TBMy = np.empty([len(DLC11), len(values)])
    DEL_TBMx = np.empty([len(DLC11), len(values)])
    DEL_BRMy = np.empty([len(DLC11), len(values)])
    DEL_BRMx = np.empty([len(DLC11), len(values)])
    i = 0
    for val in values:
        Files = []
        j = 0
        for DLC in DLC11:
            case     =param+'{:.2f}'.format(val)+'_DLC'+DLC
            filename = os.path.join(work_dir, case + '.outb')
            Files.append(filename)
            tsDf = io.fast_output_file.FASTOutputFile(filename).toDataFrame()
            tsDf = tsDf[['TwrBsMxt_[kN-m]', 'TwrBsMyt_[kN-m]', 'B1RootMyr_[N-m]', 'B1RootMxr_[N-m]']]
            ts = tsDf.to_numpy()
            ts = ts[1000:, :]
            DEL_TBMx[j, i] = compute_del(ts[:, 0], 3, 600)
            DEL_TBMy[j, i] = compute_del(ts[:, 1], 3, 600)
            DEL_BRMy[j, i] = compute_del(ts[:, 2], 3, 600)
            DEL_BRMx[j, i] = compute_del(ts[:, 3], 3, 600)
            j += 1
        print(Files)
        avgDf = fastlib.averagePostPro(Files, avgMethod='constantwindow', avgParam=None)
        avgDf = avgDf['GenPwr_[kW]']
        pwr[:, i] = avgDf.to_numpy()
        i += 1
    wind_prob = prob_WindDist(3, [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25])
    cum = sum(wind_prob)
    avgPwr = np.matmul(wind_prob, pwr)
    avg_DEL_TBMy = np.matmul(wind_prob, DEL_TBMy)
    avg_DEL_TBMx = np.matmul(wind_prob, DEL_TBMx)
    avg_DEL_BRMy = np.matmul(wind_prob, DEL_BRMy)
    avg_DEL_BRMx = np.matmul(wind_prob, DEL_BRMx)

    # find extreme out of plane tip deflection in extreme conditions
    maxTipDefl=[]
    for val in values:
        case     =param+'{:.2f}'.format(val)+'_DLC1.3_U23'
        filename = os.path.join(work_dir, case + '.outb')
        dfTs = weio.FASTOutFile(filename).toDataFrame()
        tipDeflection1 = dfTs['B1TipTDxr_[m]']
        tipDeflection2 = dfTs['B2TipTDxr_[m]']
        tipDeflection3 = dfTs['B3TipTDxr_[m]']
        maxTipDefl.append(min(min(tipDeflection1), min(tipDeflection2), min(tipDeflection3)))
    dfPlot = pd.DataFrame() #data=pwr, index=DLCs[:-2])
    dfPlot[param] = values
    dfPlot['Tip Deflection'] = maxTipDefl
    dfPlot['Average Power'] = avgPwr
    dfPlot['Blade root flap moment DEL'] = avg_DEL_BRMy
    dfPlot['Blade root edge moment DEL'] = avg_DEL_BRMx
    dfPlot['Tower base fore-aft moment DEL'] = avg_DEL_TBMy
    dfPlot['Tower base side-side moment DEL'] = avg_DEL_TBMx

    # plot_sensitivity_raw(dfPlot, param, 1)
    plot_sensitivity_norm_location(dfPlot, param, 2)

if __name__ == "__main__":


    # study = study2
    # run_study(param=study['parameter'], values=study['values'], DLCs=study['DLC'])
    # study = study1
    # run_study(param=study['parameter'], values=study['values'], DLCs=study['DLC'])
    # study = study3
    # run_study(param=study['parameter'], values=study['values'], DLCs=study['DLC'])
    study = study4
    run_study(param=study['parameter'], values=study['values'], DLCs=study['DLC'])





