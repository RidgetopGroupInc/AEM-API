# ============================================================================
"""             Advanced Electrolyte Model (AEM) PARSER v1.2.0            """
"""            © 2025 Ridgetop Group, Inc., All Rights Reserved            """
# ============================================================================

## Import Libraries
import os
import json
import sys
import threading
import time
from typing import List

SOLVENT_ABBREVIATIONS = {
    "water": "water",
    "propylene carbonate": "PC",
    "ethylene carbonate": "EC",
    "gamma-butyrolactone": "GBL",
    "1,2 dimethoxyethane": "DME",
    "ethylmethyl carbonate": "EMC",
    "diethyl carbonate": "DEC",
    "dimethyl carbonate": "DMC",
    "ethyl acetate": "EA",
    "1,3 dioxolane": "DIOXOLANE",
    "methyl butyrate": "MB",
    "ethyl propionate": "EP",
    "n-propyl acetate": "nPA",
    "ethylene glycol": "EG",
    "fluoroethylene carbonate": "FEC",
    "ethylmethoxyethyl sulfone": "EMES",
    "Dowanol-PMA": "DOW-PMA",
    "2-methoxyethyl acetate": "MEA",
    "1NM2-siloxane": "1NM2",
    "DEGDME diglyme": "DEGDME",
    "3-TEGDME triglyme": "3-TEGDME",
    "4-TEGDME tetraglyme": "4-TEGDME",
    "INL Additive FM2": "FM2",
    "INL Additive SM4": "SM4",
    "INL Additive PA5": "PA5",
    "glutaronitrile": "GLN",
    "adiponitrile": "AND",
    "ethylmethyl sulfone": "EMS",
    "methyl acetate": "MA",
    "methyl propionate": "MP",
    "methyl formate": "MF",
    "ethyl formate": "EF",
    "propionitrile": "PrN",
    "sulfolane": "TMS",
    "trimethyl phosphate(TMP)": "TMP",
    "acetonitrile": "ACN",
    "methyl monofluoroacetate": "M1FA",
    "methyl difluoroacetate": "M2FA",
    "vinylene carbonate": "VC",
    "n-propyl proprionate": "nPP",
    "butyronitrile (BN)": "BN",
    "n-butyl acetate": "nBA",
    "n-butyl propionate": "nBP",
    "n-butyl butyrate": "nBB",
    "vinyl ethylene carbonate": "VEC",
    "Tris(2,2,2-trifluoroethyl)-orthoformate TFEO": "TFEO",
    "succinonitrile": "SN",
    "Dimethyl 2,5, Dioxahexanedioate DMOHC": "DMOHC",
    "Diethyl 2,5, Dioxahexanedioate DEOHC": "DEOHC",
    "7-oxabicyclo[2.2.1]heptane-2-carbonitrile OCN": "OCN",
    "tetrahydrofuran": "THF",
    "triethyl phosphate": "TEP",
    "Bis(2,2,2-trifluoroethyl) ether BTFE": "BTFE",
    "1,1,2,2-tetrafluoroethyl-2,2,3,3-tetrafluoropropyl ether TTE": "TTE",
    "ethyl difluoroacetate": "E2FA",
    "1,2-dimethoxypropane": "DMP",
    "dimethyl sulfite": "DMS",
    "isovaleronitrile": "IVN",
    "isobutyronitrile": "IBN"
}

## aem_run CLASS
class aem_run:
    def __init__(self):
        self.name = None
        self.report01: 'aem_report01' = aem_report01()
        self.report02: 'aem_report02' = aem_report02()
        self.report03: 'aem_report03' = aem_report03()
        self.report04: 'aem_report04' = aem_report04()
        self.report05: 'aem_report05' = aem_report05()
        self.report06: 'aem_report06' = aem_report06()
        self.report10: 'aem_report10' = aem_report10()
        self.report11: 'aem_report11' = aem_report11()
        self.report12: 'aem_report12' = aem_report12()
        self.report13: 'aem_report13' = aem_report13()
        self.report14: 'aem_report14' = aem_report14()
        self.report15: 'aem_report15' = aem_report15()
        self.report16: 'aem_report16' = aem_report16()
        self.report17: 'aem_report17' = aem_report17()
        self.report18: 'aem_report18' = aem_report18()
        self.report19: 'aem_report19' = aem_report19()
        self.report20: 'aem_report20' = aem_report20()

    def parse_run(self, runDirPath):
        reports = os.listdir(runDirPath)
        for report in reports:
            parseReport(os.sep.join([runDirPath, report]), self)

