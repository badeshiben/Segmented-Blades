import numpy as np
import openmdao.api as om



class JointSizing(om.ExplicitComponent):
    """
    Compute the minimum joint size given the blade loading.

    Parameters
    ----------
    load_factor : float
        Factor to multiply input loads by
    nprf : float
        Proof load safety factor for bolts. If this is too high, it seriously constrains the design. Keep it low, <= 1.2
    ny : float
        Yield safety factor for inserts.
    nf : float
        Fatigue safety factor for bolts/inserts.
    n0 : float
        Separation safety factor for joint. If this is too high, it seriously constrains the design. Keep it low, <= 1.2
    ns : float
        Shear safety factor for joint.
    nDLC61 : float
        Safety factor for extreme loads from IEC 61400 design load case 6.1. =1.35

    Returns
    -------
    L_transition_joint : float, [m]
        Required length to accommodate spar cap size increase at segmentation joint
    m_add_joint : float, [kg]
        Mass of bolts + inserts minus mass of spar cap cutouts for segmentation joint (spar cap size change will add mass too)
    n_bolt_joint : int
        Required number of bolts for segmentation joint
    t_sparcap_joint : float, [m]
        Required sparcap thickness at segmentation joint
    w_sparcap_joint : float, [m]
        Required sparcap width at segmentation joint

    """
    def initialize(self):
        self.options.declare("rotorse_options")

    def setup(self):

        rotorse_options = self.options["rotorse_options"]

        # safety factors
        self.add_input('load_factor', val=1, units=None)  # do this for inputs that are not available in the yaml
        self.add_input('nprf', val=1.2, units=None) # bolt static safety factor (proof) [-]. If this is too high, it seriously constrains the design. Keep it low, <= 1.2
        self.add_input('ny', val=2, units=None)
        self.add_input('ns', val=2, units=None)
        self.add_input('n0', val=1.2, units=None)
        self.add_input('nf', val=2, units=None)

        # M48 10.9 bolt properties (Shigley p.433) # kf = 3  # metric 10.9, rolled thread.
        self.add_input('Sp_bolt', val=830e6, units='Pa')
        self.add_input('Sy_bolt', val=940e6, units='Pa')
        self.add_input('Su_bolt', val=1040e6, units='Pa')
        self.add_input('Se_bolt', val=162e6, units='Pa')  # (for M1.6-36). Fully corrected so don't need kf
        self.add_input('E_bolt', val=200e9, units='Pa')  # medium carbon steel
        self.add_input('d_bolt', val=0.048)
        self.add_input('L_bolt', val=1, units='m')
        self.add_input('m_bolt', val=15.15)  # kg, bolt+washer, https://www.portlandbolt.com/technical/tools/bolt-weight-calculator/

        # steel insert material properties
        # material: Stainless Steel 440A, tempered @315C. Cold worked 304: 515/860. (http://www.matweb.com/search/datasheet_print.aspx?matguid=4f9c4c71102d4cd9b4c52622588e99a0)
        self.add_input('density_insert', val=rotorse_options['density_insert'], units='kg/m**3')
        self.add_input('Sy_insert', val=rotorse_options['Sy_insert'], units='Pa')
        self.add_input('Su_insert', val=rotorse_options['Su_insert'], units='Pa')
        self.add_input('Se_insert', val=rotorse_options['Se_insert'], units='Pa')  # Azom
        self.add_input('E_insert', val=rotorse_options['E_insert'], units='Pa')
        self.add_input('mu_joint', val=0.5, units='Pa')  # eng toolbox says 0.5-0.8 for clean, dry steel

        # CFRP UD industry standard composite material properties (https://energy.sandia.gov/download/45350/)
        self.add_input('Ss_sparcap', val=rotorse_options['Ss_sparcap'], units='Pa')  # direction 1: along fibers
        self.add_input('density_sparcap', val=rotorse_options['density_sparcap'], units='kg/m**3')

        # geometric properties
        self.add_input('bolt_spacing_dia', val=3) # units: bolt diameters
        self.add_input('ply_drop_slope', val=1/8, units=None) # Required ply drop slope. max for >45 plies dropped (otherwise 1/3) https://www.sciencedirect.com/science/article/pii/S135983680000038X.
        self.add_input('t_adhesive', val=0.005, units='m') # insert-sparcap adhesive
        self.add_input('t_max_sparcap', val=1/4)# maximum spar cap thickness. Units: spar cap height
        self.add_input('w_nom', val=rotorse_options['spar_cap_ss_width'], units='m')
        self.add_input('t_nom', val=rotorse_options['spar_cap_ss_thickness'], units='m')
        self.add_input('chord', val=rotorse_options['chord_length'], units='m')
        self.add_input('h', val=rotorse_options['spar_cap_height'], units='m')
        self.add_input('L_segment', val=rotorse_options['segment_length'], units='m')
        self.add_input('eta', val=rotorse_options['blade_station'], units=None)

        # blade ultimate loads
        self.add_input('Mflap_static', val=rotorse_options['Mflap_ult'], units='N*m')
        self.add_input('Medge_static', val=rotorse_options['Medge_ult'], units='N*m')
        self.add_input('Fflap_static', val=rotorse_options['Fflap_ult'], units='N*m')

        # fatigue load calculating factors
        self.add_input('a', val=0.1965, units=None)
        self.add_input('b', val=0, units=None)
        self.add_input('c', val=0.6448, units=None)

        # max # iterations
        self.add_input('itermax', val=20, units=None)

        self.add_output('t_joint', val=0, units='m', desc='Required sparcap thickness at segmentation joint')
        self.add_output('w_joint', val=0, units='m', desc='Required sparcap width at segmentation joint')
        self.add_output('L_transition_joint', val=0, units='m', desc='Required length to accommodate spar cap size increase at segmentation joint')
        self.add_output('n_bolt_joint', val=0, units=None, desc='Required number of bolts for segmentation joint')
        self.add_output('m_add_joint', val=0, units='kg', desc='Mass of bolts + inserts minus mass of spar cap cutouts for segmentation joint')

    def compute(self, inputs, outputs):
        load_factor = inputs['load_factor']
        nprf = inputs['nprf']
        ny = inputs['ny']
        nf = inputs['nf']
        n0 = inputs['n0']
        ns = inputs['ns']

        #nDLC61 = inputs['nDLC61']
        Sp_bolt = inputs['Sp_bolt']
        Sy_bolt = inputs['Sy_bolt']
        Su_bolt = inputs['Su_bolt']
        Se_bolt = inputs['Se_bolt']
        E_bolt = inputs['E_bolt']
        d_bolt = inputs['d_bolt']
        L_bolt = inputs['L_bolt']
        m_bolt = inputs['m_bolt']

        p_insert = inputs['density_insert']
        Sy_insert = inputs['Sy_insert']
        Su_insert = inputs['Su_insert']
        Se_insert = inputs['Se_insert']
        E_insert = inputs['E_insert']
        mu = inputs['mu_joint']

        Ss_sparcap = inputs['Ss_sparcap']
        p_sparcap = inputs['density_sparcap']

        bolt_spacing_dia = inputs['bolt_spacing_dia']
        ply_drop_slope = inputs['ply_drop_slope']
        t_adhesive = inputs['t_adhesive']
        t_max_sparcap = inputs['t_max_sparcap']

        a = inputs['a']
        b = inputs['b']
        c = inputs['c']

        # bolt properties
        Ad = np.pi * d_bolt ** 2 / 4  # m2
        At = 1470 / 1e6  # m2
        Ld = L_bolt * 0.75
        Lt = L_bolt - Ld
        n_bolt = -2  # initialized
        n_bolt_prev = -1  # initialized
        bolt_spacing = bolt_spacing_dia * d_bolt

        d_insert = d_bolt * 2  # keeping the insert much larger than the bolt reduces bolt loads, which drive the design.
        A_insert = np.pi * (d_insert ** 2 - d_bolt ** 2) / 4
        L_insert = L_bolt
        mu = 0.5  # eng toolbox says 0.5-0.8 for clean, dry steel.
        V_insert = A_insert * L_insert
        m_insert = V_insert * p_insert

        # geometric properties
        h = 0.6  # m, spar cap height (bolt to bolt)
        chord = 3  # m
        n_bolt_max = chord // bolt_spacing  # max # bolts that can fit
        # V_adhesive = np.pi * ((d_insert + 2 * t_adhesive) ** 2 - d_insert ** 2) / 4  # m3
        w_hole = d_bolt * 7 / 3
        hi_hole = d_bolt * 2
        w_nom = 0.8  # spar cap nominal width at 0.690
        t_nom = 0.02258  # spar cap nominal thickness at 0.690
        t_max = h * t_max_sparcap  # spar cap max thickness
        L_segment = 3.54573  # m

        # loads, will be WISDEM inputs. For now loosely based on Derek's report at 20m. These loads do not have safety factors applied. Need to apply DLC 1.1/6.1 safety factor (1.1-1.5?)
        a = 0.1965
        b = 0
        c = 0.6448
        eta = 0.69
        kp = a * (1 - eta) ** 2 + b * (1 - eta) + c
        Mflap_static = 1.64e6 * load_factor  # Nm 50 for e50?
        Mflap_fatigue = Mflap_static * kp  # Nm
        Fflap_static = 1.5e5 * load_factor  # N
        Fflap_fatigue = Fflap_static * kp  # N
        Medge_static = 3.1e5 * load_factor  # Nm
        Medge_fatigue = Medge_static * kp  # Nm

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
        V_insert_cutout_tot = np.pi * d_insert ** 2 / 4 * L_insert * n_bolt
        V_cutout = V_insert_cutout_tot + V_bolthead_hole_tot
        m_cutout = V_cutout * p_sparcap
        m_add = m_bolt_tot + m_insert_tot - m_cutout

        outputs['L_transition_joint'] = L_transition
        outputs['t_joint'] = t
        outputs['w_joint'] = w
        outputs['n_bolt_joint'] = n_bolt
        outputs['m_add_joint'] = m_add

