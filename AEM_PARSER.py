# ============================================================================
"""             Advanced Electrolyte Model (AEM) PARSER v1.1.0             """
"""            © 2024 Ridgetop Group, Inc., All Rights Reserved            """
# ============================================================================

## Import Libraries
import os
import json
import sys
import threading
import time
from typing import List

## aem_run CLASS
class aem_run:
    def __init__(self):
        self.name = None
        self.report01 : aem_report01 = aem_report01()
        self.report02 : aem_report02 = aem_report02()
        self.report03 : aem_report03 = aem_report03()
        self.report04 : aem_report04 = aem_report04()
        self.report05 : aem_report05 = aem_report05()
        self.report06 : aem_report06 = aem_report06()
        self.report10 : aem_report10 = aem_report10()
        self.report11 : aem_report11 = aem_report11()
        self.report12 : aem_report12 = aem_report12()
        self.report13 : aem_report13 = aem_report13()
        self.report14 : aem_report14 = aem_report14()
        self.report15 : aem_report15 = aem_report15()
        self.report16 : aem_report16 = aem_report16()
        self.report17 : aem_report17 = aem_report17()
        self.report18 : aem_report18 = aem_report18()
        self.report19 : aem_report19 = aem_report19()
        self.report20 : aem_report20 = aem_report20()
    def parse_run(self, runDirPath):
        reports = os.listdir(runDirPath)
        for report in reports:
            parseReport(os.sep.join([runDirPath, report]), self)

## aem_report CLASS
class aem_report:
    def __init__(self):
        self.path : str = ''
        self.version = '2.24.3'
        self.items = []
        self.exists = False
        self.isEmpty = False
    def all_json(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        return json.dumps(all, indent=4)

r01var_2242 = [
            'solvent_comp','salt_comp','temperature','m2','c2','c2_eff_trans','wt_fr_salt','mole_fr_salt','density',
            'visc','sig1','sig2','s_plus','rational_act_coeff','diff_coeff','spec_cond','t_plus_a', 't_plus_b', 
            'dissoc_si', 'dissoc_ti'
            ] #for 2.24.2
r01var = [
            'solvent_comp','salt_comp','temperature','m2','c2','c2_eff_trans','wt_fr_salt','mole_fr_salt','density','visc',
            'sig1','sig2','s_plus','rational_act_coeff','diff_coeff','spec_cond','t_plus_a', 't_plus_b', 'salt_dissoc_si', 
            'salt_dissoc_ip', 'dissoc_ti'
         ] #for 2.24.3
r02var = [
            'solvent_comp','salt_comp','temperature','m2','c2','cmeff','alphanet','cation','anion','ip','ti','fcip','gamma',
            'y','y_bar','osmotic_coeff_molal','osmotic_coeff_molar','solvent_activity','kip','kti','ksol','adj_solvent_activity',
            'adj_phi','adj_gamma','fvpd'
         ]
r03var = [
            'solvent_comp','salt_comp','temperature','m2','c2','gfe_cation','gfe_anion','se_cation','se_anion','rp_solution',
            'rp_solvent','alpha1','alpha3','energy_sum','energy_ave','desolve_t'
         ]
r04var = [
            'solvent_comp','salt_comp','temperature','m2','c2','volsoft','fcomp','fsolv','fdiff12','d_plus','d_minus',
            'd_minus_bare','dnernst','dapp','d_ip','d_ti','d_solvent','thermodynamic_factor'
         ]
r05var_2242 = [
            'solvent_comp','salt_comp','temperature','m2','c2','c2_pseudo','density','visc','rational_act_coef_y','diffusion_coeff',
            'specific_conductivity','t_plus','t_minus','fhop_plus','fhop_minus','pos_atm','walden_log_1_over_visc','walden_log_cond',
            'walden_product','thermal_conductivity'
        ] #for 2.24.2
r05var = [
            'solvent_comp','salt_comp','temperature','m2','c2','c2_eff_trans','c2_pseudo','density','visc','rational_act_coef_y',
            'diffusion_coeff','specific_conductivity','t_plus','t_minus','fhop_plus','fhop_minus','pos_atm','walden_log_1_over_visc',
            'walden_log_cond','walden_product','thermal_conductivity'
         ] #for 2.24.3
r06var = [
            'solvent_comp','salt_comp','temperature','salt_molality','one_over_visc','k_t_plus','diffusivity_bulk_elec','li_step_full',
            'li_step_solv','kip','kti','ksolv','solvent_activity','gamma'
         ]
r10var = [
            'solvent_comp','salt_comp','temperature','surface_charge_density','cell_voltage_at_start_of_pulse','salt_concentration_basis', 
            'pulse_type','electrolyte_rel_perm_at_salt_conc','dipole_moment_data','solvent_diameter', 'equivalent_charge_on_solvent_dipole', 
            'sei_thickness', 'sei_porosity', 'sei_relative_permittivity','r', 'eff_surface_ch_density_at_r', 'solution_rel_perm_electrolyte_plus_sch', 
            'ave_r_solution_rel_perm_electrolyte_plus_sch', 'electric_field_per_sch', 'repulsive_energy_sch_to_dipole', 'cell_voltage'
         ]
r11var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','cation_eff_dia', 'anion_eff_dia', 's_plus_th', "s_minus_th", 'solvent_avail_thermo', 
            'solvent_avail_msa_hs', 'solvent_be_to_cation', 'solvent_be_to_anion', 'communal_solvation_factor', 'debye_relaxation_time', 
            'fraction_of_free_liquid_in_solvent'
         ]
r12var_2242 = [
               'solvent_comp','salt_comp','temperature','m2', 'c2','cation_solvent_one', 'cation_solvent_two', 'cation_solvent_three', 
               "cation_solvent_four", 'cation_solvent_five','anion_solvent_one', 'anion_solvent_two', 'anion_solvent_three', 
               "anion_solvent_four", 'anion_solvent_five'
        ]
r12var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','cation_solvent_one', 'cation_solvent_two', 'cation_solvent_three', 
            "cation_solvent_four", 'cation_solvent_five','cation_solvent_six', 'cation_solvent_seven', 'cation_solvent_eight', 
            "cation_solvent_nine", 'cation_solvent_ten','anion_solvent_one', 'anion_solvent_two', 'anion_solvent_three', 
            "anion_solvent_four", 'anion_solvent_five', 'anion_solvent_six', 'anion_solvent_seven', 'anion_solvent_eight', 
            "anion_solvent_nine", 'anion_solvent_ten'
         ]
r13var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','cation_factor_one', 'cation_factor_two', 'cation_factor_three', 
            "cation_factor_four", 'cation_factor_five','cation_factor_six', 'cation_factor_seven','anion_factor_one', 'anion_factor_two', 
            'anion_factor_three', "anion_factor_four", 'anion_factor_five','anion_factor_six', 'anion_factor_seven'
         ]
r14var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','full_li_step_parameter', 'partial_li_step_parameter']
r15var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','10_v1', '10_t1','20_v1', '20_t1','40_v1', '40_t1','80_v1',
            '80_t1','160_v1', '160_t1','320_v1', '320_t1', 'vsolv', 'tsolv'
         ]
r16var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','surface_tension', 'surface_ten_viscosity', '0.02_micron', 
            '0.05_micron', '0.1_micron', '0.2_micron','0.5_micron','1_micron','2_micron','5_micron','10_micron','20_micron'
         ]
r17var = [
            'solvent_comp','salt_comp','temperature','time_s', '0.02_micron', '0.05_micron', '0.1_micron', '0.2_micron',
            '0.5_micron','1_micron','2_micron','5_micron','10_micron','20_micron'
         ]
r18var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','be1', 'be2', 'be3', 'be4', 'be5', 'be6','be_sum','dt1', 
            'dt2', 'dt3', 'dt4', 'dt5', 'dt6','dt_sum','t_lambda'
         ]
r19var = [
            'solvent_comp','salt_comp','temperature','m2', 'c2','be1', 'be2', 'be3', 'be4', 'be5', 'be6','be_sum','dt1',
             'dt2', 'dt3', 'dt4', 'dt5', 'dt6','dt_sum','t_lambda'
         ]
r20var = [
            'solvent_comp','salt_comp','temperature','m2_bulk', 'm2_non_cs', 'm2_cs', 'y_free','y_non_cs','y_cs',
            'cs_factor', 'n_s_plus_bulk','n_s_plus_cs','n_s_plus_ave','be_plus_bulk','be_plus_cs','be_plus_ave',
            'n_s_cs_0','n_s_cs_ave','n_s_non_cs', 'ratio_of_n_solv_cs_to_m2_cs'
         ]

def parse_float(str):
    try:
        return float(str)
    except ValueError:
        return float('nan')

## aem_reportXX CLASS (XX - Report No.)
class aem_report01(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        if (self.version == '2.24.2'):
            c = f'{','.join(r01var_2242)}\n'
            for d in all:
                c += f'{d[r01var_2242[0]]},{d[r01var_2242[1]]},{d[r01var_2242[2]]},{d[r01var_2242[3]]},{d[r01var_2242[4]]},'
                c += f'{d[r01var_2242[5]]},{d[r01var_2242[6]]},{d[r01var_2242[7]]},{d[r01var_2242[8]]},{d[r01var_2242[9]]},'
                c += f'{d[r01var_2242[10]]},{d[r01var_2242[11]]},{d[r01var_2242[12]]},{d[r01var_2242[13]]},{d[r01var_2242[14]]},'
                c += f'{d[r01var_2242[15]]},{d[r01var_2242[16]]},{d[r01var_2242[17]]},{d[r01var_2242[18]]},{d[r01var_2242[19]]}\n'
        else:
            c = f'{','.join(r01var)}\n'
            for d in all:
                c += f'{d[r01var[0]]},{d[r01var[1]]},{d[r01var[2]]},{d[r01var[3]]},{d[r01var[4]]},'
                c += f'{d[r01var[5]]},{d[r01var[6]]},{d[r01var[7]]},{d[r01var[8]]},{d[r01var[9]]},'
                c += f'{d[r01var[10]]},{d[r01var[11]]},{d[r01var[12]]},{d[r01var[13]]},{d[r01var[14]]},'
                c += f'{d[r01var[15]]},{d[r01var[16]]},{d[r01var[17]]},{d[r01var[18]]},{d[r01var[19]]},{d[r01var[20]]}\n'
        return c   
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        if (self.version == '2.24.2'):
            c = f'{','.join(r01var_2242)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r01var_2242[0]]},{d[r01var_2242[1]]},{d[r01var_2242[2]]},{d[r01var_2242[3]]},{d[r01var_2242[4]]},'
                c += f'{d[r01var_2242[5]]},{d[r01var_2242[6]]},{d[r01var_2242[7]]},{d[r01var_2242[8]]},{d[r01var_2242[9]]},'
                c += f'{d[r01var_2242[10]]},{d[r01var_2242[11]]},{d[r01var_2242[12]]},{d[r01var_2242[13]]},{d[r01var_2242[14]]},'
                c += f'{d[r01var_2242[15]]},{d[r01var_2242[16]]},{d[r01var_2242[17]]},{d[r01var_2242[18]]},{d[r01var_2242[19]]}\n'
                f.write(c)
        else: #2.24.3
            c = f'{','.join(r01var)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r01var[0]]},{d[r01var[1]]},{d[r01var[2]]},{d[r01var[3]]},{d[r01var[4]]},'
                c += f'{d[r01var[5]]},{d[r01var[6]]},{d[r01var[7]]},{d[r01var[8]]},{d[r01var[9]]},'
                c += f'{d[r01var[10]]},{d[r01var[11]]},{d[r01var[12]]},{d[r01var[13]]},{d[r01var[14]]},'
                c += f'{d[r01var[15]]},{d[r01var[16]]},{d[r01var[17]]},{d[r01var[18]]},{d[r01var[19]]},,{d[r01var[20]]}\n'
                f.write(c)
        f.close()
        
class aem_report02(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r02var)}\n'
        for d in all:
            c += f'{d[r02var[0]]},{d[r02var[1]]},{d[r02var[2]]},{d[r02var[3]]},{d[r02var[4]]},'
            c += f'{d[r02var[5]]},{d[r02var[6]]},{d[r02var[7]]},{d[r02var[8]]},{d[r02var[9]]},'
            c += f'{d[r02var[10]]},{d[r02var[11]]},{d[r02var[12]]},{d[r02var[13]]},{d[r02var[14]]},'
            c += f'{d[r02var[15]]},{d[r02var[16]]},{d[r02var[17]]},{d[r02var[18]]},{d[r02var[19]]},'
            c += f'{d[r02var[20]]},{d[r02var[21]]},{d[r02var[22]]},{d[r02var[23]]},{d[r02var[24]]}\n'
        return c 
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r02var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r02var[0]]},{d[r02var[1]]},{d[r02var[2]]},{d[r02var[3]]},{d[r02var[4]]},'
            c += f'{d[r02var[5]]},{d[r02var[6]]},{d[r02var[7]]},{d[r02var[8]]},{d[r02var[9]]},'
            c += f'{d[r02var[10]]},{d[r02var[11]]},{d[r02var[12]]},{d[r02var[13]]},{d[r02var[14]]},'
            c += f'{d[r02var[15]]},{d[r02var[16]]},{d[r02var[17]]},{d[r02var[18]]},{d[r02var[19]]},'
            c += f'{d[r02var[20]]},{d[r02var[21]]},{d[r02var[22]]},{d[r02var[23]]},{d[r02var[24]]}\n'
            f.write(c)
        f.close()

