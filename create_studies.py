import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import fastlib
import weio

# TODO non 1.1 DLC needs to be at the end sorry

#create new beamdyn blade, elastodyn blade matrices
EDfile = weio.read('BAR_USC_template/BAR_USC_ElastoDyn_blade.dat')
BDfile = weio.read('BAR_USC_template/BAR_USC_BeamDyn_blade.dat')

EDmat_ref = EDfile.data[14]['value']
EDmat = EDmat_ref.copy()

BDmat_ref = BDfile.data[8]['value']
BDmat = BDmat_ref.copy()

# for now, vary one thing (m, i, K) at a time.
# assume mx affects all M terms linearly
# assume ix affects M 'i' terms linearly
# assume kx affects all K terms linearly

# blade properties


"""Study 1: mass sensitivity    """
mi = EDmat[20, 3]  # kg/m3
L_segment = 3.54573  # m
m_joint_nom = 1000 / L_segment  # kg/m3
num = 10
m_range = np.linspace(0.2, 2, num=num)
m_add = m_range * m_joint_nom
mx = (mi + m_add) / mi
ix = mx
kx = np.ones(num)
values = 1000 * m_range

EDmat1 = np.repeat(EDmat[:, :, np.newaxis], num, axis=2)
BDmat1 = np.repeat(BDmat[:, :, np.newaxis], num, axis=2)
for i in range(0, num):
    EDmat1[20, 3, i]   = EDmat1[20, 3, i]  * mx[i]  # BMassDen
    EDmat1[20, 4, i]   = EDmat1[20, 4, i]  * kx[i]  # FlpStff
    EDmat1[20, 5, i]   = EDmat1[20, 5, i]  * kx[i]  # EdgStff
    BDmat1[20, 1, i]   = BDmat1[20, 1, i]  * kx[i]  # K_ShrFlp
    BDmat1[20, 8, i]   = BDmat1[20, 8, i]  * kx[i]  # K_ShrEdg
    BDmat1[20, 15, i]  = BDmat1[20, 15, i] * kx[i]  # EA
    BDmat1[20, 22, i]  = BDmat1[20, 22, i] * kx[i]  # EI_Edg
    BDmat1[20, 29, i]  = BDmat1[20, 29, i] * kx[i]  # EI_Flp
    BDmat1[20, 36, i]  = BDmat1[20, 36, i] * kx[i]  # GJ
    BDmat1[20, 37, i]  = BDmat1[20, 37, i] * mx[i]  # m
    BDmat1[20, 42, i]  = BDmat1[20, 42, i] * mx[i]  # -mYcm
    BDmat1[20, 44, i]  = BDmat1[20, 44, i] * mx[i]  # m
    BDmat1[20, 48, i]  = BDmat1[20, 48, i] * mx[i]  # mXcm
    BDmat1[20, 51, i]  = BDmat1[20, 51, i] * mx[i]  # m
    BDmat1[20, 52, i]  = BDmat1[20, 52, i] * mx[i]  # mYcm
    BDmat1[20, 53, i]  = BDmat1[20, 53, i] * mx[i]  # -mXcm
    BDmat1[20, 57, i]  = BDmat1[20, 57, i] * mx[i]  # mYcm
    BDmat1[20, 58, i]  = BDmat1[20, 58, i] * ix[i]  # i_Edg
    BDmat1[20, 59, i]  = BDmat1[20, 59, i] * ix[i]  # -i_cp
    BDmat1[20, 63, i]  = BDmat1[20, 63, i] * mx[i]  # -mXcm
    BDmat1[20, 64, i]  = BDmat1[20, 64, i] * ix[i]  # -i_cp
    BDmat1[20, 65, i]  = BDmat1[20, 65, i] * ix[i]  # i_Flp
    BDmat1[20, 67, i]  = BDmat1[20, 67, i] * mx[i]  # -mYcm
    BDmat1[20, 68, i]  = BDmat1[20, 68, i] * mx[i]  # mXcm
    BDmat1[20, 72, i]  = BDmat1[20, 58, i] + BDmat1[20, 65, i]  # i_plr = i_Edg + i_Flp
    # BDmat1[20, 72, i]  = BDmat1[20, 72, i] * ix[i]  # i_plr

