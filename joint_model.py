import numpy as np

"""designs embedded bushing mechanical joint with minimum number of bolts
############### USER INPUT PARAMETERS #######################
joint location
joint type
############### SET INPUT PARAMETERS #######################"""
# safety factors
nprf = 1.2  # bolt static safety factor (proof) [-]. If this is too high, it seriously constrains the design. Keep it low, <= 1.2
ny   = 2    # insert static safety factor (yield) [-]
nf   = 2    # fatigue safety factor [-]
n0   = 1.2    # separation safety factor [-]. If this is too high, it seriously constrains the design. Keep it low, <= 1.2
ns   = 2    # shear safety factor [-]
# nDLC61 = 1.35  # DLC 6.1 load safety factor [-]

# M48 10.9 bolt properties (Shigley p.433) # kf = 3  # metric 10.9, rolled thread.
Sp_bolt = 830e6   # Pa
Sy_bolt = 940e6   # Pa
Su_bolt = 1040e6  # Pa
Se_bolt = 162e6   # Pa (for M1.6-36). Fully corrected so don't need kf
E_bolt  = 200e9   # Pa (medium carbon steel...)
d_bolt  = 0.048  # m
L_bolt  = 1  # m Assume a certain value...run some cases to figure out what is reasonable
Ad      = np.pi * d_bolt ** 2 / 4  # m2
At      = 1470 / 1e6  # m2
Ld      = L_bolt * 0.75
Lt      = L_bolt - Ld
m_bolt  = 15.15  # kg, bolt+washer, https://www.portlandbolt.com/technical/tools/bolt-weight-calculator/
n_bolt  = -2  # initialized
n_bolt_prev = -1  # initialized

# steel insert material properties
# material: Stainless Steel 440A, tempered @315C. Cold worked 304: 515/860. (http://www.matweb.com/search/datasheet_print.aspx?matguid=4f9c4c71102d4cd9b4c52622588e99a0)
p_insert  = 7800  # kg/m3
Sy_insert = 1650e6  # Pa
Su_insert = 1790e6  # Pa
Se_insert = 316e6  # Pa (Azom)
E_insert  = 210e9  # Pa
d_insert  = d_bolt * 2  # keeping the insert much larger than the bolt reduces bolt loads, which drive the design.
A_insert  = np.pi * (d_insert ** 2 - d_bolt ** 2) / 4
L_insert  = L_bolt
mu        = 0.5  # eng toolbox says 0.5-0.8 for clean, dry steel. Josh P recommended 0.3
V_insert  = A_insert * L_insert
m_insert  = V_insert * p_insert

# CFRP UD industry standard composite material properties (https://energy.sandia.gov/download/45350/)
Ss_sparcap = 30170000  # pa, direction 1 (along fibers)
p_sparcap  = 1600  # kg/m3

# geometric properties
h               = 0.6  # m, spar cap height (bolt to bolt)
bolt_spacing    = 3 * d_bolt
chord           = 3  # m
n_bolt_max      = chord//bolt_spacing  # max # bolts that can fit
t_adhesive      = 0.005  # m
V_adhesive      = np.pi * ((d_insert + 2 * t_adhesive) ** 2 - d_insert ** 2) / 4  # m3
w_hole          = d_bolt * 7 / 3
L1_hole         = d_bolt * 3
hi_hole         = d_bolt * 2
ply_drop_slope  = 1 / 8  # max for >45 plies dropped (otherwise 1/3) https://www.sciencedirect.com/science/article/pii/S135983680000038X. Derek used 1/40 slope
w_nom           = 0.8  # spar cap nominal width at 0.690
t_nom           = 0.02258  # spar cap nominal thickness at 0.690
t_max           = h/4  # spar cap max thickness
L_segment       = 3.54573  # m

# loads, will be WISDEM inputs. For now loosely based on Derek's report at 20m. These loads do not have safety factors applied. Need to apply DLC 1.1/6.1 safety factor (1.1-1.5?)
a = 0.1965
b = 0
c = 0.6448
eta = 0.69
kp = a*(1-eta)**2 + b*(1-eta) + c
Mflap_static    = 1.64e6  * 2  # Nm 50 for e50?
Mflap_fatigue   = Mflap_static * kp  # Nm
Fflap_static    = 1.5e5  * 2  # N
Fflap_fatigue   = Fflap_static * kp  # N
Medge_static    = 3.1e5  * 2  # Nm
Medge_fatigue   = Medge_static * kp  # Nm

# other parameters
itermax = 20  # max loop iterations

# 1- Calculate joint stiffness constant
k_bolt      = Ad * At * E_bolt / (Ad * Lt + At * Ld)  # bolt stiffness
k_insert    = A_insert * E_insert / L_bolt  # material stiffness.
C           = k_bolt / (k_bolt + k_insert)  # joint stiffness constant

# 2- Calculate preload (initialize to 70% proof)
Fi70p   = 0.7 * Sp_bolt * At  # N, per bolt. Need a high preload like this to resist separation. This means that the static bolt safety factor (nprf) needs to be low
Fi      = Fi70p

