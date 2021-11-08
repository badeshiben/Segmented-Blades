import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fastlib
import weio
from create_studies import study1, study2, study3, study4, study5, study6
import re
from prettyplotlib.utils import remove_chartjunk
import matplotlib.pylab as pl


colors=pl.cm.tab20b(np.linspace(0,1,10))
plt.rc("font",family="serif")
plt.rc("font",size=14)

""" PLOTTING MEAN QUANTITIES """
####################################################################################################################
""" SIMULATION TIME"""
def calc_sim_times(paramfull, plot):
    """calculate and plot simulation times for each run"""
    param = paramfull.split('_', 1)[0]
    timefile = './BAR_02_discretization_inputs/'+param+'/times.txt'
    runsfile = './BAR_02_discretization_inputs/'+param+'/runs.txt'
    CPU_hrs = []
    ws = []
    val = []
    dr = 3.448147165807185
    """extract values to plot"""
    data = pd.read_csv(timefile, delimiter=r"\s+", header=None)
    data.columns = ['fname','-','-','-','time','unit']
    for row in data.iterrows():
            if row[1]['unit'] == 'minutes':
                    CPU_hrs = CPU_hrs + [row[1]['time']/60]
            elif row[1]['unit'] == 'hours':
                    CPU_hrs = CPU_hrs + [row[1]['time']]
            elif row[1]['unit'] == 'days':
                    CPU_hrs = CPU_hrs + [row[1]['time']*24]
    runs = pd.read_csv(runsfile, delimiter=r"\s+", header=None)
    runs = runs.iloc[:, -1]
    for run in runs:
            numbers = re.findall(r'\d+(?:\.\d+)?', run)
            ws += [int(numbers[0])]
            val += [float(numbers[1])]
    ws = np.array(ws)
    wsuq = np.unique(ws)
    RPM = np.array([4, 5.5, 7.5, 7.84, 7.85])

    """plot stuff"""
    fig, ax = plt.subplots(1, figsize=(8.5, 11))
    for w in wsuq:
            wi = np.where(wsuq==w)
            color_index = wi[0][0]*2+1
            RPMi = RPM[wi]
            idxs = np.where(ws==w)[0]
            idxs = idxs.tolist()
            CPU_hrs_i = [CPU_hrs[i] for i in idxs]
            val_i = [val[i] for i in idxs]
            val_i = np.asarray(val_i)
            if paramfull == 'nNWPanel_[-]':
                val_i.sort()
                CPU_hrs_i.sort()
            if paramfull == 'DTfvw_[s]':
                ax.plot(val_i * RPMi * 6, CPU_hrs_i, '-o', color=colors[color_index], label='WS = {:}'.format(w))
            elif paramfull == 'nNWPanel_[-]':
                ax.plot(val_i*5, CPU_hrs_i, '-o', color=colors[color_index], label='WS = {:}'.format(w))  # TODO asssume dpsi_cvg=5deg
            elif paramfull == 'WakeLength_[-]':
                ax.plot(val_i*w*5/(RPMi*6*102.996267808408*2), CPU_hrs_i, '-o', color=colors[color_index], label='WS = {:}'.format(w))  # TODO asssume dpsi_cvg=5deg
            elif paramfull == 'WakeRegFactor_[-]' or 'WingRegFactor_[-]':
                ax.plot(val_i/dr, CPU_hrs_i, '-o', color=colors[color_index], label='WS = {:}'.format(w))
            else:
                ax.plot(val_i, CPU_hrs_i, '-o', color=colors[color_index], label='WS = {:}'.format(w))
    ax.grid()
    ax.legend(loc='best')
    ax.set_ylabel('Computational Time [hours]')
    remove_chartjunk(ax, ['top', 'right'])
    if paramfull == 'DTfvw_[s]':
        ax.set_xlabel('Wake Discretization [deg]')
    elif paramfull == 'nNWPanel_[-]':
        ax.set_xlabel('Near Wake Extent [deg]')
    elif paramfull == 'WakeLength_[-]':
        ax.set_xlabel('Far Wake Extent [D]')
    elif paramfull == 'WakeRegFactor_[-]':
        ax.set_xlabel('Wake Regularization Factor [dr]')
    elif paramfull == 'WingRegFactor_[-]':
        ax.set_xlabel('Wing Regularization Factor [dr]')
    elif paramfull == 'CoreSpreadEddyVisc_[-]':
        ax.set_xlabel('Core Spread Eddy Viscosity [-]')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/" + paramfull + '/' + param + "_simtime" + ".pdf"
        plt.savefig(plot_name, bbox_inches='tight')