x = EDmat1[:, :, 0]
y = BDmat1[:, :, 0]

study1 = {'EDmat': EDmat1, 'BDmat': BDmat1, 'parameter': 'mass', 'values': values,
          'DLC': ['1.1_U4', '1.1_U6', '1.1_U8', '1.1_U10', '1.1_U12', '1.1_U14', '1.1_U16', '1.1_U18', '1.1_U20', '1.1_U22', '1.1_U24', '1.1_U25', '1.3_U23']}

"""Study 2: inertia sensitivity    """
num = 10
ix = np.linspace(1, 5.5, num=num)
mx = np.ones(num)
kx = np.ones(num)

EDmat2 = np.repeat(EDmat[:, :, np.newaxis], num, axis=2)
BDmat2 = np.repeat(BDmat[:, :, np.newaxis], num, axis=2)
for i in range(0, num):
    EDmat2[20, 3, i]   = EDmat2[20, 3, i]  * mx[i]  # BMassDen
    EDmat2[20, 4, i]   = EDmat2[20, 4, i]  * kx[i]  # FlpStff
    EDmat2[20, 5, i]   = EDmat2[20, 5, i]  * kx[i]  # EdgStff
    BDmat2[20, 1, i]   = BDmat2[20, 1, i]  * kx[i]  # K_ShrFlp
    BDmat2[20, 8, i]   = BDmat2[20, 8, i]  * kx[i]  # K_ShrEdg
    BDmat2[20, 15, i]  = BDmat2[20, 15, i] * kx[i]  # EA
    BDmat2[20, 22, i]  = BDmat2[20, 22, i] * kx[i]  # EI_Edg
    BDmat2[20, 29, i]  = BDmat2[20, 29, i] * kx[i]  # EI_Flp
    BDmat2[20, 36, i]  = BDmat2[20, 36, i] * kx[i]  # GJ
    BDmat2[20, 37, i]  = BDmat2[20, 37, i] * mx[i]  # m
    BDmat2[20, 42, i]  = BDmat2[20, 42, i] * mx[i]  # -mYcm
    BDmat2[20, 44, i]  = BDmat2[20, 44, i] * mx[i]  # m
    BDmat2[20, 48, i]  = BDmat2[20, 48, i] * mx[i]  # mXcm
    BDmat2[20, 51, i]  = BDmat2[20, 51, i] * mx[i]  # m
    BDmat2[20, 52, i]  = BDmat2[20, 52, i] * mx[i]  # mYcm
    BDmat2[20, 53, i]  = BDmat2[20, 53, i] * mx[i]  # -mXcm
    BDmat2[20, 57, i]  = BDmat2[20, 57, i] * mx[i]  # mYcm
    BDmat2[20, 58, i]  = BDmat2[20, 58, i] * ix[i]  # i_Edg
    BDmat2[20, 59, i]  = BDmat2[20, 59, i] * ix[i]  # -i_cp
    BDmat2[20, 63, i]  = BDmat2[20, 63, i] * mx[i]  # -mXcm
    BDmat2[20, 64, i]  = BDmat2[20, 64, i] * ix[i]  # -i_cp
    BDmat2[20, 65, i]  = BDmat2[20, 65, i] * ix[i]  # i_Flp
    BDmat2[20, 67, i]  = BDmat2[20, 67, i] * mx[i]  # -mYcm
    BDmat2[20, 68, i]  = BDmat2[20, 68, i] * mx[i]  # mXcm
    BDmat2[20, 72, i]  = BDmat2[20, 72, i] * ix[i]  # i_plr

x = EDmat2[:, :, 0]
y = BDmat2[:, :, 0]