class aem_report03(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r03var)}\n'
        for d in all:
            c += f'{d[r03var[0]]},{d[r03var[1]]},{d[r03var[2]]},{d[r03var[3]]},{d[r03var[4]]},'
            c += f'{d[r03var[5]]},{d[r03var[6]]},{d[r03var[7]]},{d[r03var[8]]},{d[r03var[9]]},'
            c += f'{d[r03var[10]]},{d[r03var[11]]},{d[r03var[12]]},{d[r03var[13]]},{d[r03var[14]]},'
            c += f'{d[r03var[15]]}\n'
        return c  
    def save_all_csv(self,path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r03var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r03var[0]]},{d[r03var[1]]},{d[r03var[2]]},{d[r03var[3]]},{d[r03var[4]]},'
            c += f'{d[r03var[5]]},{d[r03var[6]]},{d[r03var[7]]},{d[r03var[8]]},{d[r03var[9]]},'
            c += f'{d[r03var[10]]},{d[r03var[11]]},{d[r03var[12]]},{d[r03var[13]]},{d[r03var[14]]},'
            c += f'{d[r03var[15]]}\n'
            f.write(c) 
        f.close()

class aem_report04(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r04var)}\n'
        for d in all:
            c += f'{d[r04var[0]]},{d[r04var[1]]},{d[r04var[2]]},{d[r04var[3]]},{d[r04var[4]]},'
            c += f'{d[r04var[5]]},{d[r04var[6]]},{d[r04var[7]]},{d[r04var[8]]},{d[r04var[9]]},'
            c += f'{d[r04var[10]]},{d[r04var[11]]},{d[r04var[12]]},{d[r04var[13]]},{d[r04var[14]]},'
            c += f'{d[r04var[15]]},{d[r04var[16]]},{d[r04var[17]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r04var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r04var[0]]},{d[r04var[1]]},{d[r04var[2]]},{d[r04var[3]]},{d[r04var[4]]},'
            c += f'{d[r04var[5]]},{d[r04var[6]]},{d[r04var[7]]},{d[r04var[8]]},{d[r04var[9]]},'
            c += f'{d[r04var[10]]},{d[r04var[11]]},{d[r04var[12]]},{d[r04var[13]]},{d[r04var[14]]},'
            c += f'{d[r04var[15]]},{d[r04var[16]]},{d[r04var[17]]}\n'
            f.write(c)
        f.close()

class aem_report05(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        if (self.version == '2.24.2'):
            c = f'{','.join(r05var_2242)}\n'
            for d in all:
                c += f'{d[r05var_2242[0]]},{d[r05var_2242[1]]},{d[r05var_2242[2]]},{d[r05var_2242[3]]},{d[r05var_2242[4]]},'
                c += f'{d[r05var_2242[5]]},{d[r05var_2242[6]]},{d[r05var_2242[7]]},{d[r05var_2242[8]]},{d[r05var_2242[9]]},'
                c += f'{d[r05var_2242[10]]},{d[r05var_2242[11]]},{d[r05var_2242[12]]},{d[r05var_2242[13]]},{d[r05var_2242[14]]},'
                c += f'{d[r05var_2242[15]]},{d[r05var_2242[16]]},{d[r05var_2242[17]]},{d[r05var_2242[18]]},{d[r05var_2242[19]]}\n'
        else: #for 2.24.3
            c = f'{','.join(r05var)}\n'
            for d in all:
                c += f'{d[r05var[0]]},{d[r05var[1]]},{d[r05var[2]]},{d[r05var[3]]},{d[r05var[4]]},'
                c += f'{d[r05var[5]]},{d[r05var[6]]},{d[r05var[7]]},{d[r05var[8]]},{d[r05var[9]]},'
                c += f'{d[r05var[10]]},{d[r05var[11]]},{d[r05var[12]]},{d[r05var[13]]},{d[r05var[14]]},'
                c += f'{d[r05var[15]]},{d[r05var[16]]},{d[r05var[17]]},{d[r05var[18]]},{d[r05var[19]]},{d[r05var[20]]}\n'
        return c
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        
        if (self.version == '2.24.2'):
            c = f'{','.join(r05var_2242)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r05var_2242[0]]},{d[r05var_2242[1]]},{d[r05var_2242[2]]},{d[r05var_2242[3]]},{d[r05var_2242[4]]},'
                c += f'{d[r05var_2242[5]]},{d[r05var_2242[6]]},{d[r05var_2242[7]]},{d[r05var_2242[8]]},{d[r05var_2242[9]]},'
                c += f'{d[r05var_2242[10]]},{d[r05var_2242[11]]},{d[r05var_2242[12]]},{d[r05var_2242[13]]},{d[r05var_2242[14]]},'
                c += f'{d[r05var_2242[15]]},{d[r05var_2242[16]]},{d[r05var_2242[17]]},{d[r05var_2242[18]]},{d[r05var_2242[19]]}\n'
                f.write(c)
        else: #for 2.24.3
            c = f'{','.join(r05var)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r05var[0]]},{d[r05var[1]]},{d[r05var[2]]},{d[r05var[3]]},{d[r05var[4]]},'
                c += f'{d[r05var[5]]},{d[r05var[6]]},{d[r05var[7]]},{d[r05var[8]]},{d[r05var[9]]},'
                c += f'{d[r05var[10]]},{d[r05var[11]]},{d[r05var[12]]},{d[r05var[13]]},{d[r05var[14]]},'
                c += f'{d[r05var[15]]},{d[r05var[16]]},{d[r05var[17]]},{d[r05var[18]]},{d[r05var[19]]}\n'
                f.write(c)
        f.close()  

class aem_report06(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r06var)}\n'
        for d in all:
            c += f'{d[r06var[0]]},{d[r06var[1]]},{d[r06var[2]]},{d[r06var[3]]},{d[r06var[4]]},'
            c += f'{d[r06var[5]]},{d[r06var[6]]},{d[r06var[7]]},{d[r06var[8]]},{d[r06var[9]]},'
            c += f'{d[r06var[10]]},{d[r06var[11]]},{d[r06var[12]]},{d[r06var[13]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r06var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r06var[0]]},{d[r06var[1]]},{d[r06var[2]]},{d[r06var[3]]},{d[r06var[4]]},'
            c += f'{d[r06var[5]]},{d[r06var[6]]},{d[r06var[7]]},{d[r06var[8]]},{d[r06var[9]]},'
            c += f'{d[r06var[10]]},{d[r06var[11]]},{d[r06var[12]]},{d[r06var[13]]}\n'
            f.write(c)
        f.close()  
class aem_report10(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r10var)}\n'
        for d in all:
            c += f'{d[r10var[0]]},{d[r10var[1]]},{d[r10var[2]]},{d[r10var[3]]},{d[r10var[4]]},'
            c += f'{d[r10var[5]]},{d[r10var[6]]},{d[r10var[7]]},{d[r10var[8]]},{d[r10var[9]]},'
            c += f'{d[r10var[10]]},{d[r10var[11]]},{d[r10var[12]]},{d[r10var[13]]},{d[r10var[14]]},'
            c += f'{d[r10var[15]]},{d[r10var[16]]},{d[r10var[17]]},{d[r10var[18]]},{d[r10var[19]]},{d[r10var[20]]}\n'
        return c 
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r10var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r10var[0]]},{d[r10var[1]]},{d[r10var[2]]},{d[r10var[3]]},{d[r10var[4]]},'
            c += f'{d[r10var[5]]},{d[r10var[6]]},{d[r10var[7]]},{d[r10var[8]]},{d[r10var[9]]},'
            c += f'{d[r10var[10]]},{d[r10var[11]]},{d[r10var[12]]},{d[r10var[13]]},{d[r10var[14]]},'
            c += f'{d[r10var[15]]},{d[r10var[16]]},{d[r10var[17]]},{d[r10var[18]]},{d[r10var[19]]},{d[r10var[20]]}\n'
            f.write(c)
        f.close() 
class aem_report11(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r11var)}\n'
        for d in all:
            c += f'{d[r11var[0]]},{d[r11var[1]]},{d[r11var[2]]},{d[r11var[3]]},{d[r11var[4]]},{d[r11var[5]]},{d[r11var[6]]},{d[r11var[7]]},{d[r11var[8]]},{d[r11var[9]]},{d[r11var[10]]},{d[r11var[11]]},{d[r11var[12]]},{d[r11var[13]]},{d[r11var[14]]},{d[r11var[15]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r11var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r11var[0]]},{d[r11var[1]]},{d[r11var[2]]},{d[r11var[3]]},{d[r11var[4]]},{d[r11var[5]]},{d[r11var[6]]},{d[r11var[7]]},{d[r11var[8]]},{d[r11var[9]]},{d[r11var[10]]},{d[r11var[11]]},{d[r11var[12]]},{d[r11var[13]]},{d[r11var[14]]},{d[r11var[15]]}\n'
            f.write(c)
        f.close()