if __name__ == "__main__":

    test_dict = {'density_insert': 7800, # rotorse.rc.rho[INDEX] # There are names. Use them to find the right index I guess. why no materials.rho?
                 'Sy_insert': 1650e6,    # materials.Xt[INDEX]...what about materials.sigma_y?xu
                 'Su_insert': 1790e6,    # drivese.Xy_mat (maybe????)
                 'Se_insert': 316e6,   # not defined in YAML
                 'E_insert': 210e9,   # materials.E[INDEX]
                 'Ss_sparcap': 30170000,  # why no materials.Xs?
                 'density_sparcap': 1600,  # rotorse.rc.rho[INDEX] # There are names. Use them to find the right index I guess. why no materials.rho?
                 'spar_cap_height': 0.6,  # would need WISDEM to calculate
                 'chord_length': 3,       # would need WISDEM to calculate
                 'spar_cap_ss_width': 0.8,  #rotorse.rs.brs.layer_end_nd[sparcap_SS_layer_#][station]-rotorse.rs.brs.layer_start_nd[sparcap_SS_layer_#][station]. Index Reversed? Need to calculate length from arc coordinates. May need WISDEM to calculate.
                 'spar_cap_ss_thickness': 0.02258, # rotorse.rs.brs.layer_thickness[sparcap_SS_layer_#][station]. Index Reversed? How is this reduced to one value? Otherwise probably need WISDEM to calculate
                 'segment_length': 3.54573,  # station differences in yaml?
                 'blade_station': 0.69,      # input from user? Choose from yaml? eventually from WISDEM if opt location.
                 'Mflap_ult': 1.64e6,  # WISDEM calculates
                 'Fflap_ult': 1.5e5,   # WISDEM calculates
                 'Medge_ult': 3.1e5    # WISDEM calculates
                 }

    model = om.Group()
    model.add_subsystem('jt', JointSizing(rotorse_options=test_dict)) #rotorse_options=modeling_options["WISDEM"]["RotorSE"]
    prob = om.Problem(model)
    prob.setup(derivatives=False)
    prob.set_val('jt.load_factor', 2)
    prob.run_model()
    print('t_joint', prob.get_val('jt.t_joint'))
    print('w_joint', prob.get_val('jt.w_joint'))
    print('L_transition_joint', prob.get_val('jt.L_transition_joint'))
    print('n_bolt_joint', prob.get_val('jt.n_bolt_joint'))
    print('m_add_joint', prob.get_val('jt.m_add_joint'))