study2 = {'EDmat': EDmat2, 'BDmat': BDmat2, 'parameter': 'inertia', 'values': ix,
          'DLC': ['1.1_U4', '1.1_U6', '1.1_U8', '1.1_U10', '1.1_U12', '1.1_U14', '1.1_U16', '1.1_U18', '1.1_U20', '1.1_U22', '1.1_U24', '1.1_U25', '1.3_U23']}

"""Study 3: stiffness sensitivity    """
# num = 4
kx = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
num = len(kx)
mx = np.ones(num)
ix = np.ones(num)

EDmat3 = np.repeat(EDmat[:, :, np.newaxis], num, axis=2)
BDmat3 = np.repeat(BDmat[:, :, np.newaxis], num, axis=2)
for i in range(0, num):
    EDmat3[20, 3, i]   = EDmat3[20, 3, i]  * mx[i]  # BMassDen
    EDmat3[20, 4, i]   = EDmat3[20, 4, i]  * kx[i]  # FlpStff
    EDmat3[20, 5, i]   = EDmat3[20, 5, i]  * kx[i]  # EdgStff
    BDmat3[20, 1, i]   = BDmat3[20, 1, i]  * kx[i]  # K_ShrFlp
    BDmat3[20, 8, i]   = BDmat3[20, 8, i]  * kx[i]  # K_ShrEdg
    BDmat3[20, 15, i]  = BDmat3[20, 15, i] * kx[i]  # EA
    BDmat3[20, 22, i]  = BDmat3[20, 22, i] * kx[i]  # EI_Edg
    BDmat3[20, 29, i]  = BDmat3[20, 29, i] * kx[i]  # EI_Flp
    BDmat3[20, 36, i]  = BDmat3[20, 36, i] * kx[i]  # GJ
    BDmat3[20, 37, i]  = BDmat3[20, 37, i] * mx[i]  # m
    BDmat3[20, 42, i]  = BDmat3[20, 42, i] * mx[i]  # -mYcm
    BDmat3[20, 44, i]  = BDmat3[20, 44, i] * mx[i]  # m
    BDmat3[20, 48, i]  = BDmat3[20, 48, i] * mx[i]  # mXcm
    BDmat3[20, 51, i]  = BDmat3[20, 51, i] * mx[i]  # m
    BDmat3[20, 52, i]  = BDmat3[20, 52, i] * mx[i]  # mYcm
    BDmat3[20, 53, i]  = BDmat3[20, 53, i] * mx[i]  # -mXcm
    BDmat3[20, 57, i]  = BDmat3[20, 57, i] * mx[i]  # mYcm
    BDmat3[20, 58, i]  = BDmat3[20, 58, i] * ix[i]  # i_Edg
    BDmat3[20, 59, i]  = BDmat3[20, 59, i] * ix[i]  # -i_cp
    BDmat3[20, 63, i]  = BDmat3[20, 63, i] * mx[i]  # -mXcm
    BDmat3[20, 64, i]  = BDmat3[20, 64, i] * ix[i]  # -i_cp
    BDmat3[20, 65, i]  = BDmat3[20, 65, i] * ix[i]  # i_Flp
    BDmat3[20, 67, i]  = BDmat3[20, 67, i] * mx[i]  # -mYcm
    BDmat3[20, 68, i]  = BDmat3[20, 68, i] * mx[i]  # mXcm
    BDmat3[20, 72, i]  = BDmat3[20, 72, i] * ix[i]  # i_plr

x = EDmat3[:, :, 0]
y = BDmat3[:, :, 0]

study3 = {'EDmat': EDmat3, 'BDmat': BDmat3, 'parameter': 'stiffness',  'values': kx,
          'DLC': ['1.1_U4', '1.1_U6', '1.1_U8', '1.1_U10', '1.1_U12', '1.1_U14', '1.1_U16', '1.1_U18', '1.1_U20', '1.1_U22', '1.1_U24', '1.1_U25', '1.3_U23']}