class aem_report12(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        
        if (self.version == '2.24.2'):
            c = f'{','.join(r12var_2242)}\n'
            for d in all:
                c += f'{d[r12var_2242[0]]},{d[r12var_2242[1]]},{d[r12var_2242[2]]},{d[r12var_2242[3]]},{d[r12var_2242[4]]},{d[r12var_2242[5]]},'
                c += f'{d[r12var_2242[6]]},{d[r12var_2242[7]]},{d[r12var_2242[8]]},{d[r12var_2242[9]]},{d[r12var_2242[10]]},{d[r12var_2242[11]]},'
                c += f'{d[r12var_2242[12]]},{d[r12var_2242[13]]},{d[r12var_2242[14]]}\n'
        else:
            c = f'{','.join(r12var)}\n'
            for d in all:
                c += f'{d[r12var[0]]},{d[r12var[1]]},{d[r12var[2]]},{d[r12var[3]]},{d[r12var[4]]},{d[r12var[5]]},'
                c += f'{d[r12var[6]]},{d[r12var[7]]},{d[r12var[8]]},{d[r12var[9]]},{d[r12var[10]]},{d[r12var[11]]},'
                c += f'{d[r12var[12]]},{d[r12var[13]]},{d[r12var[14]]},'
                c += f'{d[r12var[15]]},{d[r12var[16]]},{d[r12var[17]]},{d[r12var[18]]},{d[r12var[19]]},{d[r12var[20]]},'
                c += f'{d[r12var[21]]},{d[r12var[22]]},{d[r12var[23]]},{d[r12var[24]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        if (self.version == '2.24.2'):
            c = f'{','.join(r12var_2242)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r12var_2242[0]]},{d[r12var_2242[1]]},{d[r12var_2242[2]]},{d[r12var_2242[3]]},{d[r12var_2242[4]]},{d[r12var_2242[5]]},'
                c += f'{d[r12var_2242[6]]},{d[r12var_2242[7]]},{d[r12var_2242[8]]},{d[r12var_2242[9]]},{d[r12var_2242[10]]},{d[r12var_2242[11]]},'
                c += f'{d[r12var_2242[12]]},{d[r12var_2242[13]]},{d[r12var_2242[14]]}\n'
                f.write(c)
        else:
            c = f'{','.join(r12var)}\n'
            f.write(c)
            for d in all:
                c = f'{d[r12var[0]]},{d[r12var[1]]},{d[r12var[2]]},{d[r12var[3]]},{d[r12var[4]]},{d[r12var[5]]},'
                c += f'{d[r12var[6]]},{d[r12var[7]]},{d[r12var[8]]},{d[r12var[9]]},{d[r12var[10]]},{d[r12var[11]]},'
                c += f'{d[r12var[12]]},{d[r12var[13]]},{d[r12var[14]]},'
                c += f'{d[r12var[15]]},{d[r12var[16]]},{d[r12var[17]]},{d[r12var[18]]},{d[r12var[19]]},{d[r12var[20]]},'
                c += f'{d[r12var[21]]},{d[r12var[22]]},{d[r12var[23]]},{d[r12var[24]]}\n'
                f.write(c)
        f.close()
class aem_report13(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r13var)}\n'
        for d in all:
            c += f'{d[r13var[0]]},{d[r13var[1]]},{d[r13var[2]]},{d[r13var[3]]},{d[r13var[4]]},{d[r13var[5]]},{d[r13var[6]]},{d[r13var[7]]},{d[r13var[8]]},{d[r13var[9]]},{d[r13var[10]]},{d[r13var[11]]},{d[r13var[12]]},{d[r13var[13]]},{d[r13var[14]]},{d[r13var[15]]},{d[r13var[16]]},{d[r13var[17]]},{d[r13var[18]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r13var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r13var[0]]},{d[r13var[1]]},{d[r13var[2]]},{d[r13var[3]]},{d[r13var[4]]},{d[r13var[5]]},{d[r13var[6]]},{d[r13var[7]]},{d[r13var[8]]},{d[r13var[9]]},{d[r13var[10]]},{d[r13var[11]]},{d[r13var[12]]},{d[r13var[13]]},{d[r13var[14]]},{d[r13var[15]]},{d[r13var[16]]},{d[r13var[17]]},{d[r13var[18]]}\n'
            f.write(c)
        f.close()
class aem_report14(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r14var)}\n'
        for d in all:
            c += f'{d[r14var[0]]},{d[r14var[1]]},{d[r14var[2]]},{d[r14var[3]]},{d[r14var[4]]},{d[r14var[5]]},{d[r14var[6]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r14var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r14var[0]]},{d[r14var[1]]},{d[r14var[2]]},{d[r14var[3]]},{d[r14var[4]]},{d[r14var[5]]},{d[r14var[6]]}\n'
            f.write(c)
        f.close()
class aem_report15(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r15var)}\n'
        for d in all:
            c += f'{d[r15var[0]]},{d[r15var[1]]},{d[r15var[2]]},{d[r15var[3]]},{d[r15var[4]]},{d[r15var[5]]},{d[r15var[6]]},{d[r15var[7]]},{d[r15var[8]]},{d[r15var[9]]},{d[r15var[10]]},{d[r15var[11]]},{d[r15var[12]]},{d[r15var[13]]},{d[r15var[14]]},{d[r15var[15]]},{d[r15var[16]]},{d[r15var[17]]},{d[r15var[18]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r15var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r15var[0]]},{d[r15var[1]]},{d[r15var[2]]},{d[r15var[3]]},{d[r15var[4]]},{d[r15var[5]]},{d[r15var[6]]},{d[r15var[7]]},{d[r15var[8]]},{d[r15var[9]]},{d[r15var[10]]},{d[r15var[11]]},{d[r15var[12]]},{d[r15var[13]]},{d[r15var[14]]},{d[r15var[15]]},{d[r15var[16]]},{d[r15var[17]]},{d[r15var[18]]}\n'
            f.write(c)
        f.close()
class aem_report16(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r16var)}\n'
        for d in all:
            c += f'{d[r16var[0]]},{d[r16var[1]]},{d[r16var[2]]},{d[r16var[3]]},{d[r16var[4]]},'
            c += f'{d[r16var[5]]},{d[r16var[6]]},{d[r16var[7]]},{d[r16var[8]]},{d[r16var[9]]},'
            c += f'{d[r16var[10]]},{d[r16var[11]]},{d[r16var[12]]},{d[r16var[13]]},{d[r16var[14]]},'
            c += f',{d[r16var[15]]},{d[r16var[16]]}\n'
        return c  
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r16var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r16var[0]]},{d[r16var[1]]},{d[r16var[2]]},{d[r16var[3]]},{d[r16var[4]]},'
            c += f'{d[r16var[5]]},{d[r16var[6]]},{d[r16var[7]]},{d[r16var[8]]},{d[r16var[9]]},'
            c += f'{d[r16var[10]]},{d[r16var[11]]},{d[r16var[12]]},{d[r16var[13]]},{d[r16var[14]]},'
            c += f',{d[r16var[15]]},{d[r16var[16]]}\n'
            f.write(c)
        f.close()
class aem_report17(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r17var)}\n'
        for d in all:
            c += f'{d[r17var[0]]},{d[r17var[1]]},{d[r17var[2]]},{d[r17var[3]]},{d[r17var[4]]},'
            c += f'{d[r17var[5]]},{d[r17var[6]]},{d[r17var[7]]},{d[r17var[8]]},{d[r17var[9]]},'
            c += f'{d[r17var[10]]},{d[r17var[11]]},{d[r17var[12]]},{d[r17var[13]]}\n'
        return c 
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r17var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r17var[0]]},{d[r17var[1]]},{d[r17var[2]]},{d[r17var[3]]},{d[r17var[4]]},'
            c += f'{d[r17var[5]]},{d[r17var[6]]},{d[r17var[7]]},{d[r17var[8]]},{d[r17var[9]]},'
            c += f'{d[r17var[10]]},{d[r17var[11]]},{d[r17var[12]]},{d[r17var[13]]}\n'
            f.write(c)
        f.close()
class aem_report18(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r18var)}\n'
        for d in all:
            c += f'{d[r18var[0]]},{d[r18var[1]]},{d[r18var[2]]},{d[r18var[3]]},{d[r18var[4]]},'
            c += f'{d[r18var[5]]},{d[r18var[6]]},{d[r18var[7]]},{d[r18var[8]]},{d[r18var[9]]},'
            c += f'{d[r18var[10]]},{d[r18var[11]]},{d[r18var[12]]},{d[r18var[13]]},{d[r18var[14]]},'
            c += f'{d[r18var[15]]},{d[r18var[16]]},{d[r18var[17]]},{d[r18var[18]]},{d[r18var[19]]}\n'
        return c
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r18var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r18var[0]]},{d[r18var[1]]},{d[r18var[2]]},{d[r18var[3]]},{d[r18var[4]]},'
            c += f'{d[r18var[5]]},{d[r18var[6]]},{d[r18var[7]]},{d[r18var[8]]},{d[r18var[9]]},'
            c += f'{d[r18var[10]]},{d[r18var[11]]},{d[r18var[12]]},{d[r18var[13]]},{d[r18var[14]]},'
            c += f'{d[r18var[15]]},{d[r18var[16]]},{d[r18var[17]]},{d[r18var[18]]},{d[r18var[19]]}\n'
            f.write(c)
        f.close()
class aem_report19(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r19var)}\n'
        for d in all:
            c += f'{d[r19var[0]]},{d[r19var[1]]},{d[r19var[2]]},{d[r19var[3]]},{d[r19var[4]]},'
            c += f'{d[r19var[5]]},{d[r19var[6]]},{d[r19var[7]]},{d[r19var[8]]},{d[r19var[9]]},'
            c += f'{d[r19var[10]]},{d[r19var[11]]},{d[r19var[12]]},{d[r19var[13]]},{d[r19var[14]]},'
            c += f'{d[r19var[15]]},{d[r19var[16]]},{d[r19var[17]]},{d[r19var[18]]},{d[r19var[19]]}\n'
        return c 
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r19var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r19var[0]]},{d[r19var[1]]},{d[r19var[2]]},{d[r19var[3]]},{d[r19var[4]]},'
            c += f'{d[r19var[5]]},{d[r19var[6]]},{d[r19var[7]]},{d[r19var[8]]},{d[r19var[9]]},'
            c += f'{d[r19var[10]]},{d[r19var[11]]},{d[r19var[12]]},{d[r19var[13]]},{d[r19var[14]]},'
            c += f'{d[r19var[15]]},{d[r19var[16]]},{d[r19var[17]]},{d[r19var[18]]},{d[r19var[19]]}\n'
            f.write(c)
        f.close()
class aem_report20(aem_report):
    def all_csv(self):
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r20var)}\n'
        for d in all:
            c += f'{d[r20var[0]]},{d[r20var[1]]},{d[r20var[2]]},{d[r20var[3]]},{d[r20var[4]]},'
            c += f'{d[r20var[5]]},{d[r20var[6]]},{d[r20var[7]]},{d[r20var[8]]},{d[r20var[9]]},'
            c += f'{d[r20var[10]]},{d[r20var[11]]},{d[r20var[12]]},{d[r20var[13]]},{d[r20var[14]]},'
            c += f'{d[r20var[15]]},{d[r20var[16]]},{d[r20var[17]]},{d[r20var[18]]},{d[r20var[19]]}\n'
        return c
    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        f = open(path, "a")
        all = []
        for item in self.items:
            for i in item.data:
                all.append(i)
        c = f'{','.join(r20var)}\n'
        f.write(c)
        for d in all:
            c = f'{d[r20var[0]]},{d[r20var[1]]},{d[r20var[2]]},{d[r20var[3]]},{d[r20var[4]]},'
            c += f'{d[r20var[5]]},{d[r20var[6]]},{d[r20var[7]]},{d[r20var[8]]},{d[r20var[9]]},'
            c += f'{d[r20var[10]]},{d[r20var[11]]},{d[r20var[12]]},{d[r20var[13]]},{d[r20var[14]]},'
            c += f'{d[r20var[15]]},{d[r20var[16]]},{d[r20var[17]]},{d[r20var[18]]},{d[r20var[19]]}\n'
            f.write(c)
        f.close()  

## solventComp CLASS
class solventComp:
    def __init__(self):
        self.name = None
        self.proportion = None
    def __str__(self):
        return f"{self.name} {self.proportion}"

## saltComp CLASS
class saltComp: 
    def __init__(self):
        self.name = None
        self.proportion: None
    def __str__(self):
        return f"{self.name} {self.proportion}"