""" RAW DATA """
def resolution_raw_all(paramfull, outlist, WS, plot):
    """
    Parameters
    ----------
    paramfull:  parameter varied in study [str]
    outlist:    list of output parameters to plot [str]
    WS:         list of wind speeds [m/s]
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    plots results

    """
    #  use nodes 8, 23 @ 25%, 75%
    n_plot = len(outlist)
    n_col = 3
    n_row = int(np.ceil(n_plot / n_col))
    fig, ax = plt.subplots(n_row, n_col, sharey=False, sharex=True, figsize=(8.5, 11))  # (6.4,4.8)
    fsize = 8

    for ws in WS:
        df = pd.read_csv('./PostPro/' + paramfull + '/Results_ws{:.0f}_'.format(ws) + paramfull + '.csv', sep='\t')
        df = df.fillna(0)
        for i in range(0, n_row):
            for j in range(0, n_col):
                idx = i * n_col + j
                if idx < n_plot:
                    if paramfull == 'DTfvw_[s]':
                        ax[i, j].plot(df[paramfull] * df['RotSpeed_[rpm]']*6, df[outlist[idx]], '-o',
                                label='WS = {:}'.format(ws))
                    else:
                        ax[i, j].plot(df[paramfull], df[outlist[idx]], '-o', label='WS = {:}'.format(ws))
                    ax[i, j].set_title(outlist[idx], fontsize=fsize)
                    ax[i, j].grid()
                    ax[i, j].tick_params(direction='in', labelsize=6.5)
                    # text(.5, .5, outlist[idx], transform=ax[i, j].transAxes)
                    if i == n_row - 1:
                        ax[i, j].set_xlabel(paramfull)
                        if paramfull == 'DTfvw_[s]':
                            ax[i, j].set_xlabel('Wake Discretization [deg]', fontsize=fsize)
                        else:
                            ax[i, j].set_xlabel(paramfull, fontsize=fsize)
                    if idx == (n_plot - 1):
                        ax[i, j].legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tick_params(direction='in', labelsize=2)
    plt.delaxes()
    plt.delaxes()
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        param = paramfull.split('_', 1)[0]
        plot_name = "PostPro/" + paramfull + '/' + param + "_ALL_RAW" + ".pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def resolution_pDiff_single(paramfull, out, WS, loc, plot):
    """
    Parameters
    ----------
    paramfull:  parameter varied in study [str]
    out:        single output parameter to plot [str]
    WS:         list of wind speeds [m/s]
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    plots of % diff between results at current and finest resolution

    """
    fig, ax = plt.subplots(1, figsize=(8.5, 11))  # (6.4,4.8)
    param = paramfull.split('_', 1)[0]
    outname = out.split('_', 1)[0]
    dr = 3.448147165807185
    for ws in WS:
        # df = pd.read_csv('./PostPro/' + paramfull +'/Results_ws{:.0f}_'.format(ws) + paramfull + '.csv', sep='\t')
        # df_fine = df.iloc[loc]
        # dfpdiff = (df - df_fine) / df_fine * 100
        # dfpdiff = dfpdiff.fillna(0)
        k = WS.index(ws)
        color_index = 2*k + 1
        df = pd.read_csv('./PostPro/' + paramfull + '/Results_ws{:.0f}_'.format(ws) + paramfull + '.csv', sep='\t')
        full_list = [out] + [paramfull]+['RotSpeed_[rpm]']
        if paramfull in {'WakeRegFactor_[-]', 'WingRegFactor_[-]',
                         'CoreSpreadEddyVisc_[-]'}:  # Compare to SOWFA for these runs
            SOWFA_out = out
            # switch channel used as SOWFA has 15x more nodes
            if out == 'AB1N008AxInd_[-]':
                SOWFA_out = 'AB1N120AxInd_[-]'
            elif out == 'AB1N023AxInd_[-]':
                SOWFA_out = 'AB1N345AxInd_[-]'
            elif out == 'AB1N008TnInd_[-]':
                SOWFA_out = 'AB1N120TnInd_[-]'
            elif out == 'AB1N023TnInd_[-]':
                SOWFA_out = 'AB1N345TnInd_[-]'
            elif out == 'AB1N008Gam_[m^2/s]':
                SOWFA_out = 'AB1N120Gam_[m^2/s]'
            elif out == 'AB1N023Gam_[m^2/s]':
                SOWFA_out = 'AB1N345Gam_[m^2/s]'

            df_sowfa = pd.read_csv('PostPro/Results_SOWFA.csv', sep='\t')
            SOWFA_data = df_sowfa[SOWFA_out].iloc[k]
            OLAF_data = df[out]
            dfpdiff = (OLAF_data - SOWFA_data) / SOWFA_data * 100
            paramdf = df[paramfull].to_frame(name=paramfull)
            dfpdiff = pd.concat([paramdf, dfpdiff], axis=1)
            # df_fine.rename(columns={'AB1N120AxInd_[-]': 'AB1N008AxInd_[-]', 'AB1N345AxInd_[-]': 'AB1N023AxInd_[-]',
            #                'AB1N120TnInd_[-]': 'AB1N008TnInd_[-]', 'AB1N345TnInd_[-]': 'AB1N023TnInd_[-]',
            #                'AB1N120Gam_[m^2/s]': 'AB1N008Gam_[m^2/s]', 'AB1N345Gam_[m^2/s]': 'AB1N023Gam_[m^2/s]'})
        else:
            df = df[full_list]
            df_fine = df.iloc[loc]
            dfpdiff = (df - df_fine) / df_fine * 100
        dfpdiff = dfpdiff.fillna(0)
        if paramfull=='DTfvw_[s]':
            ax.plot(df[paramfull]*df['RotSpeed_[rpm]']*6, dfpdiff[out], '-o', color=colors[color_index], label='WS = {:}'.format(ws))
        elif paramfull == 'nNWPanel_[-]':
            ax.plot(df[paramfull]*5, dfpdiff[out], '-o', color=colors[color_index], label='WS = {:}'.format(ws))  # TODO asssume dpsi_cvg=5deg
        elif paramfull == 'WakeLength_[-]':
            ax.plot(df[paramfull]*ws*5/(df['RotSpeed_[rpm]']*6*102.996267808408*2), dfpdiff[out], '-o', color=colors[color_index], label='WS = {:}'.format(ws))  # TODO asssume dpsi_cvg=5deg
        elif paramfull == 'WakeRegFactor_[-]' or 'WingRegFactor_[-]':
            ax.plot(df[paramfull]/dr, dfpdiff[out], '-o', color=colors[color_index], label='WS = {:}'.format(ws))
        else:
            ax.plot(df[paramfull], dfpdiff[out], '-o', color=colors[color_index], label='WS = {:}'.format(ws))
    # ax.set_title(outname, fontsize=10)
    ax.grid()
    ax.set_ylabel('Percent Difference')
    remove_chartjunk(ax, ['top', 'right'])
    if paramfull == 'DTfvw_[s]':
        ax.set_xlabel('Wake Discretization [deg]')
    elif paramfull == 'nNWPanel_[-]':
        ax.set_xlabel('Near Wake Extent [deg]')
    elif paramfull == 'WakeLength_[-]':
        ax.set_xlabel('Far Wake Extent [D]')
    elif paramfull == 'WakeRegFactor_[-]':
        ax.set_xlabel('Wake Regularization Factor [dr]')
    elif paramfull == 'WingRegFactor_[-]':
        ax.set_xlabel('Wing Regularization Factor [dr]')
    elif paramfull == 'CoreSpreadEddyVisc_[-]':
        ax.set_xlabel('Core Spread Eddy Viscosity [-]')
    else:
        ax.set_xlabel(paramfull)
    plt.tick_params(direction='in')
    ax.legend(loc='best')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/" + paramfull + '/' + param + '_' + outname + "_%diff" + ".pdf"
        plt.savefig(plot_name, bbox_inches='tight')

