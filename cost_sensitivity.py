import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib.utils import remove_chartjunk
import matplotlib.pylab as pl
# cost sensitivity, no optimization
trans_cost = np.linspace(-50, 5, 12)
LCOE = np.array([37.4317895, 37.48617617, 37.54056285, 37.59494952, 37.6493362, 37.70372287, 37.75810954, 37.81249622, 37.86688289, 37.92126956, 37.97565624, 38.03004291])
LCOEpdiff = (LCOE - LCOE[-2]) / LCOE[-2] * 100
slope1 = LCOEpdiff/(trans_cost-trans_cost[-2])
slope2 = (LCOE - LCOE [-1])/(trans_cost-trans_cost[-1])
blade_cost = 436026  # no trans savings
Turbine_cost = 6715507  # no trans savings
x=1

# WISDEM optimizations. FIRST PASS Joint added from 20-80% span
blade_mass_i = 49427.38
# calc from solidworks
#L_segment = 3.442m
#w_init = 0.8, t_init varies. Both come from BAR_USC_masslessjoint.yaml. Calculate sparcap joint mass by subtracting mass of initial by final (mult by 4 for 2 sides of joint, and 2 sc sides)
#rho=1600
sc_joint_mass_original = np.array([572.51, 595.91, 503.33, 457.68, 385.51, 223.96, 97.66, 44.497]) * 4
joint_mass_adder_original = np.array([1141.87, 1141.04, 960.17, 809.03, 608.23, 399.10, 211.83, 98])
# joint_mass_tot = sc_joint_mass + joint_mass_adder
# joint_loc =         [20, 30, 40, 50, 60, 70, 80]
# n_bolts =           [52, 52, 57, 48, 50, 33, 17]
# joint_cost_adder =  [7362, 7362, 6566, 5542, 4503, 2950, 1562]  # just hardware, adhesive TODO need to subtract bored our carbon fiber??? - NO because it would be bored out and lost
# sc_joint_cost = sc_joint_mass * 20.08  # CF uni cost
# joint_cost_tot = joint_cost_adder + sc_joint_cost
# blade_mass =        np.array([49276, 49282, 49069, 49008, 48822, 48591, 48361])
# blade_cost =        np.array([430851, 430851, 430042, 429003, 427946, 426366, 424953])
# turbine_mass =      np.array([1276969, 1277085, 1276450, 1276348, 1275763, 1275011, 1274207])
# turbine_cost =      np.array([6692702, 6693196, 6689369, 6686203, 6681682, 6675162, 6668922])
# LCOE =              np.array([37.89, 37.90, 37.88, 37.87, 37.86, 37.83, 37.81])
# AEP = 24.74  # GWh

# # RUNNING THE OPTMIZED YAMLS THROUGH ONCE TO CAPTURE UPDATED SC WIDTH. Note: loc30 wanted 26.33 bolts (lim 26) and loc20 wanted 26.6 bolts (lim 26?)
# blade_mass = [51439, 51516, 50937, 50669, 50170, 49221, 48440]
# LCOE = [38.12, 38.14, 38.05, 38.01, 37.92, 37.73, 37.58]
#
# # RUNNING SECOND OPT WITH FIRST OPT YAMLS AS BASELINE. Note: loc30 wanted 26.19 bolts (lim 26) and loc20 wanted 26.58 bolts (lim 26?)
# # FINALLY, RUNNING THE SECOND OPT YAMLS THROUGH ONCE TO UPDATE COSTS AND MASSES - this didn't really change anything because I connected bjs cost/mass to rotor cost
# n_bolts =           [52, 52, 57.34, 48.16, 48.6, 31.82, 17.16]
# joint_mass_adder = np.array([1142.0, 1142.08, 963.41, 808.46, 598.00, 391.52, 211.11])
# joint_mass_tot = sc_joint_mass + joint_mass_adder
# joint_cost_adder =  [7362, 7362, 6582, 5529, 4409, 2886, 1556]
# joint_cost_tot = joint_cost_adder + sc_joint_cost
# print(joint_mass_tot)
# blade_mass =        np.array([51111, 50916, 50447, 50092, 49240, 48609, 48206])
# blade_cost =        np.array([440573, 437001, 431134, 426500, 413969, 404846, 399533])
# turbine_mass =      np.array([1283163, 1282717, 1281315, 1280265, 1277422, 1275229, 1273656])
# turbine_cost =      np.array([6736627, 6725193, 6704549, 6688386, 6643893, 6611137, 6591178])
# LCOE =              np.array([38.05, 38.01, 37.94, 37.88, 37.72, 37.60, 37.53])
# turbine_cost_kW =   turbine_cost/5e3