## reportItem CLASS
class reportItem:
    def __init__(self):
        self.version: str = '2.24.3'
        self.solvents : List[solventComp] = []
        self.salts : List[saltComp] = []
        self.temperature : float
        data = None
    def salts_str(self):
        g = []
        for s in self.salts:
            g.append(str(s))
        return ','.join(g)
    def salts_str_no_comma(self):
        g = []
        for s in self.salts:
            g.append(str(s))
        return '|'.join(g)
    def solvents_str(self):
        g = []
        for s in self.solvents:
            g.append(str(s))
        return ','.join(g)
    def solvents_str_no_comma(self):
        g = []
        for s in self.solvents:
            g.append(str(s))
        return '|'.join(g)
    def temperature_str(self):
        return f'{self.temperature}°C'
    def json_data(self):
        return json.dumps(self.data, indent=4)

## aem_reportXXItem CLASS (XX - Report No.)
class report01Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r01var)}\n'
        if (self.version == '2.24.2'):
            c = f'{','.join(r01var_2242)}\n'
            for d in self.data:
                c += f'{d[r01var_2242[0]]},{d[r01var_2242[1]]},{d[r01var_2242[2]]},{d[r01var_2242[3]]},{d[r01var_2242[4]]},'
                c += f'{d[r01var_2242[5]]},{d[r01var_2242[6]]},{d[r01var_2242[7]]},{d[r01var_2242[8]]},{d[r01var_2242[9]]},'
                c += f'{d[r01var_2242[10]]},{d[r01var_2242[11]]},{d[r01var_2242[12]]},{d[r01var_2242[13]]},{d[r01var_2242[14]]},'
                c += f'{d[r01var_2242[15]]},{d[r01var_2242[16]]},{d[r01var_2242[17]]},{d[r01var_2242[18]]},{d[r01var_2242[19]]}\n'
        else:
            c = f'{','.join(r01var)}\n'
            for d in all:
                c += f'{d[r01var[0]]},{d[r01var[1]]},{d[r01var[2]]},{d[r01var[3]]},{d[r01var[4]]},'
                c += f'{d[r01var[5]]},{d[r01var[6]]},{d[r01var[7]]},{d[r01var[8]]},{d[r01var[9]]},'
                c += f'{d[r01var[10]]},{d[r01var[11]]},{d[r01var[12]]},{d[r01var[13]]},{d[r01var[14]]},'
                c += f'{d[r01var[15]]},{d[r01var[16]]},{d[r01var[17]]},{d[r01var[18]]},{d[r01var[19]]},{d[r01var[20]]}\n'

        return c
class report02Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r02var)}\n'
        for d in self.data:
            c += f'{d[r02var[0]]},{d[r02var[1]]},{d[r02var[2]]},{d[r02var[3]]},{d[r02var[4]]},'
            c += f'{d[r02var[5]]},{d[r02var[6]]},{d[r02var[7]]},{d[r02var[8]]},{d[r02var[9]]},'
            c += f'{d[r02var[10]]},{d[r02var[11]]},{d[r02var[12]]},{d[r02var[13]]},{d[r02var[14]]},'
            c += f'{d[r02var[15]]},{d[r02var[16]]},{d[r02var[17]]},{d[r02var[18]]},{d[r02var[19]]},'
            c += f'{d[r02var[20]]},{d[r02var[21]]},{d[r02var[22]]},{d[r02var[23]]},{d[r02var[24]]}\n'
        return c
class report03Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r03var)}\n'
        for d in self.data:
            c += f'{d[r03var[0]]},{d[r03var[1]]},{d[r03var[2]]},{d[r03var[3]]},{d[r03var[4]]},'
            c += f'{d[r03var[5]]},{d[r03var[6]]},{d[r03var[7]]},{d[r03var[8]]},{d[r03var[9]]},'
            c += f'{d[r03var[10]]},{d[r03var[11]]},{d[r03var[12]]},{d[r03var[13]]},{d[r03var[14]]},'
            c += f'{d[r03var[15]]}\n'
        return c
class report04Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r03var)}\n'
        for d in self.data:
            c += f'{d[r04var[0]]},{d[r04var[1]]},{d[r04var[2]]},{d[r04var[3]]},{d[r04var[4]]},'
            c += f'{d[r04var[5]]},{d[r04var[6]]},{d[r04var[7]]},{d[r04var[8]]},{d[r04var[9]]},'
            c += f'{d[r04var[10]]},{d[r04var[11]]},{d[r04var[12]]},{d[r04var[13]]},{d[r04var[14]]},'
            c += f'{d[r04var[15]]},{d[r04var[16]]},{d[r04var[17]]}\n'
        return c
class report05Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r05var)}\n'
        if (self.version == '2.24.2'):
            c = f'{','.join(r05var_2242)}\n'
            for d in self.data:
                c += f'{d[r05var_2242[0]]},{d[r05var_2242[1]]},{d[r05var_2242[2]]},{d[r05var_2242[3]]},{d[r05var_2242[4]]},'
                c += f'{d[r05var_2242[5]]},{d[r05var_2242[6]]},{d[r05var_2242[7]]},{d[r05var_2242[8]]},{d[r05var_2242[9]]},'
                c += f'{d[r05var_2242[10]]},{d[r05var_2242[11]]},{d[r05var_2242[12]]},{d[r05var_2242[13]]},{d[r05var_2242[14]]},'
                c += f'{d[r05var_2242[15]]},{d[r05var_2242[16]]},{d[r05var_2242[17]]},{d[r05var_2242[18]]},{d[r05var_2242[19]]}\n'
        else: #for 2.24.3
            c = f'{','.join(r05var)}\n'
            for d in self.data:
                c += f'{d[r05var[0]]},{d[r05var[1]]},{d[r05var[2]]},{d[r05var[3]]},{d[r05var[4]]},'
                c += f'{d[r05var[5]]},{d[r05var[6]]},{d[r05var[7]]},{d[r05var[8]]},{d[r05var[9]]},'
                c += f'{d[r05var[10]]},{d[r05var[11]]},{d[r05var[12]]},{d[r05var[13]]},{d[r05var[14]]},'
                c += f'{d[r05var[15]]},{d[r05var[16]]},{d[r05var[17]]},{d[r05var[18]]},{d[r05var[19]]},{d[r05var[20]]}\n'
        return c
class report06Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r06var)}\n'
        for d in self.data:
            c += f'{d[r06var[0]]},{d[r06var[1]]},{d[r06var[2]]},{d[r06var[3]]},{d[r06var[4]]},'
            c += f'{d[r06var[5]]},{d[r06var[6]]},{d[r06var[7]]},{d[r06var[8]]},{d[r06var[9]]},'
            c += f'{d[r06var[10]]},{d[r06var[11]]},{d[r06var[12]]},{d[r06var[13]]}\n'
        return c

class report10Item(reportItem):
    def __init__(self):
        super().__init__()
        self.surface_charge_density: float = None
        self.cell_voltage_at_start_of_pulse: float = None
        self.salt_concentration_basis: float = None
        self.pulse_type: str = ''
        self.electrolyte_rel_perm_at_salt_conc: float = None
        self.dipole_moment_data: float = None
        self.solvent_diameter: float = None
        self.equivalent_charge_on_solvent_dipole: float = None
        self.sei_thickness: float = None
        self.sei_porosity: float = None
        self.sei_relative_permittivity: float = None

    def data_csv_str(self):
        c = f'{','.join(r10var)}\n'
        for d in self.data:
            c += f'{d[r10var[0]]},{d[r10var[1]]},{d[r10var[2]]},{d[r10var[3]]},{d[r10var[4]]},'
            c += f'{d[r10var[5]]},{d[r10var[6]]},{d[r10var[7]]},{d[r10var[8]]},{d[r10var[9]]},'
            c += f'{d[r10var[10]]},{d[r10var[11]]},{d[r10var[12]]},{d[r10var[13]]},{d[r10var[14]]},'
            c += f'{d[r10var[15]]},{d[r10var[16]]},{d[r10var[17]]},{d[r10var[18]]},{d[r10var[19]]}\n'
        return c
class report11Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r11var)}\n'
        for d in self.data:
            c += f'{d[r11var[0]]},{d[r11var[1]]},{d[r11var[2]]},{d[r11var[3]]},{d[r11var[4]]},{d[r11var[5]]},{d[r11var[6]]},{d[r11var[7]]},{d[r11var[8]]},{d[r11var[9]]},{d[r11var[10]]},{d[r11var[11]]},{d[r11var[12]]},{d[r11var[13]]},{d[r11var[14]]},{d[r11var[15]]}\n'
        return c
class report12Item(reportItem):
    def data_csv_str(self):
        if (self.version == '2.24.2'):
            c = f'{','.join(r12var_2242)}\n'
            for d in self.data:
                c += f'{d[r12var_2242[0]]},{d[r12var_2242[1]]},{d[r12var_2242[2]]},{d[r12var_2242[3]]},{d[r12var_2242[4]]},{d[r12var_2242[5]]},'
                c += f'{d[r12var_2242[6]]},{d[r12var_2242[7]]},{d[r12var_2242[8]]},{d[r12var_2242[9]]},{d[r12var_2242[10]]},{d[r12var_2242[11]]},'
                c += f'{d[r12var_2242[12]]},{d[r12var_2242[13]]},{d[r12var_2242[14]]}\n'
        else:
            c = f'{','.join(r12var)}\n'
            for d in self.data:
                c += f'{d[r12var[0]]},{d[r12var[1]]},{d[r12var[2]]},{d[r12var[3]]},{d[r12var[4]]},{d[r12var[5]]},'
                c += f'{d[r12var[6]]},{d[r12var[7]]},{d[r12var[8]]},{d[r12var[9]]},{d[r12var[10]]},{d[r12var[11]]},'
                c += f'{d[r12var[12]]},{d[r12var[13]]},{d[r12var[14]]},'
                c += f'{d[r12var[15]]},{d[r12var[16]]},{d[r12var[17]]},{d[r12var[18]]},{d[r12var[19]]},{d[r12var[20]]},'
                c += f'{d[r12var[21]]},{d[r12var[22]]},{d[r12var[23]]},{d[r12var[24]]}\n'
        return c
class report13Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r13var)}\n'
        for d in self.data:
            c += f'{d[r13var[0]]},{d[r13var[1]]},{d[r13var[2]]},{d[r13var[3]]},{d[r13var[4]]},{d[r13var[5]]},{d[r13var[6]]},{d[r13var[7]]},{d[r13var[8]]},{d[r13var[9]]},{d[r13var[10]]},{d[r13var[11]]},{d[r13var[12]]},{d[r13var[13]]},{d[r13var[14]]},{d[r13var[15]]},{d[r13var[16]]},{d[r13var[17]]},{d[r13var[18]]}\n'
        return c

class report14Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r14var)}\n'
        for d in self.data:
            c += f'{d[r14var[0]]},{d[r14var[1]]},{d[r14var[2]]},{d[r14var[3]]},{d[r14var[4]]},{d[r14var[5]]},{d[r14var[6]]}\n'
        return c

class report15Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r15var)}\n'
        for d in self.data:
            c += f'{d[r15var[0]]},{d[r15var[1]]},{d[r15var[2]]},{d[r15var[3]]},{d[r15var[4]]},{d[r15var[5]]},{d[r15var[6]]},{d[r15var[7]]},{d[r15var[8]]},{d[r15var[9]]},{d[r15var[10]]},{d[r15var[11]]},{d[r15var[12]]},{d[r15var[13]]},{d[r15var[14]]},{d[r15var[15]]},{d[r15var[16]]},{d[r15var[17]]},{d[r15var[18]]}\n'
        return c