## aem_report CLASS
class aem_report:
    def __init__(self):
        self.path: str = ''
        self.version = '2.24.3'
        self.items = []
        self.exists = False
        self.isEmpty = False
        self.target_solvent_comp = None
        self.target_salt_comp = None

    def all_json(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        return json.dumps(all_data, indent=4)

# Report Variables
r01var_2242 = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'c2_eff_trans', 'wt_fr_salt', 'mole_fr_salt', 'density',
    'visc', 'sig1', 'sig2', 's_plus', 'rational_act_coeff', 'diff_coeff', 'spec_cond', 't_plus_a', 't_plus_b', 
    'dissoc_si', 'dissoc_ti'
]
r01var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'c2_eff_trans', 'wt_fr_salt', 'mole_fr_salt', 'density', 'visc',
    'sig1', 'sig2', 's_plus', 'rational_act_coeff', 'diff_coeff', 'spec_cond', 't_plus_a', 't_plus_b', 'salt_dissoc_si', 
    'salt_dissoc_ip', 'dissoc_ti'
]
r02var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'cmeff', 'alphanet', 'cation', 'anion', 'ip', 'ti', 'fcip', 'gamma',
    'y', 'y_bar', 'osmotic_coeff_molal', 'osmotic_coeff_molar', 'solvent_activity', 'kip', 'kti', 'ksol', 'adj_solvent_activity',
    'adj_phi', 'adj_gamma', 'fvpd'
]
r03var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'gfe_cation', 'gfe_anion', 'se_cation', 'se_anion', 'rp_solution',
    'rp_solvent', 'alpha1', 'alpha3', 'energy_sum', 'energy_ave', 'desolve_t'
]
r04var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'volsoft', 'fcomp', 'fsolv', 'fdiff12', 'd_plus', 'd_minus',
    'd_minus_bare', 'dnernst', 'dapp', 'd_ip', 'd_ti', 'd_solvent', 'thermodynamic_factor'
]
r05var_2242 = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'c2_pseudo', 'density', 'visc', 'rational_act_coef_y', 'diffusion_coeff',
    'specific_conductivity', 't_plus', 't_minus', 'fhop_plus', 'fhop_minus', 'pos_atm', 'walden_log_1_over_visc', 'walden_log_cond',
    'walden_product', 'thermal_conductivity'
]
r05var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'c2_eff_trans', 'c2_pseudo', 'density', 'visc', 'rational_act_coef_y',
    'diffusion_coeff', 'specific_conductivity', 't_plus', 't_minus', 'fhop_plus', 'fhop_minus', 'pos_atm', 'walden_log_1_over_visc',
    'walden_log_cond', 'walden_product', 'thermal_conductivity'
]
r06var = [
    'solvent_comp', 'salt_comp', 'temperature', 'salt_molality', 'one_over_visc', 'k_t_plus', 'diffusivity_bulk_elec', 'li_step_full',
    'li_step_solv', 'kip', 'kti', 'ksolv', 'solvent_activity', 'gamma'
]
r10var = [
    'solvent_comp', 'salt_comp', 'temperature', 'surface_charge_density', 'cell_voltage_at_start_of_pulse', 'salt_concentration_basis', 
    'pulse_type', 'electrolyte_rel_perm_at_salt_conc', 'dipole_moment_data', 'solvent_diameter', 'equivalent_charge_on_solvent_dipole', 
    'sei_thickness', 'sei_porosity', 'sei_relative_permittivity', 'r', 'eff_surface_ch_density_at_r', 'solution_rel_perm_electrolyte_plus_sch', 
    'ave_r_solution_rel_perm_electrolyte_plus_sch', 'electric_field_per_sch', 'repulsive_energy_sch_to_dipole', 'cell_voltage'
]
r11var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'cation_eff_dia', 'anion_eff_dia', 's_plus_th', 's_minus_th', 'solvent_avail_thermo', 
    'solvent_avail_msa_hs', 'solvent_be_to_cation', 'solvent_be_to_anion', 'communal_solvation_factor', 'debye_relaxation_time', 
    'fraction_of_free_liquid_in_solvent'
]
r12var_2242 = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'cation_solvent_one', 'cation_solvent_two', 'cation_solvent_three', 
    'cation_solvent_four', 'cation_solvent_five', 'anion_solvent_one', 'anion_solvent_two', 'anion_solvent_three', 
    'anion_solvent_four', 'anion_solvent_five'
]
r12var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'cation_solvent_one', 'cation_solvent_two', 'cation_solvent_three', 
    'cation_solvent_four', 'cation_solvent_five', 'cation_solvent_six', 'cation_solvent_seven', 'cation_solvent_eight', 
    'cation_solvent_nine', 'cation_solvent_ten', 'anion_solvent_one', 'anion_solvent_two', 'anion_solvent_three', 
    'anion_solvent_four', 'anion_solvent_five', 'anion_solvent_six', 'anion_solvent_seven', 'anion_solvent_eight', 
    'anion_solvent_nine', 'anion_solvent_ten'
]
r13var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'cation_factor_one', 'cation_factor_two', 'cation_factor_three', 
    'cation_factor_four', 'cation_factor_five', 'cation_factor_six', 'cation_factor_seven', 'anion_factor_one', 'anion_factor_two', 
    'anion_factor_three', 'anion_factor_four', 'anion_factor_five', 'anion_factor_six', 'anion_factor_seven'
]
r14var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'full_li_step_parameter', 'partial_li_step_parameter'
]
r15var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', '10_v1', '10_t1', '20_v1', '20_t1', '40_v1', '40_t1', '80_v1',
    '80_t1', '160_v1', '160_t1', '320_v1', '320_t1', 'vsolv', 'tsolv'
]
r16var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'surface_tension', 'surface_ten_viscosity', '0.02_micron', 
    '0.05_micron', '0.1_micron', '0.2_micron', '0.5_micron', '1_micron', '2_micron', '5_micron', '10_micron', '20_micron'
]
r17var = [
    'solvent_comp', 'salt_comp', 'temperature', 'time_s', '0.02_micron', '0.05_micron', '0.1_micron', '0.2_micron',
    '0.5_micron', '1_micron', '2_micron', '5_micron', '10_micron', '20_micron'
]
r18var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'be1', 'be2', 'be3', 'be4', 'be5', 'be6', 'be_sum', 'dt1', 
    'dt2', 'dt3', 'dt4', 'dt5', 'dt6', 'dt_sum', 't_lambda'
]
r19var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2', 'c2', 'be1', 'be2', 'be3', 'be4', 'be5', 'be6', 'be_sum', 'dt1',
    'dt2', 'dt3', 'dt4', 'dt5', 'dt6', 'dt_sum', 't_lambda'
]
r20var = [
    'solvent_comp', 'salt_comp', 'temperature', 'm2_bulk', 'm2_non_cs', 'm2_cs', 'y_free', 'y_non_cs', 'y_cs',
    'cs_factor', 'n_s_plus_bulk', 'n_s_plus_cs', 'n_s_plus_ave', 'be_plus_bulk', 'be_plus_cs', 'be_plus_ave',
    'n_s_cs_0', 'n_s_cs_ave', 'n_s_non_cs', 'ratio_of_n_solv_cs_to_m2_cs'
]