"""Study 4: location sensitivity    """
L_segment = 3.54573  # m
m_70 = 1000 / L_segment  # kg/m3, at 70% span
slope = m_70/0.3
m0 = slope
span = EDmat[:, 0]
# m_add = m0 - span * slope  # linear
# mpoly = np.array([51497, -199850, 291941, -181858, 30191, 8080])  # assuming =1000 at 69% span
m_add = []
for i in span:
    m_add.append(51497*i**5 + -199850*i**4 + 291941*i**3 + -181858*i**2 + 30191*i + 8080)
m_add = np.asarray(m_add)
m_add /= L_segment
first = 6
last = 24
num = last-first
kx = 1
loc = span[first: last]

EDmat4 = np.repeat(EDmat[:, :, np.newaxis], num, axis=2)
BDmat4 = np.repeat(BDmat[:, :, np.newaxis], num, axis=2)
m=[]
for i in range(first, last):
    k = i-first
    mi = EDmat[i, 3]
    mx = (mi + m_add[i]) / mi
    ix = mx
    EDmat4[i, 3, k]   = EDmat4[i, 3, k]  * mx  # BMassDen
    EDmat4[i, 4, k]   = EDmat4[i, 4, k]  * kx  # FlpStff
    EDmat4[i, 5, k]   = EDmat4[i, 5, k]  * kx  # EdgStff
    BDmat4[i, 1, k]   = BDmat4[i, 1, k]  * kx  # K_ShrFlp
    BDmat4[i, 8, k]   = BDmat4[i, 8, k]  * kx  # K_ShrEdg
    BDmat4[i, 15, k]  = BDmat4[i, 15, k] * kx  # EA
    BDmat4[i, 22, k]  = BDmat4[i, 22, k] * kx  # EI_Edg
    BDmat4[i, 29, k]  = BDmat4[i, 29, k] * kx  # EI_Flp
    BDmat4[i, 36, k]  = BDmat4[i, 36, k] * kx  # GJ
    BDmat4[i, 37, k]  = BDmat4[i, 37, k] * mx  # m
    BDmat4[i, 42, k]  = BDmat4[i, 42, k] * mx  # -mYcm
    BDmat4[i, 44, k]  = BDmat4[i, 44, k] * mx  # m
    BDmat4[i, 48, k]  = BDmat4[i, 48, k] * mx  # mXcm
    BDmat4[i, 51, k]  = BDmat4[i, 51, k] * mx  # m
    BDmat4[i, 52, k]  = BDmat4[i, 52, k] * mx  # mYcm
    BDmat4[i, 53, k]  = BDmat4[i, 53, k] * mx  # -mXcm
    BDmat4[i, 57, k]  = BDmat4[i, 57, k] * mx  # mYcm
    BDmat4[i, 58, k]  = BDmat4[i, 58, k] * ix  # i_Edg
    BDmat4[i, 59, k]  = BDmat4[i, 59, k] * ix  # -i_cp
    BDmat4[i, 63, k]  = BDmat4[i, 63, k] * mx  # -mXcm
    BDmat4[i, 64, k]  = BDmat4[i, 64, k] * ix  # -i_cp
    BDmat4[i, 65, k]  = BDmat4[i, 65, k] * ix  # i_Flp
    BDmat4[i, 67, k]  = BDmat4[i, 67, k] * mx  # -mYcm
    BDmat4[i, 68, k]  = BDmat4[i, 68, k] * mx  # mXcm
    BDmat4[i, 72, k]  = BDmat4[i, 72, k] * ix  # i_plr
    m.append(mx)

x = EDmat4[:, :, 0]
y = BDmat4[:, :, 0]

study4 = {'EDmat': EDmat4, 'BDmat': BDmat4, 'parameter': 'location',  'values': loc,
          'DLC': ['1.1_U4', '1.1_U6', '1.1_U8', '1.1_U10', '1.1_U12', '1.1_U14', '1.1_U16', '1.1_U18', '1.1_U20', '1.1_U22', '1.1_U24', '1.1_U25', '1.3_U23']}