# I WAS USING THE WRONG BAR USC INPUT SO I HAD TO REDO EVERYTHING...BELOW ARE OUTPUTS FROM THE SECOND OPT RUN
joint_loc =         np.array([20, 30, 40, 50, 60, 70, 80, 90])
tip_length =        100 - joint_loc
n_bolts =           [48, 48, 48.74, 54, 42.28, 39.5, 22.6, 18.08]
joint_mass_adder = np.array([1239, 1239, 1070, 907, 710, 486, 278, 98])
joint_mass_adder_ratio = np.divide(joint_mass_adder, joint_mass_adder_original)
sc_joint_mass = np.multiply(sc_joint_mass_original , joint_mass_adder_ratio)
joint_mass_tot = sc_joint_mass + joint_mass_adder
joint_cost_adder =  [4901, 4901, 4221, 3583, 2805, 1929, 1104, 405]
sc_joint_cost = sc_joint_mass * 20.08  # CF uni cost
joint_cost_tot = joint_cost_adder + sc_joint_cost
print(joint_mass_tot)
blade_mass =        np.array([52304, 52001, 51570, 50970, 50348, 49646, 48987, 48588])
blade_cost =        np.array([533060, 528418, 520368, 514334, 505774, 496116, 486404, 479875])
turbine_mass =      np.array([1211212, 1210501, 1209331, 1207460, 1205448, 1203040, 1200586, 1198908])
turbine_cost =      np.array([7664081, 7648855, 7622320, 7599978, 7569540, 7526300, 7499187, 7475051])
LCOE =              np.array([37.09, 37.04, 36.96, 36.89, 36.79, 36.66, 36.58, 36.50])
turbine_cost_kW =   turbine_cost/5e3


# TODO scale updated sc mass adder with change in joint mass adder so that you don't have to run SW again

""" PLOT BLADE MASS AND JOINT MASS"""
""" PLOT BLADE COST AND JOINT COST"""
""" PLOT LCOE AND MAYBE SOMETHING ELSE?"""
colors=pl.cm.tab20b(np.linspace(0,1,10))
plt.rc("font", family="serif")
plt.rc("font", size=8)
plt.rc("lines", lw=1)
plt.rc("lines", markersize=4)

plot = 2

fig, ax = plt.subplots(2, 1, sharey=False, sharex=False, figsize=(3.2, 3.5))
color = 'tab:orange'
ax[0].plot(tip_length, joint_mass_tot/1000, '-o', color=color)
ax[0].grid()
ax[0].set_ylabel('Joint mass [ton]', color=color)
ax[0].tick_params(direction='in', axis='y', labelcolor=color)
ax[0].set_ylim(0, 5)
ax[0].xaxis.set_label_position('top')
ax[0].set_xlabel('Tip length [m]')
# ax[0].xaxis.set_tick_params(labeltop=True)
# ax[0].xaxis.set_tick_params(labelbottom=False)
ax[0].xaxis.set_ticks(tip_length.tolist())
ax[0].tick_params(bottom=False, top=True, left=True, right=True, labelbottom=False, labeltop=True, labelleft=True, labelright=True)
ax[0].set_xlim(82, 8)

ax2 = ax[0].twinx()
color = 'tab:blue'
ax2.plot(tip_length, blade_mass/1000, '-o', color=color)
ax2.set_ylabel('Blade mass [ton]', color=color)
ax2.tick_params(direction='in', axis='y', labelcolor=color)
ax2.set_ylim(48.3, 53.3)
ax2.set_xlim(82, 8)

color = 'tab:red'
ax[1].plot(joint_loc, joint_cost_tot/1000, '-o', color=color)
ax[1].grid()
ax[1].set_ylabel('Joint cost [k$]', color=color)
ax[1].tick_params(direction='in', axis='y', labelcolor=color)
ax[1].set_ylim(0, 65)
ax[1].set_xlim(18, 92)
ax[1].xaxis.set_ticks(joint_loc.tolist())

ax3 = ax[1].twinx()
color = 'tab:green'
ax3.plot(joint_loc, blade_cost/1000, '-o', color=color)
ax3.set_ylabel('Blade cost [k$]', color=color)
ax3.tick_params(direction='in', axis='y', labelcolor=color)
ax3.set_ylim(476, 541)
ax3.set_xlim(18, 92)
# ax[2].grid()
# color = 'tab:purple'
# ax[2].plot(joint_loc, LCOE, '-o', color=color)  # label='average power output [kW]')
# ax[2].set_ylabel('LCOE', color=color)
# ax[2].tick_params(direction='in', axis='y', labelcolor=color)
# ax[2].set_ylim(36.4, 37.2)
#
# ax4 = ax[2].twinx()
# color = 'tab:gray'
# ax4.plot(joint_loc, turbine_cost/1e6, '-o', color=color)
# ax4.set_ylabel('Turbine cost [M$]', color=color)
# ax4.tick_params(direction='in', axis='y', labelcolor=color)
# ax4.set_ylim(7.45, 7.7)

ax[1].set_xlabel('Joint location [m]')


# ax4.plot(dfPlot[param], dfPlot['Tower base fore-aft moment DEL'], '-o', color=color)  # label='average power output [kW]')
# ax4.set_ylabel('Tower base fore-aft moment DEL [kN-m]', color=color)
# ax4.tick_params(direction='in', axis='y', labelcolor=color)


remove_chartjunk(ax[0], ['top', 'right'])
# ax1.legend(loc='best')
if plot == 1:
    plt.show()
    plt.close()
elif plot == 2:
    plot_name = "PostPro/WISDEM_loc.pdf"
    plt.savefig(plot_name, bbox_inches='tight')


















# w_i = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
# t_i = [0.042311807748218355, 0.04569526776353126, 0.038784082083498365, 0.03350953180984813, 0.027667406379626357, 0.022583858212564614, 0.01713608265938962]
# w_f = [3.7440000000000007, 3.7440000000000007, 3.6036, 3.0429, 2.6816399999999994, 1.7571599999999996, 0.9298799999999998]
# t_f = [0.07027886441380944, 0.07304312588018114, 0.06452636771532025, 0.07106079429375539, 0.06848077011625611, 0.06245404105787048, 0.05345848905045851]

# blade_mass_diff =
# blade_mass_pdiff =