def resolution_pDiff_all(paramfull, outlist, WS, loc, plot):
    """
    Parameters
    ----------
    paramfull:  parameter varied in study [str]
    outlist:    list of output parameters to plot [str]
    WS:         list of wind speeds [m/s]
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    plots of % diff between results at current and finest resolution

    """
    #  use nodes 8, 23 @ 25%, 75%
    n_plot = len(outlist)
    n_col = 3
    n_row = int(np.ceil(n_plot/n_col))
    fig, ax = plt.subplots(n_row, n_col, sharey=False, sharex=True, figsize=(8.5, 11))  # (6.4,4.8)
    fsize = 8

    for ws in WS:
        k = WS.index(ws)
        df = pd.read_csv('./PostPro/' + paramfull +'/Results_ws{:.0f}_'.format(ws) + paramfull + '.csv', sep='\t')
        full_list = outlist + [paramfull]
        if paramfull in {'WakeRegFactor_[-]',  'WingRegFactor_[-]', 'CoreSpreadEddyVisc_[-]'}:  # Compare to SOWFA for these runs
            df_sowfa = pd.read_csv('PostPro/Results_SOWFA.csv', sep='\t')
            SOWFA_outlist = ['HSShftPwr_[kW]', 'RootMOoP1_[kN-m]', 'RootMzb1_[kN-m]', 'RotThrust_[kN]',
               'TwrBsMxt_[kN-m]', 'TwrBsMyt_[kN-m]', 'AB1N120AxInd_[-]', 'AB1N345AxInd_[-]',
               'AB1N120TnInd_[-]', 'AB1N345TnInd_[-]', 'AB1N120Gam_[m^2/s]', 'AB1N345Gam_[m^2/s]']
            SOWFA_data = df_sowfa[SOWFA_outlist].iloc[k].to_numpy()
            OLAF_data = df[outlist].to_numpy()
            pdiff = (OLAF_data-SOWFA_data)/SOWFA_data * 100
            dfpdiff = pd.DataFrame(data=pdiff, columns=outlist)
            paramdf = df[paramfull].to_frame(name=paramfull)
            dfpdiff = pd.concat([paramdf, dfpdiff], axis=1)
            # df_fine.rename(columns={'AB1N120AxInd_[-]': 'AB1N008AxInd_[-]', 'AB1N345AxInd_[-]': 'AB1N023AxInd_[-]',
            #                'AB1N120TnInd_[-]': 'AB1N008TnInd_[-]', 'AB1N345TnInd_[-]': 'AB1N023TnInd_[-]',
            #                'AB1N120Gam_[m^2/s]': 'AB1N008Gam_[m^2/s]', 'AB1N345Gam_[m^2/s]': 'AB1N023Gam_[m^2/s]'})
        else:
            rotspd = df['RotSpeed_[rpm]']
            df = df[full_list]
            df_fine = df.iloc[loc]
            dfpdiff = (df - df_fine) / df_fine * 100
        dfpdiff = dfpdiff.fillna(0)
        for i in range(0, n_row):
            for j in range(0, n_col):
                idx = i*n_col + j
                if idx < n_plot:
                    if paramfull == 'DTfvw_[s]':
                        ax[i, j].plot(df[paramfull] * rotspd * 6, dfpdiff[outlist[idx]], '-o',
                            label='WS = {:}'.format(ws))
                    elif paramfull == 'nNWPanel_[-]':
                        ax[i, j].plot(df[paramfull] * 5, dfpdiff[outlist[idx]], '-o',
                                      label='WS = {:}'.format(ws))
                    elif paramfull == 'WakeLength_[-]':
                        ax[i, j].plot(df[paramfull] * ws * 5 / (df['RotSpeed_[rpm]'] * 6 * 102.996267808408 * 2),
                                dfpdiff[outlist[idx]], '-o', label='WS = {:}'.format(ws))  # TODO asssume dpsi_cvg=5deg
                    else:
                        ax[i, j].plot(df[paramfull], dfpdiff[outlist[idx]], '-o', label='WS = {:}'.format(ws))
                    ax[i, j].set_title(outlist[idx].split('_', 1)[0], fontsize=fsize)
                    ax[i, j].tick_params(axis='both', labelsize=fsize)
                    ax[i, j].grid()
                        # text(.5, .5, outlist[idx], transform=ax[i, j].transAxes)
                    if j==0:
                        ax[i, j].set_ylabel('% Difference', fontsize=fsize)
                    if i==n_row-1:
                        if paramfull == 'DTfvw_[s]':
                            ax[i, j].set_xlabel('dpsi [deg]', fontsize=fsize)
                        elif paramfull == 'nNWPanel_[-]':
                            ax[i, j].set_xlabel('NearWakeExtent [deg]')
                        elif paramfull == 'WakeLength_[-]':
                            ax[i, j].set_xlabel('FarWakeExtent [D]')
                        else:
                            ax[i, j].set_xlabel(paramfull, fontsize=fsize)
                    if idx==2:
                        ax[i, j].legend(loc='best', fontsize=fsize)

    plt.tick_params(direction='in')
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        param = paramfull.split('_', 1)[0]
        plot_name = "PostPro/" + paramfull + '/' + param + "_ALL_%diff" + ".pdf"
        plt.savefig(plot_name, bbox_inches='tight')

