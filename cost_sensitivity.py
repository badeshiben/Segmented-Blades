import numpy as np
# cost sensitivity, no optimization
trans_cost = np.linspace(-50, 5, 12)
LCOE = np.array([37.4317895, 37.48617617, 37.54056285, 37.59494952, 37.6493362, 37.70372287, 37.75810954, 37.81249622, 37.86688289, 37.92126956, 37.97565624, 38.03004291])
LCOEpdiff = (LCOE - LCOE[-2]) / LCOE[-2] * 100
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
blade_mass =        [49276, 49282, 49069, 49008, 48822, 48591, 48361]
blade_cost =        [430851, 430851, 430042, 429003, 427946, 426366, 424953]
turbine_mass =      [1276969, 1277085, 1276450, 1276348, 1275763, 1275011, 1274207]
turbine_cost =      [6692702, 6693196, 6689369, 6686203, 6681682, 6675162, 6668922]
LCOE =              [37.89, 37.90, 37.88, 37.87, 37.86, 37.83, 37.81]
AEP = 24.74  # GWh

# RUNNING THE OPTMIZED YAMLS THROUGH ONCE TO CAPTURE UPDATED SC WIDTH. Note: loc30 wanted 26.33 bolts (lim 26) and loc20 wanted 26.6 bolts (lim 26?)
blade_mass = [51439, 51516, 50937, 50669, 50170, 49221, 48440]
LCOE = [38.12, 38.14, 38.05, 38.01, 37.92, 37.73, 37.58]

# RUNNING SECOND OPT WITH FIRST OPT YAMLS AS BASELINE. Note: loc30 wanted 26.19 bolts (lim 26) and loc20 wanted 26.58 bolts (lim 26?)
# FINALLY, RUNNING THE SECOND OPT YAMLS THROUGH ONCE TO UPDATE COSTS AND MASSES
























# w_i = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
# t_i = [0.042311807748218355, 0.04569526776353126, 0.038784082083498365, 0.03350953180984813, 0.027667406379626357, 0.022583858212564614, 0.01713608265938962]
# w_f = [3.7440000000000007, 3.7440000000000007, 3.6036, 3.0429, 2.6816399999999994, 1.7571599999999996, 0.9298799999999998]
# t_f = [0.07027886441380944, 0.07304312588018114, 0.06452636771532025, 0.07106079429375539, 0.06848077011625611, 0.06245404105787048, 0.05345848905045851]

# blade_mass_diff =
# blade_mass_pdiff =