"""Study 5: spread mass sensitivity    """
# mass is spread along three stations
loc = [19, 20, 21]
mi = EDmat[loc, 3]  # kg/m3
L_segment = 3.54573  # m
m_joint_nom = 1000 / L_segment / 3  # kg/m3
num = 10
m_range = np.linspace(0.2, 2, num=num)
m_add = m_range * m_joint_nom
mx = np.zeros([3, num])
for i in range(0, len(mi)):
    mx[i, :] = (mi[i] + m_add) / mi[i]
ix = mx
kx = np.ones(num)
values = 1000 * m_range

EDmat5 = np.repeat(EDmat[:, :, np.newaxis], num, axis=2)
BDmat5 = np.repeat(BDmat[:, :, np.newaxis], num, axis=2)
for j in range(0, len(loc)):
    for i in range(0, num):
        EDmat1[loc[j], 3, i]   = EDmat1[loc[j], 3, i]  * mx[j, i]  # BMassDen
        BDmat1[loc[j], 37, i]  = BDmat1[loc[j], 37, i] * mx[j, i]  # m
        BDmat1[loc[j], 42, i]  = BDmat1[loc[j], 42, i] * mx[j, i]  # -mYcm
        BDmat1[loc[j], 44, i]  = BDmat1[loc[j], 44, i] * mx[j, i]  # m
        BDmat1[loc[j], 48, i]  = BDmat1[loc[j], 48, i] * mx[j, i]  # mXcm
        BDmat1[loc[j], 51, i]  = BDmat1[loc[j], 51, i] * mx[j, i]  # m
        BDmat1[loc[j], 52, i]  = BDmat1[loc[j], 52, i] * mx[j, i]  # mYcm
        BDmat1[loc[j], 53, i]  = BDmat1[loc[j], 53, i] * mx[j, i]  # -mXcm
        BDmat1[loc[j], 57, i]  = BDmat1[loc[j], 57, i] * mx[j, i]  # mYcm
        BDmat1[loc[j], 58, i]  = BDmat1[loc[j], 58, i] * ix[j, i]  # i_Edg
        BDmat1[loc[j], 59, i]  = BDmat1[loc[j], 59, i] * ix[j, i]  # -i_cp
        BDmat1[loc[j], 63, i]  = BDmat1[loc[j], 63, i] * mx[j, i]  # -mXcm
        BDmat1[loc[j], 64, i]  = BDmat1[loc[j], 64, i] * ix[j, i]  # -i_cp
        BDmat1[loc[j], 65, i]  = BDmat1[loc[j], 65, i] * ix[j, i]  # i_Flp
        BDmat1[loc[j], 67, i]  = BDmat1[loc[j], 67, i] * mx[j, i]  # -mYcm
        BDmat1[loc[j], 68, i]  = BDmat1[loc[j], 68, i] * mx[j, i]  # mXcm
        BDmat1[loc[j], 72, i]  = BDmat1[loc[j], 58, i] + BDmat1[loc[j], 65, i]  # i_plr = i_Edg + i_Flp
        # BDmat1[20, 72, i]  = BDmat1[20, 72, i] * ix[i]  # i_plr

x = EDmat1[:, :, 9]
y = BDmat1[:, :, 9]

study5 = {'EDmat': EDmat1, 'BDmat': BDmat1, 'parameter': 'spread_mass', 'values': values,
          'DLC': ['1.1_U4', '1.1_U6', '1.1_U8', '1.1_U10', '1.1_U12', '1.1_U14', '1.1_U16', '1.1_U18', '1.1_U20', '1.1_U22', '1.1_U24', '1.1_U25', '1.3_U23']}



study6 = {'EDmat': 1, 'BDmat': 1, 'parameter': 'test',  'values': [1, 2],
          'DLC': ['1.1_U4', '1.1_U6', '1.3_U23']}