# 3- Calculate # bolts such that axial flap bolt forces > edge bolt forces
# Loop through number of bolts per spar cap, and calculate the following. When the flap static and fatigue loads both
# dominate, that is the minimum # bolts. Units are force per bolt ONLY HERE.
for n_bolt_min in range(3, int(np.ceil(n_bolt_max)//2*2+1), 2):
    N                           = int(np.floor(n_bolt_min / 2))
    N_array                     = np.linspace(1, N, N)
    Fax_flap_static_per_bolt    = Mflap_static / (h * n_bolt_min)
    Fax_edge_static_per_bolt    = N * Medge_static / (2 * bolt_spacing * np.sum(np.square(N_array)))
    Fax_flap_fatigue_per_bolt   = Mflap_fatigue / (h * n_bolt_min)
    Fax_edge_fatigue_per_bolt   = N * Medge_fatigue / (2 * bolt_spacing * np.sum(np.square(N_array)))
    if Fax_flap_fatigue_per_bolt > Fax_edge_fatigue_per_bolt and Fax_flap_static_per_bolt > Fax_edge_static_per_bolt:
        break

# 4- Calculate # fasteners needed to resist extreme and fatigue flap loads, and LATER: satisfy adhesive mean stress limit.
# Round up to nearest odd(?)

# a- joint static, fatigue loads per spar cap side
Fax_flap_static     = Mflap_static / h
Fax_flap_fatigue    = Mflap_fatigue / h
Fsh_flap_static     = Fflap_static / 2
Fsh_flap_fatigue    = Fflap_fatigue / 2

i = 0  # while loop counter
n_bolt_list = []
while n_bolt != n_bolt_prev:  # find a way to break out of a Fi-change-loop
    i += 1
    n_bolt_prev = n_bolt

    # b- calc # bolts & inserts to resist flap axial static loads
    # bolts
    n_bolt_flap_static = C * Fax_flap_static / (Sp_bolt * At / nprf - Fi)  # the bolt static safety factor (nprf) needs to be low to prevent the  (high) preload from overloading the bolt.
    # inserts. Could consider torsion here. Equation derived with MATLAB symbolic toolbox
    x3 = (ny*C**2*Fax_flap_static**2 - 2*ny*C*Fax_flap_static**2 + ny*Fax_flap_static**2 + 3*ny*Fsh_flap_static**2)/(np.sqrt(A_insert**2*C**2*Fax_flap_static**2*Sy_insert**2 - 2*A_insert**2*C*Fax_flap_static**2*Sy_insert**2 + A_insert**2*Fax_flap_static**2*Sy_insert**2 + 3*A_insert**2*Fsh_flap_static**2*Sy_insert**2 - 3*Fi**2*Fsh_flap_static**2*ny**2) + (-Fax_flap_static*Fi*ny + C*Fax_flap_static*Fi*ny))
    x4 = (ny*C**2*Fax_flap_static**2 - 2*ny*C*Fax_flap_static**2 + ny*Fax_flap_static**2 + 3*ny*Fsh_flap_static**2)/(np.sqrt(A_insert**2*C**2*Fax_flap_static**2*Sy_insert**2 - 2*A_insert**2*C*Fax_flap_static**2*Sy_insert**2 + A_insert**2*Fax_flap_static**2*Sy_insert**2 + 3*A_insert**2*Fsh_flap_static**2*Sy_insert**2 - 3*Fi**2*Fsh_flap_static**2*ny**2) - (-Fax_flap_static*Fi*ny + C*Fax_flap_static*Fi*ny))
    n_insert_flap_static = max([x3, x4])

    # c- calc # bolts & inserts needed to resist flap axial fatigue loads
    # bolts
    sig_i_bolt = Fi / At
    sig_a_bolt = Fax_flap_fatigue * C / At
    Sa_bolt = Se_bolt - Se_bolt / Su_bolt * sig_i_bolt
    n_bolt_flap_fatigue = nf * sig_a_bolt / Sa_bolt
    # inserts. Could consider torsion here. Removing because insert forces are far lower in static, add this back in if
    # that changes.
    sig_i_insert = Fi/A_insert
    Sa_insert = Se_insert - Se_insert/Su_insert*sig_i_insert
    n_insert_flap_fatigue = (nf/Sa_insert)**(1/2)*((Fax_flap_fatigue*(1-C)/A_insert)**2 + 3*(Fsh_flap_fatigue/A_insert)**2)**(1/4)

    # d - calc #bolts/inserts needed for spar cap to resist insert pull-out
    n_bolt_pullout = 2 * ns * Fax_flap_static / (Ss_sparcap * np.pi * (d_insert + 2 * t_adhesive))

    # e - take max  bolts needed as # bolt-insert pairs
    n_bolt = np.ceil(np.max([n_bolt_flap_fatigue, n_bolt_flap_static, n_insert_flap_static, n_insert_flap_fatigue, n_bolt_pullout, n_bolt_min]))
    n_bolt_list.append(n_bolt)

    # check for negatives. This implies that the loads magnitudes are imbalanced and out of range for the calculation
    if n_bolt_flap_static < 0 or n_bolt_flap_fatigue < 0 or n_bolt_pullout < 0:
        print('Warning: negative bolt number found. This implies that the preload exceeds the static load requirements. Please check inputs (separation and static safety factors)')

    # 5- calculate preload to prevent separation and bolt shear. Make sure it's not requiring a preload that's too close
    # to proof load....this could constrain the load the joint can handle.
    Fi_sep = n0 * Fax_flap_static * (1 - C) / n_bolt  # because separation is calculated based on extreme static loading, the bolt static safety factor (nprf) needs to be low.
    Fi_sh = Fsh_flap_static / (mu * n_bolt)  # mu: friction coefficient of insert, can assume 0.3 for metal.
    if Fi_sep > Fi70p:
        print('Warning, separation preload requirement (', Fi_sep, 'N) > 70% bolt proof load and will be limited to prevent overloading.')
    if Fi_sh > Fi70p:
        print('Warning, shear preload requirement (', Fi_sh, 'N) > 70% bolt proof load and will be limited to prevent overloading.')
    Fi = np.min([np.max([Fi_sh, Fi_sep]), Fi70p])
    if i > itermax:  # if iteration is stuck in an Fi-driven loop, then take the max # bolts required by loop
        print('Solution oscillating between bolt numbers. Choosing the maximum of these.')
        seq = itermax
        for x in range(2, itermax//2):
            if n_bolt_list[0:x] == n_bolt_list[x:2*x]:
                seq = x
        n_bolt = max(n_bolt_list[-seq:])
    if n_bolt > n_bolt_max:
        print('Warning. Unable to accommodate # bolts required (', n_bolt, '). Limiting to max # bolts that can fit in '
                                                                           'the cross section (', n_bolt_max, ').')
        n_bolt = n_bolt_max

    print('n_bolt_flap_fatigue', n_bolt_flap_fatigue)
    print('n_bolt_flap_static', n_bolt_flap_static)
    print('n_insert_flap_static', n_insert_flap_static)
    print('n_insert_flap_fatigue', n_insert_flap_fatigue)
    print('n_bolt_pullout', n_bolt_pullout)
    print('n_bolt_min', n_bolt_min)
    print('n_bolt', n_bolt)

    print('Fi_sep', Fi_sep)
    print('Fi_sh', Fi_sh)
    print('Fi70p', Fi70p)
    print('Fi', Fi)
    print('################################################')
    print('################################################')

# 6- loop through steps 4b-5 until n_bolt converges. Result is n_bolt

# 7- calc spar cap dimensions needed to resist loads. Neglect fatigue because composites handle it better than
# metal, generally. Consider shearing due to shear out on a z-line on the outside of the adhesive, in the
# middle of the bolt. Also consider shear at bolt head hole. ***OR, the spar cap can be sized with WISDEM as usual.***

# a- insert shear out.
t1 = 2 * Fsh_flap_static * ns / (L_insert * n_bolt * Ss_sparcap)

# b- shear at bolt head hole. Because carbon fiber is so isotropic, and will fail in shear
t2 = Fsh_flap_static * ns / (bolt_spacing * Ss_sparcap * n_bolt) + w_hole * hi_hole / bolt_spacing

# c-spar cap dimensions
t = np.max([t1, t2, t_nom])
if t > t_max:
    print('Warning, spar cap thickness (', t, 'm) greater than 1/4 cross section height and will be limited')
    t = t_max
w = np.max([n_bolt * bolt_spacing, w_nom])

# 8- once width and thickness are found, the required ply drop length will determine how long the bulge in the spar cap
# is, and inform spar cap total mass. ***OR, the spar cap can be sized with WISDEM as usual.***
h_hole = t / 2 + 7 / 6 * d_bolt
dt = t - t_nom
L_transition = dt / ply_drop_slope  # hopefully less than 3m or whatever.
if L_transition > L_segment:
    print('Warning. Segments too short to accommodate ply drop requirements')

# 9- mass calcs: Spar cap mass subtraction where inserts, bolts, adhesive are, inserts, bolts
n_bolt *= 2  # consider bolts in each spar cap
m_bolt_tot = n_bolt * m_bolt
m_insert_tot = n_bolt * m_insert
V_bolthead_hole = h_hole * np.pi * w_hole ** 2 / 4
V_bolthead_hole_tot = V_bolthead_hole * n_bolt
V_insert_tot = V_insert * n_bolt
V_cutout = V_insert_tot + V_bolthead_hole_tot
m_cutout = V_cutout * p_sparcap
m_tot = m_bolt_tot + m_insert_tot - m_cutout
pp = 0
print('t', t)
print('w', w)
print('L_transition', L_transition)
print('m_tot', m_tot)
print('n_bolt', n_bolt)