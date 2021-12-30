import numpy as np
trans_cost = np.linspace(-50, 5, 12)
LCOE = np.array([37.4317895, 37.48617617, 37.54056285, 37.59494952, 37.6493362, 37.70372287, 37.75810954, 37.81249622, 37.86688289, 37.92126956, 37.97565624, 38.03004291])
LCOEpdiff = (LCOE - LCOE[-2]) / LCOE[-2] * 100
blade_cost = 436026  # no trans savings
Turbine_cost = 6715507  # no trans savings
x=1