""" PLOT OUTPUTS ALONG BLADE SPAN, VARYING WS and param """
def spanwise_vary_both(paramfull, values, WS, plot):
    """
    Parameters
    ----------
    paramfull:   param to use
    values:      list of param values
    WS:         list of wind speeds [m/s]
    plot:       plot options. [0, 1, 2] - [no plot, show plot, save plot]

    Returns
    -------
    plots outputs along blade span
    """

    WSM = np.outer(WS, np.ones(len(values[0, :])))
    RPM = np.array([4, 5.5, 7.5, 7.84, 7.85])
    RPMM = np.outer(RPM, np.ones(len(values[0, :])))

    fig, ax = plt.subplots(3, 2, sharey=False, sharex=False, figsize=(15, 20))
    linestyle = [':', '-.', '--', '-', ':']
    linewidth = [1, 1, 1, 1, 2]
    colors = ['xkcd:blue', 'xkcd:green', 'xkcd:red', 'xkcd:orange', 'xkcd:black', 'xkcd:purple', 'xkcd:cyan',
              'xkcd:mustard', 'xkcd:lime green', 'xkcd:pink', 'xkcd:light brown', 'xkcd:grey', 'xkcd:sky blue',
              'xkcd:sea green', 'xkcd:maroon']
    # R = 103  # rotor radius [m]

    # The radial coordinate
    # norm_node_r = np.array([0.000000000000000e+00, 3.448147165807185e+00, 6.896294331614371e+00, 1.034444149742155e+01, 1.379258866322874e+01,
    #                         1.724073582903592e+01, 2.068888299484311e+01, 2.413703016065029e+01, 2.758517732645748e+01, 3.103332449226467e+01,
    #                         3.448147165807185e+01, 3.792961882387903e+01, 4.137776598968622e+01, 4.482591315549340e+01, 4.827406032130058e+01,
    #                         5.172220748710778e+01, 5.517035465291496e+01, 5.861850181872214e+01, 6.206664898452934e+01, 6.551479615033651e+01,
    #                         6.896294331614371e+01, 7.241109048195088e+01, 7.585923764775806e+01, 7.930738481356525e+01, 8.275553197937244e+01,
    #                         8.620367914517962e+01, 8.965182631098681e+01, 9.309997347679399e+01, 9.654812064260116e+01, 9.999626780840836e+01]) / 103
    legend_labels = []
    legend_handles = []
    for ws in WS:
        i = WS.index(ws)
        a = 0
        b = 0
        """ REPEAT EVERYTHING FOR SOWFA """
        if paramfull in {'WakeRegFactor_[-]',  'WingRegFactor_[-]', 'CoreSpreadEddyVisc_[-]'}:
            legend_labels = legend_labels + ['SOWFA; ws_[m/s] = {:}'.format(ws)]
            # pull out spanwise values
            df = pd.read_csv('PostPro/Results_SOWFA.csv', sep='\t')
            ls = [i for i in list(df.columns) if (('B1N' in i) & ('Phi' in i))]
            N = len(ls)
            norm_node_r = np.linspace(0, 1, N)
            cols = df.columns.tolist()
            axind_cols = [j for j in cols if (('AxInd' in j) & ('B1N' in j))]
            AxInd = df[axind_cols].iloc[i]
            tanind_cols = [j for j in cols if (('TnInd' in j) & ('B1N' in j))]
            TnInd = df[tanind_cols].iloc[i]
            fn_cols = [j for j in cols if (('Fn' in j) & ('B1N' in j))]
            Fn = df[fn_cols].iloc[i]
            ft_cols = [j for j in cols if (('Ft' in j) & ('B1N' in j))]
            Ft = df[ft_cols].iloc[i]
            fl_cols = [j for j in cols if (('Fl' in j) & ('B1N' in j))]
            Fl = df[fl_cols].iloc[i]
            fd_cols = [j for j in cols if (('Fd' in j) & ('B1N' in j))]
            Fd = df[fd_cols].iloc[i]
            gam_cols = [j for j in cols if (('Gam' in j) & ('B1N' in j))]
            Circ = df[gam_cols].iloc[i]

            # # compute spanwise stats, append to df, and write back to csv
            # if b == 0:  # only do it once
            #     AxIndMean = AxInd.mean(axis=1); AxIndMean = AxIndMean.rename('AxIndMean')
            #     AxIndMax  = AxInd.max(axis=1);   AxIndMax = AxIndMax.rename('AxIndMax')
            #     CircMean  = Circ.mean(axis=1);   CircMean = CircMean.rename('CircMean')
            #     CircMax   = Circ.max(axis=1);    CircMax  = CircMax.rename('CircMax')
            #     df = pd.concat([df, AxIndMean, AxIndMax, CircMean, CircMax], axis=1)
            #     df.to_csv('Results_SOWFA.csv', sep='\t', index=False)

            # AxInd = pd.concat([AxInd, mean, max], axis=1)
            # plot everything
            # (0, (3, 5, 1, 5, 1, 5))
            ax[0, 0].set_ylabel('Axial Induction')
            ax[0, 0].plot(norm_node_r, AxInd, linestyle=linestyle[i], linewidth=linewidth[i], color=colors[-1])
            ax[0, 1].set_ylabel('Tangential Induction')
            ax[0, 1].plot(norm_node_r, TnInd, linestyle=linestyle[i], linewidth=linewidth[i], color=colors[-1])
            ax[1, 0].set_ylabel('Normal Force [N]')
            ax[1, 0].plot(norm_node_r, Fn, linestyle=linestyle[i], linewidth=linewidth[i], color=colors[-1])
            ax[1, 1].set_ylabel('Tangential Force [N]')
            ax[1, 1].plot(norm_node_r, Ft, linestyle=linestyle[i], linewidth=linewidth[i], color=colors[-1])
            ax[1, 1].set_xlabel('r/R')
            # ax[2, 0].set_ylabel('Lift Force [N]')
            # ax[2, 0].plot(norm_node_r, Fl.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            # ax[2, 1].set_ylabel('Drag Force [N]')
            # ax[2, 1].plot(norm_node_r, Fd.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[2, 0].set_ylabel('Circulation')
            ax[2, 0].set_xlabel('r/R')
            ax[2, 0].plot(norm_node_r, Circ, linestyle=linestyle[i], linewidth=linewidth[i], color=colors[-1],
                          label='ws = {:}'.format(ws))

        for value in values[i, :]:
            # pull out spanwise values
            df = pd.read_csv('./PostPro/' + paramfull +'/Results_ws{:.0f}_'.format(ws) + paramfull + '.csv', sep='\t')
            ls = [i for i in list(df.columns) if (('B1N' in i) & ('Phi' in i))]
            N = len(ls)
            norm_node_r = np.linspace(0, 1, N)
            cols = df.columns.tolist()
            axind_cols = [j for j in cols if 'AxInd' in j]
            AxInd = df[axind_cols]
            tanind_cols = [j for j in cols if 'TnInd' in j]
            TnInd = df[tanind_cols]
            fn_cols = [j for j in cols if 'Fn' in j]
            Fn = df[fn_cols]
            ft_cols = [j for j in cols if 'Ft' in j]
            Ft = df[ft_cols]
            fl_cols = [j for j in cols if 'Fl' in j]
            Fl = df[fl_cols]
            fd_cols = [j for j in cols if 'Fd' in j]
            Fd = df[fd_cols]
            gam_cols = [j for j in cols if 'Gam' in j]
            Circ = df[gam_cols]

            # compute spanwise stats, append to df, and write back to csv
            AxIndMean = AxInd.mean(axis=1); AxIndMean = AxIndMean.rename('AxIndMean')
            AxIndMax  = AxInd.max(axis=1);   AxIndMax = AxIndMax.rename('AxIndMax')
            CircMean  = Circ.mean(axis=1);   CircMean = CircMean.rename('CircMean')
            CircMax   = Circ.max(axis=1);    CircMax  = CircMax.rename('CircMax')
            df = pd.concat([df, AxIndMean, AxIndMax, CircMean, CircMax], axis=1)
            df.to_csv('./PostPro/' + paramfull +'/Results_ws{:04.1f}'.format(ws) + '_' + paramfull + '.csv', sep='\t', index=False)
            # AxInd = pd.concat([AxInd, mean, max], axis=1)
            #plot everything
            k = df.index[abs(df[paramfull]-value)<1e-5][0]  # assert almost equal

            #(0, (3, 5, 1, 5, 1, 5))
            ax[0, 0].set_ylabel('Axial Induction')
            ax[0, 0].plot(norm_node_r, AxInd.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[0, 1].set_ylabel('Tangential Induction')
            ax[0, 1].plot(norm_node_r, TnInd.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[1, 0].set_ylabel('Normal Force [N]')
            ax[1, 0].plot(norm_node_r, Fn.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[1, 1].set_ylabel('Tangential Force [N]')
            ax[1, 1].plot(norm_node_r, Ft.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[1, 1].set_xlabel('r/R')
            # ax[2, 0].set_ylabel('Lift Force [N]')
            # ax[2, 0].plot(norm_node_r, Fl.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            # ax[2, 1].set_ylabel('Drag Force [N]')
            # ax[2, 1].plot(norm_node_r, Fd.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a])
            ax[2, 0].set_ylabel('Circulation')
            ax[2, 0].set_xlabel('r/R')
            ax[2, 0].plot(norm_node_r, Circ.iloc[k], linestyle=linestyle[i], linewidth=linewidth[i], color=colors[a], label='ws = {:}'.format(ws))




            """for display, change values to desired"""
            if paramfull == 'DTfvw_[s]':
                legend_value = np.round(value * RPM[i] * 6, 1)
                legend_paramfull = 'dpsi_[deg]'
            elif paramfull == 'nNWPanel_[-]':
                legend_value = np.round(value * 5, 0)
                legend_paramfull = 'NearWakeExtent_[deg]'
            elif paramfull == 'WakeLength_[-]':
                legend_value = np.round(value * ws * 5 / (RPM[i] * 6 * 102.996267808408 * 2), 0)
                legend_paramfull = 'FarWakeExtent_[D]'
            else:
                legend_value = value
                legend_paramfull = paramfull

            legend_labels = legend_labels + [legend_paramfull + " = {:04.1f}".format(legend_value) + '; ws_[m/s] = {:}'.format(ws)]
            a+=1

    ax[2, 0].legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
    ax[0, 0].grid(); ax[0, 1].grid(); ax[1, 0].grid(); ax[1, 1].grid(); ax[2, 0].grid();
    plt.tick_params(direction='in')
    plt.delaxes()
    plt.grid(True)
    if plot == 1:
        plt.show()
        plt.close()
    elif plot == 2:
        plot_name = "PostPro/" + paramfull + '/' + paramfull + "SPANWISE.pdf"
        plt.savefig(plot_name, bbox_inches='tight')

""" RUN RESOLUTION STUDY """
def run_study(WS, paramfull, values):
    """ run a resolution study
    Parameters
    ----------
    WS:                 list of wind speeds [m/s]
    paramfull:          parameter name to vary + _[units]
    parameter values:   list of parameter values

    Returns
    -------
    plots of % diff between results at current and finest resolution
    """
    param = paramfull.split('_', 1)[0]  # param name w/o units
    cwd = os.getcwd()
    work_dir = 'BAR_02_discretization_inputs/' + param + '/'
    postpro_dir = './PostPro/' + paramfull + '/'
    ##for DTfvw###############################
    RPM = np.array([4, 5.5, 7.5, 7.84, 7.85])
    rotSpd = RPM * 0.104719755  # rad/s
    ##########################################
    """get location of most resolved parameter value"""
    if paramfull == 'DTfvw_[s]':
        loc = 0
    elif paramfull == 'nNWPanel_[-]':
        loc = -1
    elif paramfull == 'WakeLength_[-]':
        loc = -1
    elif paramfull == 'WakeRegFactor_[-]':
        loc = 0
    elif paramfull == 'WingRegFactor_[-]':
        loc = 0
    elif paramfull == 'CoreSpreadEddyVisc_[-]':
        loc = -1

    # create csvs
    # if not os.path.isdir(cwd + postpro_dir[1:]):
    #     os.mkdir(cwd + postpro_dir[1:])
    # for wsp in WS:
    #     i = WS.index(wsp)
    #     outFiles=[]
    #     for val in values[i,:]:
    #         case     ='ws{:.0f}'.format(wsp)+'_'+param+'{:.3f}'.format(val)
    #         filename = os.path.join(work_dir, case + '.outb')
    #         outFiles.append(filename)
    #     # print(outFiles)
    #     dfAvg = fastlib.averagePostPro(outFiles,avgMethod='periods',avgParam=1,ColMap={'WS_[m/s]':'Wind1VelX_[m/s]'})
    #     dfAvg.insert(0,paramfull, values[i, :])
    #     # --- Save to csv since step above can be expensive
    #     csvname = 'Results_ws{:.0f}_'.format(wsp) + paramfull + '.csv'
    #     csvpath = os.path.join(postpro_dir, csvname)
    #     dfAvg.to_csv(csvpath, sep='\t', index=False)
    #     print(dfAvg)
    # print('created all csvs ')

    outlist = ['HSShftPwr_[kW]', 'RootMIP1_[kN-m]', 'RootMOoP1_[kN-m]', 'RootMzb1_[kN-m]', 'RotThrust_[kN]',
               'TwrBsMxt_[kN-m]', 'TwrBsMyt_[kN-m]', 'AB1N008AxInd_[-]', 'AB1N023AxInd_[-]',
               'AB1N008TnInd_[-]', 'AB1N023TnInd_[-]', 'AB1N008Gam_[m^2/s]', 'AB1N023Gam_[m^2/s]']
    outlist_pd = ['HSShftPwr_[kW]', 'RootMOoP1_[kN-m]', 'RootMzb1_[kN-m]', 'RotThrust_[kN]',
               'TwrBsMxt_[kN-m]', 'TwrBsMyt_[kN-m]', 'AB1N008AxInd_[-]', 'AB1N023AxInd_[-]',
               'AB1N008TnInd_[-]', 'AB1N023TnInd_[-]', 'AB1N008Gam_[m^2/s]', 'AB1N023Gam_[m^2/s]']

    # outlist_pd = ['AB1N008AxInd_[-]', 'AB1N023AxInd_[-]',                                              #  TODO fix
    #            'AB1N008TnInd_[-]', 'AB1N023TnInd_[-]', 'AB1N008Gam_[m^2/s]', 'AB1N023Gam_[m^2/s]']

    # calc_sim_times(paramfull, 2)
    for out in outlist_pd:
        resolution_pDiff_single(paramfull, out, WS, loc, 2)
    resolution_raw_all(paramfull, outlist, WS, 2)
    resolution_pDiff_all(paramfull, outlist_pd, WS, loc, 2)
    spanwise_vary_both(paramfull, values, WS, 2)

    print('Ran ' + paramfull + ' post processing')

if __name__ == "__main__":

    study = study1
    run_study(WS=study['WS'], paramfull=study['paramfull'], values=study[study['param']])





