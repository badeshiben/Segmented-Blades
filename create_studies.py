import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import fastlib
import weio

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
m_joint_nom = 2000 / L_segment  # kg/m3
num = 10
m_range = np.linspace(0.2, 2, num=num)
m_add = m_range * m_joint_nom
mx = (mi + m_add) / mi
ix = mx
kx = np.ones(num)
mult = m_range

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
    BDmat1[20, 72, i]  = BDmat1[20, 72, i] * ix[i]  # i_plr

x = EDmat1[:, :, 0]
y = BDmat1[:, :, 0]

study1 = {'EDmat': EDmat1, 'BDmat': BDmat1, 'case': 'mass', 'multipliers': mult, 'num': num}

"""Study 2: inertia sensitivity    """
num = 10
ix = np.linspace(1, 5.5, num=num)
i_add = m_range * m_joint_nom
mx = np.ones(num)
kx = np.ones(num)
mult = ix

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

study2 = {'EDmat': EDmat2, 'BDmat': BDmat2, 'case': 'inertia', 'multipliers': mult, 'num': num}

"""Study 3: stiffness sensitivity    """
num = 10
kx = np.linspace(1, 5.5, num=num)
k_add = m_range * m_joint_nom
mx = np.ones(num)
ix = np.ones(num)
mult = kx

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

study3 = {'EDmat': EDmat3, 'BDmat': BDmat3, 'case': 'stiffness', 'multipliers': mult, 'num': num}

 # K_ShrFlp = 1
 # K_ShrEdg = 1
 # EA = 1
 # EI_Edg = 1
 # EI_Flp = 1
 # GJ = 1
 # m_add = 1
 # Xcm = 1
 # Ycm = 1
# i_Edg = 1
# i_Flp = 1
# i_plr = i_Flp + i_Edg
# i_cp = 1
#
# BDmat[20, 1] = K_ShrFlp
# BDmat[20, 8] = K_ShrEdg
# BDmat[20, 15] = EA
# BDmat[20, 22] = EI_Edg
# BDmat[20, 29] = EI_Flp
# BDmat[20, 36] = GJ