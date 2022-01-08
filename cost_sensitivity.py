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
sc_joint_mass = np.array([572.51, 595.91, 503.33, 457.68, 385.51, 223.96, 97.66]) * 4
joint_mass_adder = np.array([1141.87, 1141.04, 960.17, 809.03, 608.23, 399.10, 211.83])
joint_mass_tot = sc_joint_mass + joint_mass_adder
joint_loc =         [20, 30, 40, 50, 60, 70, 80]
n_bolts =           [52, 52, 57, 48, 50, 33, 17]
joint_cost_adder =  [7362, 7362, 6566, 5542, 4503, 2950, 1562]  # just hardware, adhesive TODO need to subtract bored our carbon fiber??? - NO because it would be bored out and lost
sc_joint_cost = sc_joint_mass * 20.08  # CF uni cost
joint_cost_tot = joint_cost_adder + sc_joint_cost
blade_mass =        np.array([49276, 49282, 49069, 49008, 48822, 48591, 48361])
blade_cost =        np.array([430851, 430851, 430042, 429003, 427946, 426366, 424953])
turbine_mass =      np.array([1276969, 1277085, 1276450, 1276348, 1275763, 1275011, 1274207])
turbine_cost =      np.array([6692702, 6693196, 6689369, 6686203, 6681682, 6675162, 6668922])
LCOE =              np.array([37.89, 37.90, 37.88, 37.87, 37.86, 37.83, 37.81])
AEP = 24.74  # GWh

# RUNNING THE OPTMIZED YAMLS THROUGH ONCE TO CAPTURE UPDATED SC WIDTH. Note: loc30 wanted 26.33 bolts (lim 26) and loc20 wanted 26.6 bolts (lim 26?)
blade_mass = [51439, 51516, 50937, 50669, 50170, 49221, 48440]
LCOE = [38.12, 38.14, 38.05, 38.01, 37.92, 37.73, 37.58]

# RUNNING SECOND OPT WITH FIRST OPT YAMLS AS BASELINE. Note: loc30 wanted 26.19 bolts (lim 26) and loc20 wanted 26.58 bolts (lim 26?)
# FINALLY, RUNNING THE SECOND OPT YAMLS THROUGH ONCE TO UPDATE COSTS AND MASSES - this didn't really change anything because I connected bjs cost/mass to rotor cost
n_bolts =           [52, 52, 57.34, 48.16, 48.6, 31.82, 17.16]
joint_mass_adder = np.array([1142.0, 1142.08, 963.41, 808.46, 598.00, 391.52, 211.11])
joint_mass_tot = sc_joint_mass + joint_mass_adder
joint_cost_adder =  [7362, 7362, 6582, 5529, 4409, 2886, 1556]
joint_cost_tot = joint_cost_adder + sc_joint_cost
blade_mass =        np.array([51111, 50916, 50447, 50092, 49240, 48609, 48206])
blade_cost =        np.array([440573, 437001, 431134, 426500, 413969, 404846, 399533])
turbine_mass =      np.array([1283163, 1282717, 1281315, 1280265, 1277422, 1275229, 1273656])
turbine_cost =      np.array([6736627, 6725193, 6704549, 6688386, 6643893, 6611137, 6591178])
LCOE =              np.array([38.05, 38.01, 37.94, 37.88, 37.72, 37.60, 37.53])

""" PLOT BLADE MASS AND JOINT MASS"""
""" PLOT BLADE COST AND JOINT COST"""
""" PLOT LCOE AND MAYBE SOMETHING ELSE?"""
colors=pl.cm.tab20b(np.linspace(0,1,10))
plt.rc("font", family="serif")
plt.rc("font", size=8)
plt.rc("lines", lw=1)
plt.rc("lines", markersize=4)

plot = 2

fig, ax = plt.subplots(3, 1, sharey=False, sharex=True, figsize=(3.2, 5))
color = 'tab:orange'
ax[0].plot(joint_loc, joint_mass_tot/1000, '-o', color=color)
ax[0].grid()
ax[0].set_ylabel('Joint mass [tonne]', color=color)
ax[0].tick_params(direction='in', axis='y', labelcolor=color)
ax[0].set_ylim(0, 4)

ax2 = ax[0].twinx()
color = 'tab:blue'
ax2.plot(joint_loc, blade_mass/1000, '-o', color=color)
ax2.set_ylabel('Blade mass [tonne]', color=color)
ax2.tick_params(direction='in', axis='y', labelcolor=color)
ax2.set_ylim(47.6, 51.6)

color = 'tab:red'
ax[1].plot(joint_loc, joint_cost_tot/1000, '-o', color=color)
ax[1].grid()
ax[1].set_ylabel('Joint cost [K USD]', color=color)
ax[1].tick_params(direction='in', axis='y', labelcolor=color)
ax[1].set_ylim(0, 60)

ax3 = ax[1].twinx()
color = 'tab:green'
ax3.plot(joint_loc, blade_cost/1000, '-o', color=color)
ax3.set_ylabel('Blade cost [K USD]', color=color)
ax3.tick_params(direction='in', axis='y', labelcolor=color)
ax3.set_ylim(390, 450)

ax[2].grid()
color = 'tab:purple'
ax[2].plot(joint_loc, LCOE, '-o', color=color)  # label='average power output [kW]')
ax[2].set_ylabel('LCOE', color=color)
ax[2].tick_params(direction='in', axis='y', labelcolor=color)
ax[2].set_ylim(37.4, 38.2)

ax4 = ax[2].twinx()
color = 'tab:gray'
ax4.plot(joint_loc, turbine_cost/1e6, '-o', color=color)
ax4.set_ylabel('Turbine cost [M USD]', color=color)
ax4.tick_params(direction='in', axis='y', labelcolor=color)
ax4.set_ylim(6.55, 6.75)

ax[2].set_xlabel('Joint location [span]')


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