## Helper Functions
def parse_float(value):
    """Convert string to float, handling asterisks and invalid values as NaN."""
    if not value or value in ('********', '*****', '*DNC*'):
        return float('nan')
    try:
        return float(value)
    except ValueError:
        return float('nan')

def isfloat(value):
    """Check if a string can be converted to float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def getReportVersionNumber(text):
    """Extract AEM version number from report text."""
    lines = text.splitlines()
    for line in lines:
        if "AEM ver." in line:
            return line.split("AEM ver.")[1].strip().split()[0]
    return '2.24.3'  # Default to latest if not found

## aem_reportXX CLASS (XX - Report No.)
class aem_report01(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        if self.version == '2.24.2':
            c = f'{",".join(r01var_2242)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r01var_2242)}\n'
        else:  # 2.24.3
            c = f'{",".join(r01var)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r01var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            if self.version == '2.24.2':
                f.write(f'{",".join(r01var_2242)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r01var_2242)}\n')
            else:  # 2.24.3
                f.write(f'{",".join(r01var)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r01var)}\n')

class aem_report02(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r02var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r02var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r02var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r02var)}\n')

class aem_report03(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r03var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r03var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r03var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r03var)}\n')

class aem_report04(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r04var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r04var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r04var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r04var)}\n')

class aem_report05(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        if self.version == '2.24.2':
            c = f'{",".join(r05var_2242)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r05var_2242)}\n'
        else:  # 2.24.3
            c = f'{",".join(r05var)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r05var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            if self.version == '2.24.2':
                f.write(f'{",".join(r05var_2242)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r05var_2242)}\n')
            else:  # 2.24.3
                f.write(f'{",".join(r05var)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r05var)}\n')

class aem_report06(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r06var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r06var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r06var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r06var)}\n')

class aem_report10(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r10var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r10var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r10var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r10var)}\n')

class aem_report11(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r11var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r11var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r11var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r11var)}\n')

class aem_report12(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        if self.version == '2.24.2':
            c = f'{",".join(r12var_2242)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r12var_2242)}\n'
        else:
            c = f'{",".join(r12var)}\n'
            for d in all_data:
                c += f'{",".join(str(d.get(var, "")) for var in r12var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            if self.version == '2.24.2':
                f.write(f'{",".join(r12var_2242)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r12var_2242)}\n')
            else:
                f.write(f'{",".join(r12var)}\n')
                for d in all_data:
                    f.write(f'{",".join(str(d.get(var, "")) for var in r12var)}\n')

class aem_report13(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r13var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r13var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r13var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r13var)}\n')

class aem_report14(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r14var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r14var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r14var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r14var)}\n')

class aem_report15(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r15var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r15var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r15var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r15var)}\n')

class aem_report16(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r16var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r16var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r16var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r16var)}\n')

class aem_report17(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r17var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r17var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r17var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r17var)}\n')

class aem_report18(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r18var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r18var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r18var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r18var)}\n')

class aem_report19(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r19var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r19var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r19var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r19var)}\n')

class aem_report20(aem_report):
    def all_csv(self):
        all_data = []
        for item in self.items:
            for i in item.data:
                all_data.append(i)
        c = f'{",".join(r20var)}\n'
        for d in all_data:
            c += f'{",".join(str(d.get(var, "")) for var in r20var)}\n'
        return c

    def save_all_csv(self, path):
        if os.path.exists(path):
            os.remove(path)
        with open(path, "a") as f:
            all_data = []
            for item in self.items:
                for i in item.data:
                    all_data.append(i)
            f.write(f'{",".join(r20var)}\n')
            for d in all_data:
                f.write(f'{",".join(str(d.get(var, "")) for var in r20var)}\n')

## solventComp and saltComp CLASS
class solventComp:
    def __init__(self):
        self.name = None
        self.proportion = None

    def __str__(self):
        return f"{self.name} {self.proportion}"

class saltComp:
    def __init__(self):
        self.name = None
        self.proportion = None

    def __str__(self):
        return f"{self.name} {self.proportion}"

## reportItem CLASS
class reportItem:
    def __init__(self):
        self.version: str = '2.24.3'
        self.solvents: List[solventComp] = []
        self.salts: List[saltComp] = []
        self.temperature: float = None
        self.data = []

    def salts_str(self):
        return ','.join(str(s) for s in self.salts)

    def salts_str_no_comma(self):
        return ' | '.join(str(s) for s in self.salts)

    def solvents_str(self):
        return ','.join(str(s) for s in self.solvents)

    def solvents_str_no_comma(self):
        return ' | '.join(str(s) for s in self.solvents)

    def temperature_str(self):
        return f'{self.temperature}°C' if self.temperature is not None else ''

    def json_data(self):
        return json.dumps(self.data, indent=4)

## aem_reportXXItem CLASS (XX - Report No.)
class report01Item(reportItem):
    pass

class report02Item(reportItem):
    pass

class report03Item(reportItem):
    pass

class report04Item(reportItem):
    pass

class report05Item(reportItem):
    pass

class report06Item(reportItem):
    pass

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

class report11Item(reportItem):
    pass

class report12Item(reportItem):
    pass

class report13Item(reportItem):
    pass

class report14Item(reportItem):
    pass

class report15Item(reportItem):
    pass

class report16Item(reportItem):
    pass

class report17Item(reportItem):
    pass

class report18Item(reportItem):
    pass

class report19Item(reportItem):
    pass

class report20Item(reportItem):
    pass

## Parsing Functions
def parseReport(report, run):
    if os.path.getsize(report) == 0:
        print(f'### AEM-PARSER v1.1.0:: {os.path.basename(report)} is empty!')
        return
    if "Report01 --" in report or "Report1 --" in report:
        run.report01 = parseReport01(report)
    elif "Report02 --" in report or "Report2 --" in report:
        run.report02 = parseReport02(report)
    elif "Report03 --" in report or "Report3 --" in report:
        run.report03 = parseReport03(report)
    elif "Report04 --" in report or "Report4 --" in report:
        run.report04 = parseReport04(report)
    elif "Report05 --" in report or "Report5 --" in report:
        run.report05 = parseReport05(report)
    elif "Report06 --" in report or "Report6 --" in report:
        run.report06 = parseReport06(report)
    elif "Report10 --" in report:
        run.report10 = parseReport10(report)
    elif "Report11 --" in report:
        run.report11 = parseReport11(report)
    elif "Report12 --" in report:
        run.report12 = parseReport12(report)
    elif "Report13 --" in report:
        run.report13 = parseReport13(report)
    elif "Report14 --" in report:
        run.report14 = parseReport14(report)
    elif "Report15 --" in report:
        run.report15 = parseReport15(report)
    elif "Report16 --" in report:
        run.report16 = parseReport16(report)
    elif "Report17 --" in report:
        run.report17 = parseReport17(report)
    elif "Report18 --" in report:
        run.report18 = parseReport18(report)
    elif "Report19 --" in report:
        run.report19 = parseReport19(report)
    elif "Report20 --" in report:
        run.report20 = parseReport20(report)

def parse_composition_temperature(pieces, r):
    """Parse composition and temperature, handling binary salts and solvents correctly."""
    # Parse salts
    saltC = pieces[0].split("at Temp. =")[0].strip().replace('        ', ' ')
    saltcSplit = saltC.split(' + ')
    r.salts = []  # Clear existing salts to ensure fresh population
    if len(saltcSplit) == 1:
        # Single salt case
        parts = [p.strip() for p in saltcSplit[0].split() if p]
        if parts:
            salt = saltComp()
            if isfloat(parts[0]):
                salt.proportion = parts[0]
                salt.name = ' '.join(parts[1:]).strip()
            else:
                salt.name = ' '.join(parts).strip()
                salt.proportion = '1.000'
            r.salts.append(salt)
    else:
        # Binary salt case
        for s in saltcSplit:
            s = s.strip()
            parts = [p.strip() for p in s.split() if p]
            if parts and len(parts) >= 2 and isfloat(parts[0]):
                salt = saltComp()  # Create new salt object for each entry
                salt.proportion = parts[0]  # First part is the proportion
                salt.name = ' '.join(parts[1:]).strip()  # Remaining parts form the name
                r.salts.append(salt)
            else:
                print(f"### AEM-PARSER v1.1.0:: Warning: Invalid salt format in {r.path}: {s}")
    # Parse temperature
    temp_part = pieces[0].split("at Temp. =")[1].split("C")[0].strip()
    r.temperature = float(temp_part)  # Convert to float directly
    # Parse solvents
    solC = []
    foo = pieces[1].split('-----------------------------------------------------------------------')[1].splitlines()
    for fo in foo:
        sc = []
        fo = fo.strip()
        spl = [s.strip() for s in fo.split() if s]  # Split and filter empty strings
        if len(spl) >= 4:  # Expecting name + 3 fractions (mole, mass, volume)
            compound = []
            for s in spl:
                if isfloat(s):
                    compound.append(s)
                    break  # Stop at the first fraction (mole fraction)
                else:
                    compound.append(s)
            solC.append(' '.join(compound))
    # Filter out empty or invalid entries (replace filterNonEmpty with a list comprehension)
    solventCompostion = [s for s in solC if s and isfloat(s.split()[-1])]
    for s in solventCompostion:
        spl = s.split()
        if len(spl) >= 2:
            proportion = spl.pop()  # Last item is the proportion
            name = ' '.join(spl)  # Remaining items form the name
            solvent = solventComp()
            solvent.name = SOLVENT_ABBREVIATIONS.get(name, name)  # Use abbreviation if found
            solvent.proportion = proportion
            r.solvents.append(solvent)
        else:
            print(f"### AEM-PARSER v1.1.0:: Warning: Invalid solvent format in {r.path}: {s}")

def getReportVersionNumber(text):
    if (text.startswith('  AEM ver. 2.24.2M-D-ACCC')):
        return '2.24.2'
    elif (text.startswith('  AEM ver. 2.24.3M-D-ACCC')):
        return '2.24.3'

def parseReport01(reportPath):
    report01 = aem_report01()
    report01.exists = True
    report01.path = reportPath
    report01.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report01Item()
        r.version = report01.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report01.target_solvent_comp = r.solvents_str_no_comma()
            report01.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report01.target_solvent_comp and r.salts_str_no_comma() == report01.target_salt_comp:
            try:
                table_section = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 17 and report01.version == '2.24.2':
                    j = {r01var_2242[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r01var_2242))}
                    j.update({
                        r01var_2242[0]: r.solvents_str_no_comma(),
                        r01var_2242[1]: r.salts_str_no_comma(),
                        r01var_2242[2]: r.temperature
                    })
                    data.append(j)
                elif len(d) == 18 and report01.version == '2.24.3':
                    j = {r01var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r01var))}
                    j.update({
                        r01var[0]: r.solvents_str_no_comma(),
                        r01var[1]: r.salts_str_no_comma(),
                        r01var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report01.items.append(r)
    return report01

def parseReport02(reportPath):
    report02 = aem_report02()
    report02.exists = True
    report02.path = reportPath
    report02.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report02Item()
        r.version = report02.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report02.target_solvent_comp = r.solvents_str_no_comma()
            report02.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report02.target_solvent_comp and r.salts_str_no_comma() == report02.target_salt_comp:
            try:
                table_section = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 22:
                    j = {r02var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r02var))}
                    j.update({
                        r02var[0]: r.solvents_str_no_comma(),
                        r02var[1]: r.salts_str_no_comma(),
                        r02var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report02.items.append(r)
    return report02

def parseReport03(reportPath):
    report03 = aem_report03()
    report03.exists = True
    report03.path = reportPath
    report03.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report03Item()
        r.version = report03.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report03.target_solvent_comp = r.solvents_str_no_comma()
            report03.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report03.target_solvent_comp and r.salts_str_no_comma() == report03.target_salt_comp:
            try:
                table_section = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                for sep in ['----', '===', '\n\n']:
                    if sep in pieces[1]:
                        table_section = pieces[1].split(sep)[-1]
                        break
                else:
                    print(f"### AEM-PARSER v1.1.0:: Failed to find table separator in {reportPath}")
                    table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("*DNC*", "").replace('/', '')
                d = f.strip().split()
                if len(d) == 13:
                    j = {r03var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r03var))}
                    j.update({
                        r03var[0]: r.solvents_str_no_comma(),
                        r03var[1]: r.salts_str_no_comma(),
                        r03var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report03.items.append(r)
    return report03

def parseReport04(reportPath):
    report04 = aem_report04()
    report04.exists = True
    report04.path = reportPath
    report04.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report04Item()
        r.version = report04.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report04.target_solvent_comp = r.solvents_str_no_comma()
            report04.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report04.target_solvent_comp and r.salts_str_no_comma() == report04.target_salt_comp:
            try:
                table_section = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 15:
                    j = {r04var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r04var))}
                    j.update({
                        r04var[0]: r.solvents_str_no_comma(),
                        r04var[1]: r.salts_str_no_comma(),
                        r04var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report04.items.append(r)
    return report04

def parseReport05(reportPath):
    report05 = aem_report05()
    report05.exists = True
    report05.path = reportPath
    report05.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report05Item()
        r.version = report05.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report05.target_solvent_comp = r.solvents_str_no_comma()
            report05.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report05.target_solvent_comp and r.salts_str_no_comma() == report05.target_salt_comp:
            try:
                table_section = pieces[1].split('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 17 and report05.version == '2.24.2':
                    j = {r05var_2242[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r05var_2242))}
                    j.update({
                        r05var_2242[0]: r.solvents_str_no_comma(),
                        r05var_2242[1]: r.salts_str_no_comma(),
                        r05var_2242[2]: r.temperature
                    })
                    data.append(j)
                elif len(d) == 18 and report05.version == '2.24.3':
                    j = {r05var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r05var))}
                    j.update({
                        r05var[0]: r.solvents_str_no_comma(),
                        r05var[1]: r.salts_str_no_comma(),
                        r05var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report05.items.append(r)
    return report05

def parseReport06(reportPath):
    report06 = aem_report06()
    report06.exists = True
    report06.path = reportPath
    report06.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report06Item()
        r.version = report06.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report06.target_solvent_comp = r.solvents_str_no_comma()
            report06.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report06.target_solvent_comp and r.salts_str_no_comma() == report06.target_salt_comp:
            try:
                table_section = pieces[1].split('--------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 11:
                    j = {r06var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r06var))}
                    j.update({
                        r06var[0]: r.solvents_str_no_comma(),
                        r06var[1]: r.salts_str_no_comma(),
                        r06var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report06.items.append(r)
    return report06

def parse_report_10_specific_variables(pieces, r: report10Item):
    try:
        body = pieces[1].split('\n  \n  \n')
        lines = body[1].splitlines()
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
    except IndexError:
        print(f"### AEM-PARSER v1.1.0:: Warning: Incomplete Report10 specific variables parsing")

def parseReport10(reportPath):
    report10 = aem_report10()
    report10.exists = True
    report10.path = reportPath
    report10.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report10Item()
        r.version = report10.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report10.target_solvent_comp = r.solvents_str_no_comma()
            report10.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report10.target_solvent_comp and r.salts_str_no_comma() == report10.target_salt_comp:
            parse_report_10_specific_variables(pieces, r)
            try:
                table_section = pieces[1].split('------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 7:
                    j = {r10var[i]: parse_float(d[i-14]) if i > 13 else d[i-14] for i in range(14, len(r10var))}
                    j.update({
                        r10var[0]: r.solvents_str_no_comma(),
                        r10var[1]: r.salts_str_no_comma(),
                        r10var[2]: r.temperature,
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
                        r10var[13]: r.sei_relative_permittivity
                    })
                    data.append(j)
            r.data = data
            report10.items.append(r)
    return report10

def parseReport11(reportPath):
    report11 = aem_report11()
    report11.exists = True
    report11.path = reportPath
    report11.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report11Item()
        r.version = report11.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report11.target_solvent_comp = r.solvents_str_no_comma()
            report11.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report11.target_solvent_comp and r.salts_str_no_comma() == report11.target_salt_comp:
            try:
                table_section = pieces[1].split('-------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 13:
                    j = {r11var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r11var))}
                    j.update({
                        r11var[0]: r.solvents_str_no_comma(),
                        r11var[1]: r.salts_str_no_comma(),
                        r11var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report11.items.append(r)
    return report11

def parseReport12(reportPath):
    report12 = aem_report12()
    report12.exists = True
    report12.path = reportPath
    report12.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report12Item()
        r.version = report12.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report12.target_solvent_comp = r.solvents_str_no_comma()
            report12.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report12.target_solvent_comp and r.salts_str_no_comma() == report12.target_salt_comp:
            try:
                table_section = pieces[1].split('-------------------------------------------------------------------------------------------------------------------------------------------------------------' if report12.version == '2.24.3' else '-----------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 12 and report12.version == '2.24.2':
                    j = {r12var_2242[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r12var_2242))}
                    j.update({
                        r12var_2242[0]: r.solvents_str_no_comma(),
                        r12var_2242[1]: r.salts_str_no_comma(),
                        r12var_2242[2]: r.temperature
                    })
                    data.append(j)
                elif len(d) == 22 and report12.version == '2.24.3':
                    j = {r12var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r12var))}
                    j.update({
                        r12var[0]: r.solvents_str_no_comma(),
                        r12var[1]: r.salts_str_no_comma(),
                        r12var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report12.items.append(r)
    return report12

def parseReport13(reportPath):
    report13 = aem_report13()
    report13.exists = True
    report13.path = reportPath
    report13.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report13Item()
        r.version = report13.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report13.target_solvent_comp = r.solvents_str_no_comma()
            report13.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report13.target_solvent_comp and r.salts_str_no_comma() == report13.target_salt_comp:
            try:
                table_section = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 16:
                    j = {r13var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r13var))}
                    j.update({
                        r13var[0]: r.solvents_str_no_comma(),
                        r13var[1]: r.salts_str_no_comma(),
                        r13var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report13.items.append(r)
    return report13

def parseReport14(reportPath):
    report14 = aem_report14()
    report14.exists = True
    report14.path = reportPath
    report14.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report14Item()
        r.version = report14.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report14.target_solvent_comp = r.solvents_str_no_comma()
            report14.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report14.target_solvent_comp and r.salts_str_no_comma() == report14.target_salt_comp:
            try:
                table_section = pieces[1].split('----------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 4:
                    j = {r14var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r14var))}
                    j.update({
                        r14var[0]: r.solvents_str_no_comma(),
                        r14var[1]: r.salts_str_no_comma(),
                        r14var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report14.items.append(r)
    return report14

def parseReport15(reportPath):
    report15 = aem_report15()
    report15.exists = True
    report15.path = reportPath
    report15.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report15Item()
        r.version = report15.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report15.target_solvent_comp = r.solvents_str_no_comma()
            report15.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report15.target_solvent_comp and r.salts_str_no_comma() == report15.target_salt_comp:
            try:
                table_section = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("           ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 16:
                    j = {r15var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r15var))}
                    j.update({
                        r15var[0]: r.solvents_str_no_comma(),
                        r15var[1]: r.salts_str_no_comma(),
                        r15var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report15.items.append(r)
    return report15

def parseReport16(reportPath):
    report16 = aem_report16()
    report16.exists = True
    report16.path = reportPath
    report16.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report16Item()
        r.version = report16.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report16.target_solvent_comp = r.solvents_str_no_comma()
            report16.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report16.target_solvent_comp and r.salts_str_no_comma() == report16.target_salt_comp:
            try:
                table_section = pieces[1].split('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace('          ', ' ').replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 14:
                    j = {r16var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r16var))}
                    j.update({
                        r16var[0]: r.solvents_str_no_comma(),
                        r16var[1]: r.salts_str_no_comma(),
                        r16var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report16.items.append(r)
    return report16

def parseReport17(reportPath):
    report17 = aem_report17()
    report17.exists = True
    report17.path = reportPath
    report17.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report17Item()
        r.version = report17.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report17.target_solvent_comp = r.solvents_str_no_comma()
            report17.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report17.target_solvent_comp and r.salts_str_no_comma() == report17.target_salt_comp:
            try:
                table_section = pieces[1].split('-----------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace('            ', ' ').replace('         ', ' ').replace('        ', ' ').replace('       ', ' ').replace('      ', ' ').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
                d = f.strip().split()
                if len(d) == 11:
                    j = {r17var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r17var))}
                    j.update({
                        r17var[0]: r.solvents_str_no_comma(),
                        r17var[1]: r.salts_str_no_comma(),
                        r17var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report17.items.append(r)
    return report17

def parseReport18(reportPath):
    report18 = aem_report18()
    report18.exists = True
    report18.path = reportPath
    report18.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report18Item()
        r.version = report18.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report18.target_solvent_comp = r.solvents_str_no_comma()
            report18.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report18.target_solvent_comp and r.salts_str_no_comma() == report18.target_salt_comp:
            try:
                table_section = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 17:
                    j = {r18var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r18var))}
                    j.update({
                        r18var[0]: r.solvents_str_no_comma(),
                        r18var[1]: r.salts_str_no_comma(),
                        r18var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report18.items.append(r)
    return report18

def parseReport19(reportPath):
    report19 = aem_report19()
    report19.exists = True
    report19.path = reportPath
    report19.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report19Item()
        r.version = report19.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report19.target_solvent_comp = r.solvents_str_no_comma()
            report19.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report19.target_solvent_comp and r.salts_str_no_comma() == report19.target_salt_comp:
            try:
                table_section = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 17:
                    j = {r19var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r19var))}
                    j.update({
                        r19var[0]: r.solvents_str_no_comma(),
                        r19var[1]: r.salts_str_no_comma(),
                        r19var[2]: r.temperature
                    })
                    data.append(j)
            r.data = data
            report19.items.append(r)
    return report19

def parseReport20(reportPath):
    report20 = aem_report20()
    report20.exists = True
    report20.path = reportPath
    report20.version = getReportVersionNumber(open(reportPath).read())
    with open(reportPath) as f:
        text = f.read()
    contents = text.split('alt = ')
    contents.pop(0)
    first_item = None
    for content in contents:
        data = []
        r = report20Item()
        r.version = report20.version
        content = content.replace('==============================================================', '===============================')
        pieces = content.split("===============================")
        parse_composition_temperature(pieces, r)
        if first_item is None:
            first_item = r
            report20.target_solvent_comp = r.solvents_str_no_comma()
            report20.target_salt_comp = r.salts_str_no_comma()
        if r.solvents_str_no_comma() == report20.target_solvent_comp and r.salts_str_no_comma() == report20.target_salt_comp:
            try:
                table_section = pieces[1].split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')[1]
            except IndexError:
                table_section = pieces[1]
            foo = table_section.splitlines()
            for fo in foo:
                f = fo.replace("    ", " ").replace("   ", " ").replace("  ", " ")
                d = f.strip().split()
                if len(d) == 17:
                    j = {r20var[i]: parse_float(d[i-3]) if i > 2 else d[i-3] for i in range(3, len(r20var))}
                    j.update({
                        r20var[0]: r.solvents_str_no_comma(),
                        r20var[1]: r.salts_str_no_comma(),
                        r20var[2]: r.temperature
                    })
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
    if os.path.isdir(dir):
        run = aem_run()
        run.parse_run(dir)
        d = os.path.join(dir, 'csv')
        if not os.path.exists(d):
            try:
                os.mkdir(d)
            except OSError as error:
                print(f'### AEM-PARSER v1.1.0:: Error Occurred creating {d} directory: {error}')
                os._exit(0)
        threads = []
        if run.report01.exists:
            threads.append(threading.Thread(target=write_report_01_csv, args=(run, os.path.join(d, 'Report01.csv'))))
        if run.report02.exists:
            threads.append(threading.Thread(target=write_report_02_csv, args=(run, os.path.join(d, 'Report02.csv'))))
        if run.report03.exists:
            threads.append(threading.Thread(target=write_report_03_csv, args=(run, os.path.join(d, 'Report03.csv'))))
        if run.report04.exists:
            threads.append(threading.Thread(target=write_report_04_csv, args=(run, os.path.join(d, 'Report04.csv'))))
        if run.report05.exists:
            threads.append(threading.Thread(target=write_report_05_csv, args=(run, os.path.join(d, 'Report05.csv'))))
        if run.report06.exists:
            threads.append(threading.Thread(target=write_report_06_csv, args=(run, os.path.join(d, 'Report06.csv'))))
        if run.report10.exists:
            threads.append(threading.Thread(target=write_report_10_csv, args=(run, os.path.join(d, 'Report10.csv'))))
        if run.report11.exists:
            threads.append(threading.Thread(target=write_report_11_csv, args=(run, os.path.join(d, 'Report11.csv'))))
        if run.report12.exists:
            threads.append(threading.Thread(target=write_report_12_csv, args=(run, os.path.join(d, 'Report12.csv'))))
        if run.report13.exists:
            threads.append(threading.Thread(target=write_report_13_csv, args=(run, os.path.join(d, 'Report13.csv'))))
        if run.report14.exists:
            threads.append(threading.Thread(target=write_report_14_csv, args=(run, os.path.join(d, 'Report14.csv'))))
        if run.report15.exists:
            threads.append(threading.Thread(target=write_report_15_csv, args=(run, os.path.join(d, 'Report15.csv'))))
        if run.report16.exists:
            threads.append(threading.Thread(target=write_report_16_csv, args=(run, os.path.join(d, 'Report16.csv'))))
        if run.report17.exists:
            threads.append(threading.Thread(target=write_report_17_csv, args=(run, os.path.join(d, 'Report17.csv'))))
        if run.report18.exists:
            threads.append(threading.Thread(target=write_report_18_csv, args=(run, os.path.join(d, 'Report18.csv'))))
        if run.report19.exists:
            threads.append(threading.Thread(target=write_report_19_csv, args=(run, os.path.join(d, 'Report19.csv'))))
        if run.report20.exists:
            threads.append(threading.Thread(target=write_report_20_csv, args=(run, os.path.join(d, 'Report20.csv'))))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"### AEM-PARSER v1.1.0:: Finished .csv conversion! Elapsed time: {elapsed_time:.2f} seconds")
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