class report16Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r16var)}\n'
        for d in self.data:
            c += f'{d[r16var[0]]},{d[r16var[1]]},{d[r16var[2]]},{d[r16var[3]]},{d[r16var[4]]},'
            c += f'{d[r16var[5]]},{d[r16var[6]]},{d[r16var[7]]},{d[r16var[8]]},{d[r16var[9]]},'
            c += f'{d[r16var[10]]},{d[r16var[11]]},{d[r16var[12]]},{d[r16var[13]]},{d[r16var[14]]},'
            c += f'{d[r16var[15]]},{d[r16var[16]]}\n'
        return c

class report17Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r17var)}\n'
        for d in self.data:
            c += f'{d[r17var[0]]},{d[r17var[1]]},{d[r17var[2]]},{d[r17var[3]]},{d[r17var[4]]},'
            c += f'{d[r17var[5]]},{d[r17var[6]]},{d[r17var[7]]},{d[r17var[8]]},{d[r17var[9]]},'
            c += f'{d[r17var[10]]},{d[r17var[11]]},{d[r17var[12]]},{d[r17var[13]]}\n'
        return c
class report18Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r18var)}\n'
        for d in self.data:
            c += f'{d[r18var[0]]},{d[r18var[1]]},{d[r18var[2]]},{d[r18var[3]]},{d[r18var[4]]},'
            c += f'{d[r18var[5]]},{d[r18var[6]]},{d[r18var[7]]},{d[r18var[8]]},{d[r18var[9]]},'
            c += f'{d[r18var[10]]},{d[r18var[11]]},{d[r18var[12]]},{d[r18var[13]]},{d[r18var[14]]},'
            c += f'{d[r18var[15]]},{d[r18var[16]]},{d[r18var[17]]},{d[r18var[18]]},{d[r18var[19]]}\n'
        return c
class report19Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r19var)}\n'
        for d in self.data:
            c += f'{d[r19var[0]]},{d[r19var[1]]},{d[r19var[2]]},{d[r19var[3]]},{d[r19var[4]]},'
            c += f'{d[r19var[5]]},{d[r19var[6]]},{d[r19var[7]]},{d[r19var[8]]},{d[r19var[9]]},'
            c += f'{d[r19var[10]]},{d[r19var[11]]},{d[r19var[12]]},{d[r19var[13]]},{d[r19var[14]]},'
            c += f'{d[r19var[15]]},{d[r19var[16]]},{d[r19var[17]]},{d[r19var[18]]},{d[r19var[19]]}\n'
        return c
class report20Item(reportItem):
    def data_csv_str(self):
        c = f'{','.join(r20var)}\n'
        for d in self.data:
            c += f'{d[r20var[0]]},{d[r20var[1]]},{d[r20var[2]]},{d[r20var[3]]},{d[r20var[4]]},'
            c += f'{d[r20var[5]]},{d[r20var[6]]},{d[r20var[7]]},{d[r20var[8]]},{d[r20var[9]]},'
            c += f'{d[r20var[10]]},{d[r20var[11]]},{d[r20var[12]]},{d[r20var[13]]},{d[r20var[14]]},'
            c += f'{d[r20var[15]]},{d[r20var[16]]},{d[r20var[17]]},{d[r20var[18]]},{d[r20var[19]]}\n'
        return c

## Misc. Functions
def filterNonEmpty(v):
    if v == '':
        return False
    else:
        return True

def set_to_empty(report, run):
    if (("Report01 --" in report) | ("Report1 --" in report)):
        run.report01 = aem_report01()
        run.report01.exists = False
    elif (("Report02 --" in report) | ("Report2 --" in report)):
        run.report02 = aem_report02()
        run.report02.exists = False
    elif (("Report03 --" in report) | ("Report3 --" in report)):
        run.report03 = aem_report03()
        run.report03.exists = False
    elif (("Report04 --" in report) | ("Report4 --" in report)):
        run.report04 = aem_report04()
        run.report04.exists = False
    elif (("Report05 --" in report) | ("Report5 --" in report)):
        run.report05 = aem_report05()
        run.report05.exists = False
    elif (("Report06 --" in report) | ("Report6 --" in report)):
        run.report06 = aem_report06()
        run.report06.exists = False
    elif (("Report10 --" in report) | ("Report10 --" in report)):
        run.report10 = aem_report10()
        run.report10.exists = False
    elif (("Report11 --" in report)):
        run.report11 = aem_report11()
        run.report11.exists = False
    elif (("Report12 --" in report)):
        run.report12 = aem_report12()
        run.report12.exists = False
    elif (("Report13 --" in report)):
        run.report13 = aem_report13()
        run.report13.exists = False
    elif (("Report14 --" in report)):
        run.report14 = aem_report14()
        run.report14.exists = False
    elif (("Report15 --" in report)):
        run.report15 = aem_report15()
        run.report15.exists = False
    elif (("Report16 --" in report)):
        run.report16 = aem_report16()
        run.report16.exists = False
    elif (("Report17 --" in report)):
        run.report17 = aem_report17()
        run.report17.exists = False
    elif (("Report18 --" in report)):
        run.report18 = aem_report18()
        run.report18.exists = False
    elif (("Report19 --" in report)):
        run.report19 = aem_report19()
        run.report19.exists = False
    elif (("Report20 --" in report)):
        run.report20 = aem_report20()
        run.report20.exists = False

def rep1_thread_fn(report, r):
    r = parseReport01(report)
def rep2_thread_fn(report, r):
    r = parseReport02(report)
def rep3_thread_fn(report, r):
    r.report03 = parseReport03(report)
def rep4_thread_fn(report, run):
    run.report04 = parseReport04(report)
def rep5_thread_fn(report, run):
    run.report05 = parseReport05(report)
def rep6_thread_fn(report, run):
    run.report06 = parseReport06(report)
def rep10_thread_fn(report, run):
    run.report10 = parseReport10(report)
def rep11_thread_fn(report, run):
    run.report11 = parseReport11(report)
def rep12_thread_fn(report, run):
    run.report12 = parseReport12(report)
def rep13_thread_fn(report, run):
    run.report13 = parseReport13(report)
def rep14_thread_fn(report, run):
    run.report14 = parseReport14(report)
def rep15_thread_fn(report, run):
    run.report15 = parseReport15(report)
def rep16_thread_fn(report, run):
    run.report16 = parseReport16(report)
def rep17_thread_fn(report, run):
    run.report17 = parseReport17(report)
def rep18_thread_fn(report, run):
    run.report18 = parseReport18(report)
def rep19_thread_fn(report, run):
    run.report19 = parseReport19(report)
def rep20_thread_fn(report, run):
    run.report20 = parseReport20(report)

## Parsing Functions
def parseReport(report, run):
    if os.path.getsize(report) == 0:
        print(f'### AEM-PARSER v1.1.0:: {report} is empty')
        set_to_empty(report, run)
    elif ("Report01 --" in report):
        run.report01 = parseReport01(report)
    elif ("Report1 --" in report):
        run.report01 = parseReport01(report)
    elif ("Report02 --" in report):
        run.report02 = parseReport02(report)
    elif ("Report2 --" in report):
        run.report02 = parseReport02(report)
    elif ("Report03 --" in report):
        run.report03 = parseReport03(report)
    elif ("Report3 --" in report):
        run.report03 = parseReport03(report)
    elif ("Report04 --" in report):
        run.report04 = parseReport04(report)
    elif ("Report4 --" in report):
        run.report04 = parseReport04(report)
    elif ("Report05 --" in report):
        run.report05 = parseReport05(report)
    elif ("Report5 --" in report):
        run.report05 = parseReport05(report)
    elif ("Report06 --" in report):
        run.report06 = parseReport06(report)
    elif ("Report6 --" in report):
        run.report06 = parseReport06(report)
    elif ("Report10 --" in report):
        run.report10 = parseReport10(report)
    elif ("Report11 --" in report):
        run.report11 = parseReport11(report)
    elif ("Report12 --" in report):
        run.report12 = parseReport12(report)
    elif ("Report13 --" in report):
        run.report13 = parseReport13(report)
    elif ("Report14 --" in report):
        run.report14 = parseReport14(report)
    elif ("Report15 --" in report):
        run.report15 = parseReport15(report)
    elif ("Report16 --" in report):
        run.report16 = parseReport16(report)
    elif ("Report17 --" in report):
        run.report17 = parseReport17(report)
    elif ("Report18 --" in report):
        run.report18 = parseReport18(report)
    elif ("Report19 --" in report):
        run.report19 = parseReport19(report)
    elif ("Report20 --" in report):
        run.report20 = parseReport20(report)
    else:
        pass
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def check_stars(e):
    if ('********' == e) | ('*****' == e):
        return float("NaN")
    else: 
        return float(e)

def parse_composition_temperature(pieces, r):
    saltC = pieces[0].split("at Temp. =")[0].strip().replace('        ', ' ')
    saltcSplit = saltC.split(' + ')
    solC = []
    salt = saltComp()
    if len(saltcSplit) == 1:
        salt.name = saltcSplit[0].strip()
        salt.proportion = '1.000'
        r.salts.append(salt)
    else:
        for s in saltcSplit:
            s.strip()
            ss = s.split(' ')
            sName = ''
            sComp = None
            for q in ss:
                q.strip()
                if (isfloat(q) == False):
                    sName += q
                else:
                    sComp = q
            salt.name =sName
            salt.proportion=sComp
            r.salts.append(salt)
    r.temperature = float(pieces[0].split("at Temp. =")[1].split("C")[0].strip())
    foo = pieces[1].split('-----------------------------------------------------------------------')[1].splitlines()
    for fo in foo:
        sc= []
        fo = fo.strip()
        spl = fo.split(' ')
        compound = []
        name = ""
        proportion=""
        for s in spl:
            s= s.strip()
            if (isfloat(s) == False):
                if ((s != '')):
                    compound.append(s.strip()) 
            else:
                compound.append(s.strip())
                break
        solC.append(' '.join(compound))
    solventCompostion = filter(filterNonEmpty, solC)
    for s in solventCompostion:
        spl = s.split(" ")
        proportion = spl.pop()
        name = ' '.join(spl)
        solvent = solventComp()
        solvent.name = name
        solvent.proportion = proportion
        r.solvents.append(solvent)
        
def getReportVersionNumber(text):
    if (text.startswith('  AEM ver. 2.24.2M-D-ACCC')):
        return '2.24.2'
    else:
        return '2.24.3'
def parseReport01(reportPath):
    report01 = aem_report01()
    report01.exists = True
    report01.path = reportPath
    f=open(reportPath)
    text = f.read()
    report01.version = getReportVersionNumber(text)
    if (report01.version == '2.24.2'):
        tableSep = '-----------------------------------------------------------------------------------------------------------------------------------------------------'
    else:
        tableSep = '-------------------------------------------------------------------------------------------------------------------------------------------------------------'
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report01Item()
        r.version = report01.version
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split(tableSep)[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 17:
                j = {
                    r01var_2242[0]: r.solvents_str_no_comma(),
                    r01var_2242[1]: r.salts_str_no_comma(),
                    r01var_2242[2]: parse_float(r.temperature),
                    r01var_2242[3]: parse_float(d[0]),
                    r01var_2242[4]: parse_float(d[1]),
                    r01var_2242[5]: parse_float(d[2]),
                    r01var_2242[6]: parse_float(d[3]),
                    r01var_2242[7]: parse_float(d[4]),
                    r01var_2242[8]: parse_float(d[5]),
                    r01var_2242[9]: check_stars(d[6]),
                    r01var_2242[10]: parse_float(d[7]),
                    r01var_2242[11]: parse_float(d[8]),
                    r01var_2242[12]: parse_float(d[9]),
                    r01var_2242[13]: parse_float(d[10]),
                    r01var_2242[14]: parse_float(d[11]),
                    r01var_2242[15]: parse_float(d[12]),
                    r01var_2242[16]: parse_float(d[13]),
                    r01var_2242[17]: parse_float(d[14]),
                    r01var_2242[18]: parse_float(d[15]),
                    r01var_2242[19]: parse_float(d[16])
                }
                data.append(j)
            elif len(d) == 18:
                j = {
                    r01var[0]: r.solvents_str_no_comma(),
                    r01var[1]: r.salts_str_no_comma(),
                    r01var[2]: parse_float(r.temperature),
                    r01var[3]: parse_float(d[0]),
                    r01var[4]: parse_float(d[1]),
                    r01var[5]: parse_float(d[2]),
                    r01var[6]: parse_float(d[3]),
                    r01var[7]: parse_float(d[4]),
                    r01var[8]: parse_float(d[5]),
                    r01var[9]: check_stars(d[6]),
                    r01var[10]: parse_float(d[7]),
                    r01var[11]: parse_float(d[8]),
                    r01var[12]: parse_float(d[9]),
                    r01var[13]: parse_float(d[10]),
                    r01var[14]: parse_float(d[11]),
                    r01var[15]: parse_float(d[12]),
                    r01var[16]: parse_float(d[13]),
                    r01var[17]: parse_float(d[14]),
                    r01var[18]: parse_float(d[15]),
                    r01var[19]: parse_float(d[16]),
                    r01var[20]: parse_float(d[17])
                }
                data.append(j)   
        r.data = data
        report01.items.append(r)
    return report01
        
def parseReport02(reportPath):
    report02 = aem_report02()
    report02.exists = True
    report02.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report02Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 22:
                j = {
                    r02var[0]: r.solvents_str_no_comma(),
                    r02var[1]: r.salts_str_no_comma(),
                    r02var[2]: parse_float(r.temperature),
                    r02var[3]: parse_float(d[0]),
                    r02var[4]: parse_float(d[1]),
                    r02var[5]: parse_float(d[2]),
                    r02var[6]: parse_float(d[3]),
                    r02var[7]: parse_float(d[4]),
                    r02var[8]: parse_float(d[5]),
                    r02var[9]: parse_float(d[6]),
                    r02var[10]: parse_float(d[7]),
                    r02var[11]: parse_float(d[8]),
                    r02var[12]: parse_float(d[9]),
                    r02var[13]: parse_float(d[10]),
                    r02var[14]: parse_float(d[11]),
                    r02var[15]: parse_float(d[12]),
                    r02var[16]: parse_float(d[13]),
                    r02var[17]: parse_float(d[14]),
                    r02var[18]: parse_float(d[15]),
                    r02var[19]: parse_float(d[16]),
                    r02var[20]: parse_float(d[17]),
                    r02var[21]: parse_float(d[18]),
                    r02var[22]: parse_float(d[19]),
                    r02var[23]: parse_float(d[20]),
                    r02var[24]: parse_float(d[21]),
                }
                data.append(j)
            
        r.data = data
        report02.items.append(r)
    return report02

def parseReport03(reportPath):
    report03 = aem_report03()
    report03.exists = True
    report03.path = reportPath
    f=open(reportPath)
    text = f.read()
    report03.version = getReportVersionNumber(text)
    if (report03.version == '2.24.2'):
        tableSep = '----------------------------------------------------------------------------------------------------------------------------------------'
    else:
        tableSep = '--------------------------------------------------------------------------------------------------------------------------------------------'
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report03Item()
        r.version = report03.version
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split(tableSep)[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("*DNC*", "").replace('/', '')
            d = f.strip().split(" ")
            if len(d) == 13:
                j = {
                    r03var[0]: r.solvents_str_no_comma(),
                    r03var[1]: r.salts_str_no_comma(),
                    r03var[2]: parse_float(r.temperature),
                    r03var[3]: parse_float(d[0]),
                    r03var[4]: parse_float(d[1]),
                    r03var[5]: parse_float(d[2]),
                    r03var[6]: parse_float(d[3]),
                    r03var[7]: parse_float(d[4]),
                    r03var[8]: parse_float(d[5]),
                    r03var[9]: parse_float(d[6]),
                    r03var[10]: parse_float(d[7]),
                    r03var[11]: parse_float(d[8]),
                    r03var[12]: parse_float(d[9]),
                    r03var[13]: parse_float(d[10]),
                    r03var[14]: parse_float(d[11]),
                    r03var[15]: parse_float(d[12]),
                }
                data.append(j)
            
        r.data = data
        report03.items.append(r)
    return report03

def parseReport04(reportPath):
    report04 = aem_report04()
    report04.exists = True
    report04.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report04Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 15:
                j = {
                    r04var[0]: r.solvents_str_no_comma(),
                    r04var[1]: r.salts_str_no_comma(),
                    r04var[2]: parse_float(r.temperature),
                    r04var[3]: parse_float(d[0]),
                    r04var[4]: parse_float(d[1]),
                    r04var[5]: parse_float(d[2]),
                    r04var[6]: parse_float(d[3]),
                    r04var[7]: check_stars(parse_float(d[4])),
                    r04var[8]: parse_float(d[5]),
                    r04var[9]: parse_float(d[6]),
                    r04var[10]: parse_float(d[7]),
                    r04var[11]: parse_float(d[8]),
                    r04var[12]: parse_float(d[9]),
                    r04var[13]: parse_float(d[10]),
                    r04var[14]: parse_float(d[11]),
                    r04var[15]: parse_float(d[12]),
                    r04var[16]: parse_float(d[13]),
                    r04var[17]: parse_float(d[14]),
                }
                data.append(j)
            
        r.data = data
        report04.items.append(r)
    return report04

def parseReport05(reportPath):
    report05 = aem_report05()
    report05.exists = True
    report05.path = reportPath
    f=open(reportPath)
    text = f.read()
    report05.version = getReportVersionNumber(text)
    if (report05.version == '2.24.2'):
        tableSep = '--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    else:
        tableSep = '----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report05Item()
        r.version = report05.version
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split(tableSep)[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 17:
                j = {
                    r05var_2242[0]: r.solvents_str_no_comma(),
                    r05var_2242[1]: r.salts_str_no_comma(),
                    r05var_2242[2]: parse_float(r.temperature),
                    r05var_2242[3]: parse_float(d[0]),
                    r05var_2242[4]: parse_float(d[1]),
                    r05var_2242[5]: parse_float(d[2]),
                    r05var_2242[6]: parse_float(d[3]),
                    r05var_2242[7]: parse_float(d[4]),
                    r05var_2242[8]: parse_float(d[5]),
                    r05var_2242[9]: parse_float(d[6]),
                    r05var_2242[10]: parse_float(d[7]),
                    r05var_2242[11]: parse_float(d[8]),
                    r05var_2242[12]: parse_float(d[9]),
                    r05var_2242[13]: parse_float(d[10]),
                    r05var_2242[14]: parse_float(d[11]),
                    r05var_2242[15]: parse_float(d[12]),
                    r05var_2242[16]: parse_float(d[13]),
                    r05var_2242[17]: parse_float(d[14]),
                    r05var_2242[18]: parse_float(d[15]),
                    r05var_2242[19]: parse_float(d[16]),
                }
            elif len(d) == 18:
                j = {
                    r05var[0]: r.solvents_str_no_comma(),
                    r05var[1]: r.salts_str_no_comma(),
                    r05var[2]: parse_float(r.temperature),
                    r05var[3]: parse_float(d[0]),
                    r05var[4]: parse_float(d[1]),
                    r05var[5]: parse_float(d[2]),
                    r05var[6]: parse_float(d[3]),
                    r05var[7]: parse_float(d[4]),
                    r05var[8]: parse_float(d[5]),
                    r05var[9]: parse_float(d[6]),
                    r05var[10]: parse_float(d[7]),
                    r05var[11]: parse_float(d[8]),
                    r05var[12]: parse_float(d[9]),
                    r05var[13]: parse_float(d[10]),
                    r05var[14]: parse_float(d[11]),
                    r05var[15]: parse_float(d[12]),
                    r05var[16]: parse_float(d[13]),
                    r05var[17]: parse_float(d[14]),
                    r05var[18]: parse_float(d[15]),
                    r05var[19]: parse_float(d[16]),
                    r05var[20]: parse_float(d[17]),
                }
                data.append(j)
        r.data = data
        report05.items.append(r)
    return report05

def parseReport06(reportPath):
    report06 = aem_report06()
    report06.exists = True
    report06.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report06Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('--------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 11:
                j = {
                    r06var[0]: r.solvents_str_no_comma(),
                    r06var[1]: r.salts_str_no_comma(),
                    r06var[2]: parse_float(r.temperature),
                    r06var[3]: parse_float(d[0]),
                    r06var[4]: parse_float(d[1]),
                    r06var[5]: parse_float(d[2]),
                    r06var[6]: parse_float(d[3]),
                    r06var[7]: parse_float(d[4]),
                    r06var[8]: parse_float(d[5]),
                    r06var[9]: parse_float(d[6]),
                    r06var[10]: parse_float(d[7]),
                    r06var[11]: parse_float(d[8]),
                    r06var[12]: parse_float(d[9]),
                    r06var[13]: parse_float(d[10]),
                    
                }
                data.append(j)
            
        r.data = data
        report06.items.append(r)
    return report06
def parse_report_10_specific_variables(pieces, r: report10Item):
    body = pieces[1].split('\n  \n  \n')
    lines = body[1].splitlines()
    i = 0 
    r.surface_charge_density = parse_float(lines[0].split('  Surface Charge Density at target electrode surface: ')[1].split('  C/cm^2')[0].strip())
    r.cell_voltage_at_start_of_pulse = parse_float(lines[1].split('  Cell Voltage at start of pulse: ')[1].split('  V')[0].strip())
    r.salt_concentration_basis = parse_float(lines[3].split('  at  ')[1].split('  molal')[0].strip())
    r.pulse_type = lines[5].split('Pulse type: ')[1].split(';')[0].strip()
    r.electrolyte_rel_perm_at_salt_conc = parse_float(lines[6].split('  Electrolyte Rel. Perm. at Salt Conc.: ')[1].split('  (reference at infinite r distance)')[0].strip())
    r.dipole_moment_data = parse_float(lines[7].split('  Dipole Moment, data:  ')[1].split('  D')[0].strip())
    r.solvent_diameter = parse_float(lines[8].split('  Solvent diameter:  ')[1].split('  Angstroms')[0].strip())
    r.equivalent_charge_on_solvent_dipole = parse_float(lines[9].split('Equivalent charge on solvent dipole:')[1].strip())
    r.sei_thickness = parse_float(lines[11].split('      SEI thickness at target electrode: ')[1].split('  Angstroms')[0].strip())
    r.sei_porosity = parse_float(lines[12].split('      SEI porosity at target electrode: ')[1].split('  Angstroms')[0].strip())
    r.sei_relative_permittivity = parse_float(lines[13].split('      SEI relative permittivity at target electrode: ')[1].strip())
    

def parseReport10(reportPath):
    report10 = aem_report10()
    report10.exists = True
    report10.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report10Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        parse_report_10_specific_variables(pieces, r)
        foo = pieces[1].split('------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 7:
                j = {
                    r10var[0]: r.solvents_str_no_comma(),
                    r10var[1]: r.salts_str_no_comma(),
                    r10var[2]: parse_float(r.temperature),
                    r10var[3]: r.surface_charge_density,
                    r10var[4]: r.cell_voltage_at_start_of_pulse,
                    r10var[5]: r.salt_concentration_basis,
                    r10var[6]: r.pulse_type,
                    r10var[7]: r.electrolyte_rel_perm_at_salt_conc,
                    r10var[8]: r.dipole_moment_data,
                    r10var[9]: r.solvent_diameter,
                    r10var[10]: r.equivalent_charge_on_solvent_dipole,
                    r10var[11]: r.sei_thickness,
                    r10var[12]: r.sei_porosity,
                    r10var[13]: r.sei_relative_permittivity,
                    r10var[14]: parse_float(d[0]),
                    r10var[15]: parse_float(d[1]),
                    r10var[16]: parse_float(d[2]),
                    r10var[17]: parse_float(d[3]),
                    r10var[18]: parse_float(d[4]),
                    r10var[19]: parse_float(d[5]),
                    r10var[20]: parse_float(d[6]),
                }
                data.append(j)
            
        r.data = data
        report10.items.append(r)
    return report10
def parseReport11(reportPath):
    report11 = aem_report11()
    report11.exists = True
    report11.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report11Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('-------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 13:
                j = {
                    r11var[0]: r.solvents_str_no_comma(),
                    r11var[1]: r.salts_str_no_comma(),
                    r11var[2]: parse_float(r.temperature),
                    r11var[3]: parse_float(d[0]),
                    r11var[4]: parse_float(d[1]),
                    r11var[5]: parse_float(d[2]),
                    r11var[6]: parse_float(d[3]),
                    r11var[7]: parse_float(d[4]),
                    r11var[8]: parse_float(d[5]),
                    r11var[9]: parse_float(d[6]),
                    r11var[10]: parse_float(d[7]),
                    r11var[11]: parse_float(d[8]),
                    r11var[12]: parse_float(d[9]),
                    r11var[13]: parse_float(d[10]),
                    r11var[14]: parse_float(d[11]),
                    r11var[15]: parse_float(d[12]),
                
                }
                data.append(j)
            
        r.data = data
        report11.items.append(r)
    return report11

def parseReport12(reportPath):
    report12 = aem_report12()
    report12.exists = True
    report12.path = reportPath
    f=open(reportPath)
    text = f.read()
    report12.version = getReportVersionNumber(text)
    if (report12.version == '2.24.2'):
        tableSep = '-----------------------------------------------------------------------------------------------------------------------------------'
    else:
        tableSep = '-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report12Item()
        r.version = report12.version
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split(tableSep)[1].splitlines()
        for fo in foo:
            f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 12:
                j = {
                    r12var_2242[0]: r.solvents_str_no_comma(),
                    r12var_2242[1]: r.salts_str_no_comma(),
                    r12var_2242[2]: parse_float(r.temperature),
                    r12var_2242[3]: parse_float(d[0]),
                    r12var_2242[4]: parse_float(d[1]),
                    r12var_2242[5]: parse_float(d[2]),
                    r12var_2242[6]: parse_float(d[3]),
                    r12var_2242[7]: parse_float(d[4]),
                    r12var_2242[8]: parse_float(d[5]),
                    r12var_2242[9]: parse_float(d[6]),
                    r12var_2242[10]: parse_float(d[7]),
                    r12var_2242[11]: parse_float(d[8]),
                    r12var_2242[12]: parse_float(d[9]),
                    r12var_2242[13]: parse_float(d[10]),
                    r12var_2242[14]: parse_float(d[11]),
                }
                data.append(j)
            elif len(d) == 22:
                j = {
                    r12var[0]: r.solvents_str_no_comma(),
                    r12var[1]: r.salts_str_no_comma(),
                    r12var[2]: parse_float(r.temperature),
                    r12var[3]: parse_float(d[0]),
                    r12var[4]: parse_float(d[1]),
                    r12var[5]: parse_float(d[2]),
                    r12var[6]: parse_float(d[3]),
                    r12var[7]: parse_float(d[4]),
                    r12var[8]: parse_float(d[5]),
                    r12var[9]: parse_float(d[6]),
                    r12var[10]: parse_float(d[7]),
                    r12var[11]: parse_float(d[8]),
                    r12var[12]: parse_float(d[9]),
                    r12var[13]: parse_float(d[10]),
                    r12var[14]: parse_float(d[11]),
                    r12var[15]: parse_float(d[12]),
                    r12var[16]: parse_float(d[13]),
                    r12var[17]: parse_float(d[14]),
                    r12var[18]: parse_float(d[15]),
                    r12var[19]: parse_float(d[16]),
                    r12var[20]: parse_float(d[17]),
                    r12var[21]: parse_float(d[18]),
                    r12var[22]: parse_float(d[19]),
                    r12var[23]: parse_float(d[20]),
                    r12var[24]: parse_float(d[21]),
                }
                data.append(j)
        r.data = data
        report12.items.append(r)
    return report12

def parseReport13(reportPath):
    report13 = aem_report13()
    report13.exists = True
    report13.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report13Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 16:
                j = {
                    r13var[0]: r.solvents_str_no_comma(),
                    r13var[1]: r.salts_str_no_comma(),
                    r13var[2]: parse_float(r.temperature),
                    r13var[3]: parse_float(d[0]),
                    r13var[4]: parse_float(d[1]),
                    r13var[5]: parse_float(d[2]),
                    r13var[6]: parse_float(d[3]),
                    r13var[7]: parse_float(d[4]),
                    r13var[8]: parse_float(d[5]),
                    r13var[9]: parse_float(d[6]),
                    r13var[10]: parse_float(d[7]),
                    r13var[11]: parse_float(d[8]),
                    r13var[12]: parse_float(d[9]),
                    r13var[13]: parse_float(d[10]),
                    r13var[14]: parse_float(d[11]),
                    r13var[15]: parse_float(d[12]),
                    r13var[16]: parse_float(d[13]),
                    r13var[17]: parse_float(d[14]),
                    r13var[18]: parse_float(d[15]),
                
                }
                data.append(j)
            
        r.data = data
        report13.items.append(r)
    return report13

def parseReport14(reportPath):
    report14 = aem_report14()
    report14.exists = True
    report14.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report14Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 4:
                j = {
                    r14var[0]: r.solvents_str_no_comma(),
                    r14var[1]: r.salts_str_no_comma(),
                    r14var[2]: parse_float(r.temperature),
                    r14var[3]: parse_float(d[0]),
                    r14var[4]: parse_float(d[1]),
                    r14var[5]: parse_float(d[2]),
                    r14var[6]: parse_float(d[3]),
                }
                data.append(j)
            
        r.data = data
        report14.items.append(r)
    return report14

def parseReport15(reportPath):
    report15 = aem_report15()
    report15.exists = True
    report15.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report15Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 16:
                j = {
                    r15var[0]: r.solvents_str_no_comma(),
                    r15var[1]: r.salts_str_no_comma(),
                    r15var[2]: parse_float(r.temperature),
                    r15var[3]: check_stars(d[0]),
                    r15var[4]: parse_float(d[1]),
                    r15var[5]: parse_float(d[2]),
                    r15var[6]: parse_float(d[3]),
                    r15var[7]: parse_float(d[4]),
                    r15var[8]: parse_float(d[5]),
                    r15var[9]: parse_float(d[6]),
                    r15var[10]: parse_float(d[7]),
                    r15var[11]: parse_float(d[8]),
                    r15var[12]: parse_float(d[9]),
                    r15var[13]: parse_float(d[10]),
                    r15var[14]: parse_float(d[11]),
                    r15var[15]: parse_float(d[12]),
                    r15var[16]: parse_float(d[13]),
                    r15var[17]: parse_float(d[14]),
                    r15var[18]: parse_float(d[15]),
                
                }
                data.append(j)
            
        r.data = data
        report15.items.append(r)
    return report15

def parseReport16(reportPath):
    report16 = aem_report16()
    report16.exists = True
    report16.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report16Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace('          ', ' ').replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 14:
                j = {
                    r16var[0]: r.solvents_str_no_comma(),
                    r16var[1]: r.salts_str_no_comma(),
                    r16var[2]: parse_float(r.temperature),
                    r16var[3]: parse_float(d[0]),
                    r16var[4]: parse_float(d[1]),
                    r16var[5]: parse_float(d[2]),
                    r16var[6]: parse_float(d[3]),
                    r16var[7]: parse_float(d[4]),
                    r16var[8]: parse_float(d[5]),
                    r16var[9]: parse_float(d[6]),
                    r16var[10]: parse_float(d[7]),
                    r16var[11]: parse_float(d[8]),
                    r16var[12]: parse_float(d[9]),
                    r16var[13]: parse_float(d[10]),
                    r16var[14]: parse_float(d[11]),
                    r16var[15]: parse_float(d[12]),
                    r16var[16]: parse_float(d[13]),
                   
                }
                data.append(j)
            
        r.data = data
        report16.items.append(r)
    return report16

def parseReport17(reportPath):
    report17 = aem_report17()
    report17.exists = True
    report17.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report17Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace('            ', ' ').replace('         ',' ').replace('        ',' ').replace('       ',' ').replace('      ',' ').replace('     ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')
            d = f.strip().split(" ")
            if len(d) == 11:
                j = {
                    r17var[0]: r.solvents_str_no_comma(),
                    r17var[1]: r.salts_str_no_comma(),
                    r17var[2]: parse_float(r.temperature),
                    r17var[3]: parse_float(d[0]),
                    r17var[4]: parse_float(d[1]),
                    r17var[5]: parse_float(d[2]),
                    r17var[6]: parse_float(d[3]),
                    r17var[7]: parse_float(d[4]),
                    r17var[8]: parse_float(d[5]),
                    r17var[9]: parse_float(d[6]),
                    r17var[10]: parse_float(d[7]),
                    r17var[11]: parse_float(d[8]),
                    r17var[12]: parse_float(d[9]),
                    r17var[13]: parse_float(d[10]),
                    
                }
                data.append(j)
            
        r.data = data
        report17.items.append(r)
    return report17

def parseReport18(reportPath):
    report18 = aem_report18()
    report18.exists = True
    report18.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report18Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 17:
                j = {
                    r18var[0]: r.solvents_str_no_comma(),
                    r18var[1]: r.salts_str_no_comma(),
                    r18var[2]: parse_float(r.temperature),
                    r18var[3]: parse_float(d[0]),
                    r18var[4]: parse_float(d[1]),
                    r18var[5]: parse_float(d[2]),
                    r18var[6]: parse_float(d[3]),
                    r18var[7]: parse_float(d[4]),
                    r18var[8]: parse_float(d[5]),
                    r18var[9]: parse_float(d[6]),
                    r18var[10]: parse_float(d[7]),
                    r18var[11]: parse_float(d[8]),
                    r18var[12]: parse_float(d[9]),
                    r18var[13]: parse_float(d[10]),
                    r18var[14]: parse_float(d[11]),
                    r18var[15]: parse_float(d[12]),
                    r18var[16]: parse_float(d[13]),
                    r18var[17]: parse_float(d[14]),
                    r18var[18]: parse_float(d[15]),
                    r18var[19]: parse_float(d[16]),
                    
                }
                data.append(j)
            
        r.data = data
        report18.items.append(r)
    return report18

def parseReport19(reportPath):
    report19 = aem_report19()
    report19.exists = True
    report19.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report19Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 17:
                j = {
                    r19var[0]: r.solvents_str_no_comma(),
                    r19var[1]: r.salts_str_no_comma(),
                    r19var[2]: parse_float(r.temperature),
                    r19var[3]: parse_float(d[0]),
                    r19var[4]: parse_float(d[1]),
                    r19var[5]: parse_float(d[2]),
                    r19var[6]: parse_float(d[3]),
                    r19var[7]: parse_float(d[4]),
                    r19var[8]: parse_float(d[5]),
                    r19var[9]: parse_float(d[6]),
                    r19var[10]: parse_float(d[7]),
                    r19var[11]: parse_float(d[8]),
                    r19var[12]: parse_float(d[9]),
                    r19var[13]: parse_float(d[10]),
                    r19var[14]: parse_float(d[11]),
                    r19var[15]: parse_float(d[12]),
                    r19var[16]: parse_float(d[13]),
                    r19var[17]: parse_float(d[14]),
                    r19var[18]: parse_float(d[15]),
                    r19var[19]: parse_float(d[16]),
                    
                }
                data.append(j)
            
        r.data = data
        report19.items.append(r)
    return report19

def parseReport20(reportPath):
    report20 = aem_report20()
    report20.exists = True
    report20.path = reportPath
    f=open(reportPath)
    text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    for content in contents:
        data = []
        r = report20Item()
        solC = []
        content =content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        foo = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1].splitlines()
        for fo in foo:
            f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
            d = f.strip().split(" ")
            if len(d) == 17:
                j = {
                    r20var[0]: r.solvents_str_no_comma(),
                    r20var[1]: r.salts_str_no_comma(),
                    r20var[2]: parse_float(r.temperature),
                    r20var[3]: parse_float(d[0]),
                    r20var[4]: parse_float(d[1]),
                    r20var[5]: parse_float(d[2]),
                    r20var[6]: parse_float(d[3]),
                    r20var[7]: parse_float(d[4]),
                    r20var[8]: parse_float(d[5]),
                    r20var[9]: parse_float(d[6]),
                    r20var[10]: parse_float(d[7]),
                    r20var[11]: parse_float(d[8]),
                    r20var[12]: parse_float(d[9]),
                    r20var[13]: parse_float(d[10]),
                    r20var[14]: parse_float(d[11]),
                    r20var[15]: parse_float(d[12]),
                    r20var[16]: parse_float(d[13]),
                    r20var[17]: parse_float(d[14]),
                    r20var[18]: parse_float(d[15]),
                    r20var[19]: parse_float(d[16]),
                    
                }
                data.append(j)
            
        r.data = data
        report20.items.append(r)
    return report20

## aem_convert_to_csv thread definitions
def write_report_01_csv(run, path):
    run.report01.save_all_csv(path)
def write_report_02_csv(run, path):
    run.report02.save_all_csv(path)
def write_report_03_csv(run, path):
    run.report03.save_all_csv(path)
def write_report_04_csv(run, path):
    run.report04.save_all_csv(path)
def write_report_05_csv(run, path):
    run.report05.save_all_csv(path)
def write_report_06_csv(run, path):
    run.report06.save_all_csv(path)
def write_report_10_csv(run, path):
    run.report10.save_all_csv(path)
def write_report_11_csv(run, path):
    run.report11.save_all_csv(path)
def write_report_12_csv(run, path):
    run.report12.save_all_csv(path)
def write_report_13_csv(run, path):
    run.report13.save_all_csv(path)
def write_report_14_csv(run, path):
    run.report14.save_all_csv(path)
def write_report_15_csv(run, path):
    run.report15.save_all_csv(path)
def write_report_16_csv(run, path):
    run.report16.save_all_csv(path)
def write_report_17_csv(run, path):
    run.report17.save_all_csv(path)
def write_report_18_csv(run, path):
    run.report18.save_all_csv(path)
def write_report_19_csv(run, path):
    run.report19.save_all_csv(path)
def write_report_20_csv(run, path):
    run.report20.save_all_csv(path)

## aem_convert_to_csv Function
def aem_convert_to_csv(dir):
    print(f"### AEM-PARSER v1.1.0:: Starting .csv conversion...")
    start_time = time.time()
    if (os.path.isdir(dir)):
        run = aem_run()
        run.parse_run(dir)
        d = os.path.join(dir, 'csv')
        if os.path.exists(d) == False:
            try: 
                os.mkdir(d)
            except OSError as error:
                print(f'### AEM-PARSER v1.1.0::Error Occured creating {d} directory: {error}')
                os._exit(0)
        if (run.report01.exists):
            t1 = threading.Thread(target=write_report_01_csv, args=(run,os.path.join(d, 'Report01.csv')))
        if (run.report02.exists):
            t2 = threading.Thread(target=write_report_02_csv, args=(run,os.path.join(d, 'Report02.csv')))
        if (run.report03.exists):
            t3 = threading.Thread(target=write_report_03_csv, args=(run,os.path.join(d, 'Report03.csv')))
        if (run.report04.exists):
            t4 = threading.Thread(target=write_report_04_csv, args=(run,os.path.join(d, 'Report04.csv')))
        if (run.report05.exists):
            t5 = threading.Thread(target=write_report_05_csv, args=(run,os.path.join(d, 'Report05.csv')))
        if (run.report06.exists):
            t6 = threading.Thread(target=write_report_06_csv, args=(run,os.path.join(d, 'Report06.csv')))
        if (run.report10.exists):
            t10 = threading.Thread(target=write_report_10_csv, args=(run,os.path.join(d, 'Report10.csv')))
        if (run.report11.exists):
            t11 = threading.Thread(target=write_report_11_csv, args=(run,os.path.join(d, 'Report11.csv')))
        if (run.report12.exists):
            t12 = threading.Thread(target=write_report_12_csv, args=(run,os.path.join(d, 'Report12.csv')))
        if (run.report13.exists):
            t13 = threading.Thread(target=write_report_13_csv, args=(run,os.path.join(d, 'Report13.csv')))
        if (run.report14.exists):
            t14 = threading.Thread(target=write_report_14_csv, args=(run,os.path.join(d, 'Report14.csv')))
        if (run.report15.exists):
            t15 = threading.Thread(target=write_report_15_csv, args=(run,os.path.join(d, 'Report15.csv')))
        if (run.report16.exists):
            t16 = threading.Thread(target=write_report_16_csv, args=(run,os.path.join(d, 'Report16.csv')))
        if (run.report17.exists):
            t17 = threading.Thread(target=write_report_17_csv, args=(run,os.path.join(d, 'Report17.csv')))
        if (run.report18.exists):
            t18 = threading.Thread(target=write_report_18_csv, args=(run,os.path.join(d, 'Report18.csv')))
        if (run.report19.exists):
            t19 = threading.Thread(target=write_report_19_csv, args=(run,os.path.join(d, 'Report19.csv')))
        if (run.report20.exists):
            t20 = threading.Thread(target=write_report_20_csv, args=(run,os.path.join(d, 'Report20.csv')))
        
        if 't1' in locals():
            t1.start()
        if 't2' in locals():
            t2.start()
        if 't3' in locals():
            t3.start()
        if 't4' in locals():
            t4.start()
        if 't5' in locals():
            t5.start()
        if 't6' in locals():
            t6.start()
        if 't10' in locals():
            t10.start()
        if 't11' in locals():
            t11.start()
        if 't12' in locals():
            t12.start()
        if 't13' in locals():
            t13.start()
        if 't14' in locals():
            t14.start()
        if 't15' in locals():
            t15.start()
        if 't16' in locals():
            t16.start()
        if 't17' in locals():
            t17.start()
        if 't18' in locals():
            t18.start()
        if 't19' in locals():
            t19.start()
        if 't20' in locals():
            t20.start()
        if 't1' in locals():
            t1.join()
        if 't2' in locals():
            t2.join()
        if 't3' in locals():
            t3.join()
        if 't4' in locals():
            t4.join()
        if 't5' in locals():
            t5.join()
        if 't6' in locals():
            t6.join()
        if 't10' in locals():
            t10.join()
        if 't11' in locals():
            t11.join()
        if 't12' in locals():
            t12.join()
        if 't13' in locals():
            t13.join()
        if 't14' in locals():
            t14.join()
        if 't15' in locals():
            t15.join()
        if 't16' in locals():
            t16.join()
        if 't17' in locals():
            t17.join()
        if 't18' in locals():
            t18.join()
        if 't19' in locals():
            t19.join()
        if 't20' in locals():
            t20.join()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"### AEM-PARSER v1.1.0:: Elapsed time: {elapsed_time} seconds")
    else:
        print(f'### AEM-PARSER v1.1.0:: {dir} does not exist')
        os._exit(0)

## aem_convert_to_json Function
def aem_convert_to_json(dir):
    print(f"### AEM-PARSER v1.1.0:: Starting .json conversion...")
    if (os.path.isdir(dir)):
        run = aem_run()
        run.parse_run(dir)
        d = os.path.join(dir, 'json')
        try: 
            os.mkdir(d)
        except OSError as error:
            print(f'### AEM-PARSER v1.1.0:: Error Occured creating {d} directory: {error}')
            os._exit(0)
        if (run.report01.exists):
            p = os.path.join(d, 'Report01.json')
            f = open(p, "w")
            f.write(run.report01.all_json())
            f.close()
        if (run.report02.exists):
            p = os.path.join(d, 'Report02.json')
            f = open(p, "w")
            f.write(run.report02.all_json())
            f.close()
        if (run.report03.exists):
            p = os.path.join(d, 'Report03.json')
            f = open(p, "w")
            f.write(run.report03.all_json())
            f.close()
        if (run.report04.exists):
            p = os.path.join(d, 'Report04.json')
            f = open(p, "w")
            f.write(run.report04.all_json())
            f.close()
        if (run.report05.exists):
            p = os.path.join(d, 'Report05.json')
            f = open(p, "w")
            f.write(run.report05.all_json())
            f.close()
        if (run.report06.exists):
            p = os.path.join(d, 'Report06.json')
            f = open(p, "w")
            f.write(run.report06.all_json())
            f.close()
        if (run.report10.exists):
            p = os.path.join(d, 'Report10.json')
            f = open(p, "w")
            f.write(run.report10.all_json())
            f.close()
        if (run.report11.exists):
            p = os.path.join(d, 'Report11.json')
            f = open(p, "w")
            f.write(run.report11.all_json())
            f.close()
        if (run.report12.exists):
            p = os.path.join(d, 'Report12.json')
            f = open(p, "w")
            f.write(run.report12.all_json())
            f.close()
        if (run.report13.exists):
            p = os.path.join(d, 'Report13.json')
            f = open(p, "w")
            f.write(run.report13.all_json())
            f.close()
        if (run.report14.exists):
            p = os.path.join(d, 'Report14.json')
            f = open(p, "w")
            f.write(run.report14.all_json())
            f.close()
        if (run.report15.exists):
            p = os.path.join(d, 'Report15.json')
            f = open(p, "w")
            f.write(run.report15.all_json())
            f.close()
        if (run.report16.exists):
            p = os.path.join(d, 'Report16.json')
            f = open(p, "w")
            f.write(run.report16.all_json())
            f.close()
        if (run.report17.exists):
            p = os.path.join(d, 'Report17.json')
            f = open(p, "w")
            f.write(run.report17.all_json())
            f.close()
        if (run.report18.exists):
            p = os.path.join(d, 'Report18.json')
            f = open(p, "w")
            f.write(run.report18.all_json())
            f.close()
        if (run.report19.exists):
            p = os.path.join(d, 'Report19.json')
            f = open(p, "w")
            f.write(run.report19.all_json())
            f.close()
        if (run.report20.exists):
            p = os.path.join(d, 'Report20.json')
            f = open(p, "w")
            f.write(run.report20.all_json())
            f.close()
        print(f"### AEM-PARSER v1.1.0:: Finished .json conversion!")
    else:
        print(f'### AEM-PARSER v1.1.0:: {sys.argv[1]} does not exist!')
        os._exit(0)
