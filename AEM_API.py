# ============================================================================
"""     Advanced Electrolyte Model (AEM) [v2.24.3] API v1.3.0 (w/ACCC)     """
""" © 2025 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## IMPORT LIBRARIES AND DEPENDENCIES
import errno
import time
import subprocess as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import OrderedDict
import datetime
import json
import uuid
import os
import sys
import shutil
from AEM_PARSER import aem_run, aem_convert_to_csv, aem_convert_to_json

## DELIMITERS AND DEFAULT PRECISION VALUES
delim1 = "|"
delim2 = "_"
default_salt_decimals = 2
default_solvent_precision = 100
vals2str = lambda ls: [str(x) for x in ls]

## API, AEM, & OUTPUT DIRECTORY PATHS
API_HOME_PATH = os.path.dirname(os.path.realpath(__file__))
DLM_EXECUTABLE = "DLM_Executable.exe"

## SOLVENT AND SALT DIRECTORY PATHS
SOLVENT_DB = os.path.join(API_HOME_PATH, "data", "solventDB.csv")
SALT_DB = os.path.join(API_HOME_PATH, "data", "saltDB.csv")
AEM_SOLVENTS = os.path.join(API_HOME_PATH, "data", "AEM_solvents.csv")
AEM_SALTS = os.path.join(API_HOME_PATH, "data", "AEM_salts.csv")
AEM_ACCC_SOLVENTS = os.path.join(API_HOME_PATH, "data", "AEM_ACCC_solvents.csv")
AEM_ACCC_SALTS = os.path.join(API_HOME_PATH, "data", "AEM_ACCC_salts.csv")
    
## ElectrolyteComposition CLASS
class ElectrolyteComposition:
    def __init__(self, 
                 solvents=None, 
                 salts=None, 
                 specified_from=None, 
                 solvent_DB=None, 
                 salt_DB=None, 
                 CompositionID=None,
                 solvent_precision=default_solvent_precision, 
                 salt_decimals=default_salt_decimals):
        self.solvents = dict() if solvents is None else solvents
        self.salts = dict() if salts is None else salts
        self.specified_from = "" if specified_from is None else specified_from
        self.solvent_DB = self.load_solvent_DB() if solvent_DB is None else solvent_DB
        self.salt_DB = self.load_salt_DB() if salt_DB is None else salt_DB
        self.CompositionID = "" if CompositionID is None else CompositionID
        self.solvent_precision = solvent_precision
        self.salt_decimals = salt_decimals
        self.date = datetime.datetime.now().strftime("%m/%d/%Y")

    def dump_info(self):
        filt_solvent_info = self.solvent_DB[self.solvent_DB.name.isin(self.solvents.keys())].to_json(orient="records")
        filt_salt_info = self.salt_DB[self.salt_DB.name.isin(self.salts.keys())].to_json(orient="records")
        return {"solvents": filt_solvent_info, "salts": filt_salt_info}

    def name_composition(self):
        rep = self.CompositionID.replace("_", "")
        return rep.replace("|", "")

    def to_solution_volume(self):
        return  # Placeholder, no changes needed here

    @staticmethod
    def cid_to_parsable(cid):
        rep = cid.replace("_", "")
        return rep.replace("|", "")

    @staticmethod
    def normalize_solvent_dictionary(solvents, solvent_precision):
        total = float(sum(solvents.values()))
        _solvents = {solvent: int(round(solvents[solvent] / total * solvent_precision)) for solvent in solvents.keys()}
        _solvents_nonzero = {solvent: _solvents[solvent] for solvent in _solvents.keys() if _solvents[solvent] != 0}
        ordered_solvents = OrderedDict(sorted(_solvents_nonzero.items(), key=lambda tup: tup[0]))
        return ordered_solvents

    @staticmethod
    def normalize_salt_dictionary(salts, salt_decimal):
        _salts = {salt: round(salts[salt], salt_decimal) for salt in salts.keys()}
        _salts_nonzero = {salt: _salts[salt] for salt in _salts.keys() if _salts[salt] != 0.0}
        ordered_salts = OrderedDict(sorted(_salts_nonzero.items(), key=lambda tup: tup[0]))
        return ordered_salts

    @staticmethod
    def load_solvent_DB(data_path=API_HOME_PATH, filename=SOLVENT_DB):
        path = os.path.join(API_HOME_PATH, filename)
        return pd.read_csv(path)

    @staticmethod
    def load_salt_DB(data_path=API_HOME_PATH, filename=SALT_DB):
        path = os.path.join(API_HOME_PATH, filename)
        return pd.read_csv(path)

    @staticmethod
    def dicts_to_CompositionID(solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        if len(solvents) != 0:
            solvents_normalized = ElectrolyteComposition.normalize_solvent_dictionary(solvents, solvent_precision)
            parts = [solvents_normalized.keys(), vals2str(solvents_normalized.values())]
        else:
            parts = ['', '']
        if len(salts) != 0:
            salts_normalized = ElectrolyteComposition.normalize_salt_dictionary(salts, salt_decimals)
            parts.extend([salts_normalized.keys(), vals2str(salts_normalized.values())])
        else:
            parts.extend['','']
        return delim1.join([delim2.join(x) for x in parts])

    @staticmethod
    def CompositionID_to_dicts(CompositionID):
        ls = CompositionID.split(delim1)
        solvent_names = ls[0].split(delim2)
        solvent_mfs = [i for i in ls[1].split(delim2)]
        assert len(solvent_names) == len(solvent_mfs), "CompositionID is invalid, different lengths for solvent_names vs solvent_mfs"
        assert '0' not in solvent_mfs, "Zeros not allowed in defining composition"
        solvent_mfs_precisions = list(set([len(i) if len(i) > 1 else 2 for i in solvent_mfs]))
        assert len(solvent_mfs_precisions) == 1, f"Length (precision) of solvent mass fractions must be identical: {solvent_mfs_precisions}"
        solvent_precision = int(10 ** int(solvent_mfs_precisions[0]))
        solvent_mfs = [float(i) for i in solvent_mfs]
        solvents = ElectrolyteComposition.normalize_solvent_dictionary({solvent_names[i]: solvent_mfs[i] for i in range(len(solvent_names))}, solvent_precision)
        salt_decimals = default_salt_decimals
        salts = {}
        if len(ls) > 2:  # Salts are present
            assert len(ls) == 4, "If salts are added, must define molality"
            salt_names = ls[2].split(delim2)
            molality = [float(i) for i in ls[3].split(delim2)]
            assert len(salt_names) == len(molality), "CompositionID is invalid, different lengths for salt_names vs molality"
            salts = ElectrolyteComposition.normalize_salt_dictionary({salt_names[i]: molality[i] for i in range(len(salt_names))}, salt_decimals)
        return {"solvents": solvents, "salts": salts, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}

    @classmethod
    def by_CompositionID(cls, CompositionID):
        dicts = cls.CompositionID_to_dicts(CompositionID)
        return cls(**dicts, CompositionID=CompositionID, specified_from=json.dumps({"CompositionID": CompositionID}))

    @classmethod
    def by_mass(cls, solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents_orig = solvents.copy()
        salts_orig = salts.copy()
        total_solvent_mass = sum(solvents.values())
        solvents_normalized = {solvent: (mass / total_solvent_mass) for solvent, mass in solvents.items()}
        solvents_normalized = cls.normalize_solvent_dictionary(solvents_normalized, solvent_precision)
        salts_normalized = {}
        if salts:
            total_solvent_mass_kg = total_solvent_mass / 1000.0  # Convert to kilograms
            salts_normalized = {salt: (mass / total_solvent_mass_kg) for salt, mass in salts.items()}
            salts_normalized = cls.normalize_salt_dictionary(salts_normalized, salt_decimals)
        cid = cls.dicts_to_CompositionID(solvents=solvents_normalized, salts=salts_normalized, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents_normalized, "salts": salts_normalized, "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        return cls(**d, specified_from=json.dumps({"by_mass": {"solvents": solvents_orig, "salts": salts_orig}}))
    @classmethod
    def translate_electrolyte(cls, solvents={}, salts={},solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents = {key.upper(): value for key, value in solvents.items()}
        salts = {key.upper(): value for key, value in salts.items()}
        cid = cls.dicts_to_CompositionID(solvents=solvents, salts=salts, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents.copy(), "salts": salts.copy(), "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        return cls(**d, specified_from=json.dumps({"by_mass_fraction_and_molality": {"solvents": solvents, "salts": salts}}))

    @classmethod
    def by_mass_fraction_and_molality(cls, solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents_orig = solvents.copy()
        salts_orig = salts.copy()
        solvents_normalized = cls.normalize_solvent_dictionary(solvents, solvent_precision)
        
        salts_normalized = {}
        if salts:
            salts_normalized = cls.normalize_salt_dictionary(salts, salt_decimals)
        
        cid = cls.dicts_to_CompositionID(solvents=solvents_orig, salts=salts_orig, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents.copy(), "salts": salts.copy(), "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        return cls(**d, specified_from=json.dumps({"by_mass_fraction_and_molality": {"solvents": solvents_orig, "salts": salts_orig}}))

    @classmethod
    def by_solution_volume(cls, volumes={}, densities={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvent_DB = cls.load_solvent_DB()
        salt_DB = cls.load_salt_DB()
        volumes = {k: int(v) for k, v in volumes.items()}
        densities = {k: float(v) for k, v in densities.items()}
        specified_from = json.dumps({"by_solution_volume": {"volumes": volumes.copy(), "densities": densities.copy()}})
        solvents = {}  # mass fraction
        salts = {}  # molality
        solvents_mass = {}
        salts_moles = {}
        assert set(volumes.keys()) == set(densities.keys()), "Same keys must be in each of volumes and densities"
        total_dose_masses = {solution: volumes[solution] / 1000 * densities[solution] for solution in volumes.keys()}  # in grams
        
        for solution in total_dose_masses.keys():
            solution_comp = cls.CompositionID_to_dicts(solution)
            source_solvent_precision = int(solution_comp["solvent_precision"])
            solution_total_salt_mass = 0
            
            if solution_comp["salts"]:
                for salt in solution_comp["salts"].keys():
                    assert salt in salt_DB.name.values, f"Salt proposed that is not in salt_DB, please check! - {salt}"
                    mm = float(salt_DB[salt_DB.name == salt]["molar mass"].iloc[0])
                    m = solution_comp["salts"][salt]
                    solution_total_salt_mass += mm * m  # g/mol * molality of single salt
                
            solution_salt_mass_fraction = solution_total_salt_mass / (solution_total_salt_mass + 1000)
            solution_solvent_mass_fraction = 1 - solution_salt_mass_fraction
            dose_total_solvent_mass = solution_solvent_mass_fraction * total_dose_masses[solution]
            
            for solvent in solution_comp["solvents"].keys():
                if solvent not in solvents_mass:
                    solvents_mass[solvent] = dose_total_solvent_mass * solution_comp["solvents"][solvent] / source_solvent_precision
                else:
                    solvents_mass[solvent] += dose_total_solvent_mass * solution_comp["solvents"][solvent] / source_solvent_precision
            
            if solution_comp["salts"]:
                for salt in solution_comp["salts"].keys():
                    m = solution_comp["salts"][salt]
                    if salt not in salts_moles:
                        salts_moles[salt] = m * dose_total_solvent_mass / 1000
                    else:
                        salts_moles[salt] += m * dose_total_solvent_mass / 1000
        
        solvents = cls.normalize_solvent_dictionary(solvents_mass, solvent_precision)
        salts = cls.normalize_salt_dictionary({salt: salts_moles[salt] / (sum(list(solvents_mass.values())) / 1000) for salt in salts_moles}, salt_decimals)
        cid = cls.dicts_to_CompositionID(solvents=solvents, salts=salts, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents, "salts": salts, "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        print(f"### AEM-API v1.3.0:: CompositionID: {cid}")
        return cls(**d, specified_from=specified_from)



## AEM_API CLASS
class AEM_API:
    # List of Report Files generated
    report_files = [
        "Report1 -- Summary of Key Properties",
        "Report2 -- Ion association populations and other thermodynamic terms",
        "Report3 -- Ion solvation energies, permittivity and cation desolvation",
        "Report4 -- Diffusivities and selected conductivity terms",
        "Report5 -- Summary of Transport Properties and Walden analysis",
        "Report6 -- Activation Energies",
        "Report7 -- Large-Scale Simulation Optimization",
        "Report8 -- Non-convergent cases",
        "Report9 --  Double-Layer Regions transport analysis",
        "Report10 -- Electrode surface-charge effects",
        "Report11 -- Summary of Ion Solvation Quantities",
        "Report12 -- Preferential Ion Solvation",
        "Report13 -- Conductivity Factors",
        "Report14 -- Li-STEP Terms",
        "Report15 -- Cation transit under Faradaic conditions",
        "Report16 -- Surface Tension and pore filling time over salt conc",
        "Report17 -- Percent pore length filled over time",
        "Report18 -- Ligand-wise cation desolvation energy and time",
        "Report19 -- Ligand-wise cation desolvation energy and time (accounting for CS)",
        "Report20 -- Terms relating to structure and Communal Ion Solvation (CS)"
    ]
    # Constructor to initialize AEM_API with electrolyte composition and read AEM data
    def __init__(self, 
                 electrolyte=None,
                 #accc_electrolyte=None,
                 accc_solvent_class=None,
                 number_of_total_solvents=None,
                 number_of_total_salts=None,
                 number_of_accc_solvents=0,
                 number_of_accc_salts=0,
                 accc_solvent_proportions=None,
                 accc_salt_proportions=None,
                 accc_solvent_class_for_second_salt = None,
                 accc_salt_class=None,
                 accc_salt_class_2=None,
                 salt_csv=AEM_SALTS, 
                 solvent_csv=AEM_SOLVENTS,
                 solventcomp=None,
                 cmfoption=None,
                 cmfsolventindex=None,
                 solventcomppropbasis=None,
                 saltcomp=None,
                 saltconcmode=1,
                 totalsaltconc=None, 
                 tmin=None, 
                 tmax=None, 
                 stepsize=None,
                 tis=None,
                 contactangle=None,
                 porelength=None,
                 saltconc=None,
                 scaep=None,
                 scaep_pulse=None,
                 scaep_cellvoltage=None,
                 scaep_bulksaltconc=None,
                 scaep_thickness=None,
                 scaep_permittivity=None,
                 scaep_porosity=None,
                 dl=None,
                 dl_saltconc=None,
                 dl_currentdensity=None, 
                 dl_temperature=None,
                 output_dir=None,
                 run_name=None,
                 AEMHomePath=None,
                 AEMProgramName=None):
        self.AEMHomePath = AEMHomePath
        DLMout = self.runDLMExecutable()
        if DLMout == '1':
            self.read_AEM_data(salt_csv, solvent_csv)
        if DLMout == '6':
            self.read_AEM_data(salt_csv, solvent_csv)
          
        self.electrolyte = electrolyte
        self.accc_solvent_class = accc_solvent_class
        self.accc_solvent_class_for_second_salt = accc_solvent_class_for_second_salt
        self.number_of_accc_solvents = number_of_accc_solvents
        self.number_of_total_solvents = number_of_total_solvents
        self.number_of_accc_salts = number_of_accc_salts
        self.number_of_total_salts = number_of_total_salts
        self.accc_solvent_proportions = accc_solvent_proportions
        self.accc_salt_proportions = accc_salt_proportions
        self.cues = False
        self.run_yet = False
        self.data_processed = False
        self.aem_exe_filename = AEMProgramName  
        self.report_string = os.path.join(AEMHomePath,"Report1 -- Summary of Key Properties")
        self.dlmout = DLMout
        self.solventcomp = solventcomp
        self.cmfoption = cmfoption
        self.cmfsolventindex = cmfsolventindex
        self.solventcomppropbasis = solventcomppropbasis
        self.saltcomp = saltcomp
        self.saltconcmode = saltconcmode
        self.accc_salt_class = accc_salt_class
        self.accc_salt_class_2 = accc_salt_class_2
        self.totalsaltconc = totalsaltconc
        self.tmin = tmin
        self.tmax = tmax
        self.salt_offset = 0.1  # for ensuring equality in salt molality comparison
        self.stepsize = stepsize  
        self.tis = tis  
        self.contactangle = contactangle
        self.porelength = porelength
        self.saltconc = saltconc
        self.scaep = scaep
        self.scaep_pulse = scaep_pulse
        self.scaep_cellvoltage = scaep_cellvoltage
        self.scaep_bulksaltconc = scaep_bulksaltconc
        self.scaep_thickness = scaep_thickness
        self.scaep_permittivity = scaep_permittivity
        self.scaep_porosity = scaep_porosity
        self.dl = dl
        self.dl_saltconc = dl_saltconc
        self.dl_currdensity = dl_currentdensity
        self.dl_temperature = dl_temperature
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.run_id = str(uuid.uuid4())
        self.run_name = run_name
        self.run_date = datetime.datetime.now().strftime("%Y%m%d")
        self.run_time = datetime.datetime.now().strftime("%H%M%S")

        if self.run_name is None:
            self.run_output_dir = os.path.join(self.output_dir, f"AEMAPIRun_{self.run_id}_{self.run_date}_{self.run_time}")
        else:
            self.run_output_dir = os.path.join(self.output_dir, f"AEMAPIRun_{self.run_name}_{self.run_date}_{self.run_time}")
        os.makedirs(self.run_output_dir, exist_ok=True)
    print(f"### AEM-API v1.3.0:: Starting Program!")
    
    # Method to read AEM data from CSV files
    def read_AEM_data(self, salt_csv, solvent_csv):
        saltDF = pd.read_csv(salt_csv)
        solventDF = pd.read_csv(solvent_csv)
        salts = saltDF.set_index('string').T.to_dict('list')
        salts = {k.strip(): [v[0], v[1].strip()] for k, v in salts.items()}
        solvents = solventDF.set_index('string').T.to_dict('list')
        solvents = {k.strip(): [v[0], v[1].strip()] for k, v in solvents.items()}
        self.AEM_solvents = solvents
        self.AEM_salts = salts

    # Method to read AEM data from CSV files
    def read_AEM_ACCC_data(self, electrolyte):
        self.AEM_ACCC_solvents = electrolyte.solvents
        self.AEM_ACCC_salts = electrolyte.salts

    # Method to match ACCC Component Identifiers in Filenames
    def matchACCCComp(self):
        match_found = False  # Flag to track if a match is found
        for salt in self.AEM_ACCC_salts:
            # Extract solvent part from the salt name
            solvent_part = '_'.join(salt.split('_')[2:])
            # Check if solvent_part matches any of the keys in the solvents dictionary
            solvents = '_'.join(self.AEM_ACCC_solvents.keys())
            if solvent_part == solvents:
                match_found = True
                break  # Break out of the inner loop if a match is found
            # Raise an error if no match was found for this salt
            if not match_found:
                raise ValueError(f"Salt {salt} does not match any solvent in {list(self.AEM_ACCC_solvents.keys())}.")
        return None

    # Method to run the AEM model
    def runDLMExecutable(self):
        print(f"### AEM-API v1.3.0:: Checking ACCC Access from DLM ...")
        fp = os.path.join(API_HOME_PATH, DLM_EXECUTABLE)
        # Run the executable with the 'check' argument
        p = sp.Popen([fp, 'check'], shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, cwd=self.AEMHomePath)
        # Capture the output
        stdout, _ = p.communicate()  # Capture output
        stdout = stdout.decode('utf-8').strip()  # Decode and strip any extra whitespace/newlines
        # Log the output and return it
        if stdout == '1':
            print(f"### AEM-API v1.3.0:: ACCC Access Invalid!")
        elif stdout == '6':
            print(f"### AEM-API v1.3.0:: ACCC Access Valid")
        else:
            print(f"### AEM-API v1.3.0:: Unknown output: {stdout}")
        print(f"### AEM-API v1.3.0:: ACCC Access Check Complete!")
        return stdout
    def accc_generate_solvent_cues(self):
        number_of_solvents = len(self.electrolyte.solvents)
        if self.solventcomp == 1: #Fixed Composition Mode
            self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
            self.cues.append(self.solventcomppropbasis)
            assert self.number_of_total_solvents == (number_of_solvents + self.number_of_accc_solvents), "Solvent count mismatch"
            assert (number_of_solvents + self.number_of_accc_solvents) <= 10, "Number of solvents must be no greater than 10"
            self.params["Number of Solvents"] = self.number_of_total_solvents
            self.cues.append(self.number_of_total_solvents)
            self.params["Number of ACCC Solvents"] = self.number_of_accc_solvents
            self.cues.append(self.number_of_accc_solvents)
            if (self.number_of_accc_solvents != 0):
                self.params["How many salts will be used in this electrolyte having ACCC solvents?"] = self.number_of_total_salts
                self.cues.append(self.number_of_total_salts)
                self.params['Input suffix (1st Solvent Class)'] = self.accc_solvent_class
                self.cues.append(self.accc_solvent_class)
                if (self.number_of_total_salts == 2):
                    self.params['Input suffix (1st Solvent Class)'] = self.accc_solvent_class_for_second_salt
                    self.cues.append(self.accc_solvent_class_for_second_salt)
            i = 0
            for solvent in self.electrolyte.solvents.keys():
                i=i+1
                self.params[f'Solvent {i} ID'] = solvent
                self.cues.append(self.AEM_solvents[solvent][0])  # append cues
            if self.number_of_total_solvents > 1:
                i=0
                for solvent in self.electrolyte.solvents:
                    i=i+1
                    self.params[f'Solvent {i} Proportion'] = self.electrolyte.solvents[solvent]
                    self.cues.append(self.electrolyte.solvents[solvent])
                for proportion in self.accc_solvent_proportions:
                    self.params[f'Solvent {i} Proportion (ACCC)'] = proportion
                    self.cues.append(proportion)  
        elif self.solventcomp == 2:
            assert self.number_of_total_solvents <= 5, "Number of solvents must be no greater than 5"
            assert self.number_of_total_solvents >= 2, "Number of solvents must be at least 2" 
            assert self.number_of_total_solvents == (number_of_solvents + self.number_of_accc_solvents), "Solvent count mismatch"
            self.params["Number of Solvents"] = self.number_of_total_solvents
            self.cues.append(self.number_of_total_solvents)
            if self.number_of_total_solvents > 2:
                self.params["Use constant mass fraction"] = self.cmfoption 
                self.cues.append(self.cmfoption)
                solvent_list = list(self.electrolyte.solvents.keys())
            self.params["Number of ACCC Solvents"] = self.number_of_accc_solvents
            self.cues.append(self.number_of_accc_solvents)
            if (self.number_of_accc_solvents != 0):
                self.params["How many salts will be used in this electrolyte having ACCC solvents?"] = self.number_of_total_salts
                self.cues.append(self.number_of_total_salts)
                self.params['Input suffix (1st Solvent Class)'] = self.accc_solvent_class
                self.cues.append(self.accc_solvent_class)
                if (self.number_of_total_salts == 2):
                    self.params['Input suffix (1st Solvent Class)'] = self.accc_solvent_class_for_second_salt
                    self.cues.append(self.accc_solvent_class_for_second_salt)
            if self.cmfsolventindex is None:
                if self.cmfoption == 1:  # CMF is enabled but no index provided
                    raise ValueError("cmfsolventindex must be provided when cmfoption is 1. Got None.")
                self.cmfsolventindex = 0  # Default to 0 if CMF is not enabled
                if not (0 <= self.cmfsolventindex < len(solvent_list)):
                    raise ValueError(f"cmfsolventindex must be between 0 and {len(solvent_list) - 1}. Got {self.cmfsolventindex}.")
            cmf_applied = False
            i = 0
            for index, solvent in enumerate(self.electrolyte.solvents.keys()):
                self.params[f'Solvent {i} ID'] = solvent
                self.cues.append(self.AEM_solvents[solvent][0])  # Append solvent cue
                i=i+1
                if (self.cmfoption == 1) & (cmf_applied == False) & (self.number_of_total_solvents > 2):
                    if (index == self.cmfsolventindex):
                        self.params[f'Solvent {i} CMF?'] = 1
                        self.cues.append(1)
                        print("self.electrolyte.solvents", self.electrolyte.solvents)
                        self.params[f'Indicate constant mass fraction'] = self.electrolyte.solvents[solvent]
                        self.cues.append(self.electrolyte.solvents[solvent])
                        cmf_applied = True
                    else:
                        self.params[f'Solvent {i} CMF?'] = 0
                        self.cues.append(0)
               
    def aem_generate_solvent_cues(self):
        number_of_solvents = len(self.electrolyte.solvents)
        if self.solventcomp == 1: #Fixed Composition Mode
            self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
            self.cues.append(self.solventcomppropbasis)
            assert number_of_solvents <= 10, "Number of solvents must be no greater than 10"
            self.params["Number of Solvents"] = number_of_solvents
            self.cues.append(number_of_solvents)
            i = 0
            for solvent in self.electrolyte.solvents.keys():
                i=i+1
                self.params[f'Solvent {i} ID'] = solvent
                self.cues.append(self.AEM_solvents[solvent][0])  # append cues
            if len(self.electrolyte.solvents.keys()) > 1:
                i=0
                for solvent in self.electrolyte.solvents:
                    i=i+1
                    self.params[f'Solvent {i} Proportion'] = self.electrolyte.solvents[solvent]
                    self.cues.append(self.electrolyte.solvents[solvent])
        elif self.solventcomp == 2: #Matrix Composition Mode
            assert number_of_solvents <= 5, "Number of solvents must be no greater than 5"
            assert number_of_solvents >= 2, "Number of solvents must be at least 2"
            if number_of_solvents > 2:
               self.params["Use constant mass fraction"] = self.cmfoption 
               self.cues.append(self.cmfoption)
               solvent_list = list(self.electrolyte.solvents.keys())
            if self.cmfsolventindex is None:
                if self.cmfoption == 1:  # CMF is enabled but no index provided
                    raise ValueError("cmfsolventindex must be provided when cmfoption is 1. Got None.")
                self.cmfsolventindex = 0  # Default to 0 if CMF is not enabled
            if not (0 <= self.cmfsolventindex < len(solvent_list)):
                raise ValueError(f"cmfsolventindex must be between 0 and {len(solvent_list) - 1}. Got {self.cmfsolventindex}.")
            cmf_applied = False
            for index, solvent in enumerate(self.electrolyte.solvents.keys()):
                self.cues.append(self.AEM_solvents[solvent][0])  # Append solvent cue
                if self.cmfoption == 1 and not cmf_applied:
                    if index == self.cmfsolventindex:
                        is_last_solvent = (self.cmfsolventindex == len(solvent_list) - 1)
                        self.cues.append(0 if not is_last_solvent else 1)  # CMF indicator (0 for First, 1 for Last)
                        self.cues.append(self.electrolyte.solvents[solvent])  # Append mass fraction for CMF solvent
                        self.params["Constant Mass Fraction Solvent"] = self.electrolyte.solvents[solvent]
                        cmf_applied = True  # Stop further CMF indicators
                    else:
                        self.cues.append(0)  # CMF indicator (0 for non-CMF solvents before CMF solvent)
            
    def accc_generate_salt_cues(self):        
        assert self.number_of_total_salts <= 2, "Number of salts must be no greater than 2"
        self.params["Number of Salts"] = self.number_of_total_salts
        self.cues.append(self.number_of_total_salts)
        if self.number_of_accc_salts is None:
            self.number_of_accc_salts = 0
        self.params["Number of ACCC Salts"] = self.number_of_accc_salts
        self.cues.append(self.number_of_accc_salts)
        if self.number_of_accc_salts != 0:
            self.cues.append(self.accc_salt_class)
            self.params["ACCC Salt Class 1"] = self.accc_salt_class
            if self.number_of_accc_salts == 2:
                self.cues.append(self.accc_salt_class_2)
                self.params["ACCC Salt Class 2"] = self.accc_salt_class_2
        i=0
        for salt in self.electrolyte.salts.keys():
            i=i+1
            self.params[f'Salt {i} ID'] = salt
            self.cues.append(self.AEM_salts[salt][0])  # append self.cues
        if self.number_of_total_salts > 1:
            self.cues.append(self.saltcomp)  # specify single fixed salt prop
            self.params["Salt Composition Proportion Mode"] = self.saltcomp
            if self.saltcomp == 1:
                i=0
                for salt in self.electrolyte.salts:
                    i=i+1
                    self.params[f'Salt {i} Proportion'] = self.electrolyte.salts[salt]
                    self.cues.append(self.electrolyte.salts[salt])
                for proportion in self.accc_salt_proportions:
                    i=i+1
                    self.params[f'Salt {i} Proportion (ACCC)'] = proportion
                    self.cues.append(proportion)
        self.params["Salt concentration mode"] = self.saltconcmode    
        self.cues.append(self.saltconcmode)  # append self.cues 
        if self.saltconcmode == 1:
            self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
            self.cues.append(self.totalsaltconc)

    def aem_generate_salt_cues(self): #generate basic salt cues (non-accc)   
        number_of_salts = len(self.electrolyte.salts)
        assert number_of_salts <= 2, "Number of salts must be no greater than 2"
        self.cues.append(number_of_salts)
        self.params["Number of Salts"] = number_of_salts
        i=0
        for salt in self.electrolyte.salts.keys():
            i=i+1
            self.params[f'Salt {i} ID'] = salt
            self.cues.append(self.AEM_salts[salt][0])  # append self.cues
        if number_of_salts > 1:
            self.cues.append(self.saltcomp)  # specify single fixed salt prop
            self.params["Salt Composition Proportion Mode"] = self.saltcomp
            if self.saltcomp == 1:
                i=0
                for salt in self.electrolyte.salts:
                    i=i+1
                    self.params[f'Salt {i} Proportion'] = self.electrolyte.salts[salt]
                    self.cues.append(self.electrolyte.salts[salt])
        self.params["Salt concentration mode"] = self.saltconcmode    
        self.cues.append(self.saltconcmode)  # append self.cues 
        if self.saltconcmode == 1:
            self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
            self.cues.append(self.totalsaltconc)

    def aem_generate_other_cues(self):
        #Temperature
        self.params["Minimum Temperature"] = self.tmin
        self.cues.append(self.tmin)
        self.params["Maximum Temperature"] = self.tmax
        self.cues.append(self.tmax)
        self.params["Temperature Step Size"] = self.stepsize
        self.cues.append(self.stepsize)
        #ion stability
        self.params["Method for Triple-Ion Stability"] = self.tis
        self.cues.append(self.tis)
        #Electrolyte ingress into pores
        self.params["Contact Angle"] = self.contactangle
        self.cues.append(self.contactangle)
        self.params["Pore Length"] = self.porelength        
        self.cues.append(self.porelength)
        self.params["Salt Concentration of Interest"] = self.saltconc        
        self.cues.append(self.saltconc)
        if self.solventcomp == 1:
            self.params["Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations"] = self.scaep
            self.cues.append(self.scaep)
            if self.scaep == 1:
                self.params["Type of pulse condition"] = self.scaep_pulse #1 (Discharge) 2 (Charge)
                self.cues.append(self.scaep_pulse)
                self.params["Cell voltage of interest"] = self.scaep_cellvoltage 
                self.cues.append(self.scaep_cellvoltage)
                self.params["Bulk salt concentration"] = self.scaep_bulksaltconc 
                self.cues.append(self.scaep_bulksaltconc)
                self.params["Thickness of SEI cathode/anode"] = self.scaep_thickness 
                self.cues.append(self.scaep_thickness)
                self.params["Relative permittivity of SEI cathode/anode"] = self.scaep_permittivity 
                self.cues.append(self.scaep_permittivity)
                self.params["Porosity of SEI cathode/anode"] = self.scaep_porosity 
                self.cues.append(self.scaep_porosity)
            self.params["Double Layer (DL) Calculations"] = self.dl
            self.cues.append(self.dl)
            if self.dl == 1:
                self.params["Pre-pulse salt concentration"] = self.dl_saltconc 
                self.cues.append(self.dl_saltconc)
                self.params["Current density"] = self.dl_currdensity 
                self.cues.append(self.dl_currdensity)
                self.params["Temperature of interest for DL calculations "] = self.dl_temperature 
                self.cues.append(self.dl_temperature)
            

                
    def clean_Nones(self):
        if (self.accc_solvent_proportions is None): self.accc_solvent_proportions = []                      
        if (self.accc_salt_proportions is None): self.accc_salt_proportions = []                      
        if (self.number_of_accc_solvents is None): self.number_of_accc_solvents = 0   
        if (self.number_of_accc_salts is None): self.number_of_accc_salts = 0 
        if (self.saltcomp is None): self.saltcomp = 1
        if (self.solventcomp is None): self.solventcomp = 1 
        if (self.scaep is None): self.scaep = 0
        if (self.dl is None): self.dl = 0              
        if (self.saltconcmode is None): self.saltconcmode = 1
        if (self.tis is None): self.tis = 1

                
    def aem_generate_cues(self): #generate basic cues (non-accc)
        self.clean_Nones()
        self.cues = []
        self.params = {}
        self.params["Solvent Composition"] = self.solventcomp
        self.cues.append(self.solventcomp)
        self.aem_generate_solvent_cues()
        self.aem_generate_salt_cues()
        self.aem_generate_other_cues()
        self.cues.append(0)

    def aem_generate_accc_cues(self):
        self.clean_Nones()
        self.cues = []
        self.params = {}
        self.params["Solvent Composition"] = self.solventcomp
        self.cues.append(self.solventcomp)
        self.accc_generate_solvent_cues()       
        self.accc_generate_salt_cues()       
        self.aem_generate_other_cues()
        self.cues.append(0)
    # Method to generate input cues for the AEM model
    def generate_cues(self):
        if self.dlmout == '1':
            self.aem_generate_cues()
        elif self.dlmout == '6':
            self.aem_generate_accc_cues()

    # Method to run the AEM model
    def runAEM(self, quiet=True):
        print(f"### AEM-API v1.3.0:: Starting Run {self.run_id}...")
        if not self.cues:
            raise ValueError("cues not populated, run generate_cues first")
        # generate input byte string
        inp = [str(cue) for cue in self.cues]
        print(f"### AEM-API v1.3.0:: Cues: {inp}...")
        inpb = bytes('\n'.join(inp) + '\n\n', encoding="ascii")
        # Start timing
        start_time = time.time()
        # Launch AEM and pass input byte string
        if quiet:
            out = sp.DEVNULL
        else:
            out = sys.stdout
        fp = os.path.join(self.AEMHomePath, self.aem_exe_filename)
        p = sp.Popen(fp, stdin=sp.PIPE, stdout=out, stderr=sp.STDOUT, cwd=self.AEMHomePath)
        p.communicate(inpb)
        #End timing and print completion with runtime
        end_time = time.time()
        runtime = (end_time - start_time)
        hours = int(runtime // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = int(runtime % 60)
        milliseconds = int((runtime % 1) * 1000)  # Convert fractional seconds to milliseconds
        # Format runtime to HH:MM:SS.mmm
        runtime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
        print(f"### AEM-API v1.3.0:: Run {self.run_id} Complete! (Runtime: {runtime_str})")
        self.copy_report_files()
        self.save_run_log()
        self.run_yet = True
    
    # Function to log run summary
    def save_run_log(self):
        if self.run_name is None:
            log_data = {
                "run_id": self.run_id,
                "run_date": self.run_date,
                "run_time": self.run_time,
                "electrolyte_composition": self.electrolyte.CompositionID if self.electrolyte is not None else None,
                "ACCC_electrolyte_composition": self.accc_electrolyte.CompositionID if self.accc_electrolyte is not None else None,
                "input_params": self.params
            }
            log_file = os.path.join(self.run_output_dir, f"AEMRun-{self.run_id}-{self.run_date}-{self.run_time}-Log.json")
            print(f"### AEM-API v1.3.0:: Run {self.run_id}: Log saved to {log_file}")
        else:
            log_data = {
                "run_name": self.run_name,
                "run_id": self.run_id,
                "run_date": self.run_date,
                "run_time": self.run_time,
                "electrolyte_composition": self.electrolyte.CompositionID if self.electrolyte is not None else None,
                #"ACCC_electrolyte_composition": self.accc_electrolyte.CompositionID if self.accc_electrolyte is not None else None,
                "input_params": self.params
            }
            log_file = os.path.join(self.run_output_dir, f"AEMRun-{self.run_name}-{self.run_date}-{self.run_time}-Log.json")
            print(f"### AEM-API v1.3.0:: Run {self.run_name}: Log saved to {log_file}")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=4)
        return None
    
    # Function to copy report files to run_output_dir
    def copy_report_files(self):
        dstfolder = os.path.join(self.run_output_dir, "Reports")
        try:
            os.makedirs(dstfolder, exist_ok=True)
            print(f"### AEM-API v1.3.0:: Run {self.run_id}: Destination folder created at {dstfolder}")
        except OSError as e:
            print(f"### AEM-API v1.3.0:: Run {self.run_id}: Failed to create destination folder {dstfolder}: {e}")
            return
        for report_file in self.report_files:
            src = os.path.join(self.AEMHomePath, report_file)
            dst = os.path.join(dstfolder, report_file)  # Removed f-string, as it’s unnecessary
            print(f"### AEM-API v1.3.0:: Run {self.run_id}: Copying from {src} to {dst}")
            if os.path.exists(src):
                try:
                    shutil.copy(src, dst)
                    print(f"### AEM-API v1.3.0:: Run {self.run_id}: Successfully copied {report_file}")
                except OSError as e:
                    print(f"### AEM-API v1.3.0:: Run {self.run_id}: Failed to copy {report_file}: {e}")
                    if e.errno == errno.ENAMETOOLONG:
                        print(f"### AEM-API v1.3.0:: Run {self.run_id}: Path too long. Consider enabling long path support on Windows.")
                    elif e.errno == errno.EACCES:
                        print(f"### AEM-API v1.3.0:: Run {self.run_id}: Permission denied. Check write access to {dstfolder}")
            else:
                print(f"### AEM-API v1.3.0:: Run {self.run_id}: Report file {report_file} not found at {src}")
        print(f"### AEM-API v1.3.0:: Run {self.run_id}: Copied generated Report files to {dstfolder}")
        print(f"### AEM-API v1.3.0:: Run {self.run_id}: Running AEM-PARSER on Report files and converting to .csv and .json...")
        aem_convert_to_csv(dstfolder)
        print(f"### AEM-API v1.3.0:: Run {self.run_id}: AEM-PARSER converted Report files to .csv and saved to {dstfolder}\\csv")
        aem_convert_to_json(dstfolder)
        print(f"### AEM-API v1.3.0:: Run {self.run_id}: AEM-PARSER converted Report files to .json and saved to {dstfolder}\\json")

    # Function to preview data from parsed report files
    def plot_parsed_data(self, x, y, report_number):
        plot_dir = os.path.join(self.run_output_dir, "Plots")
        plot_path = os.path.join(plot_dir, f"AEMOutput-{report_number}-{y}_vs_{x}.png")
        os.makedirs(plot_dir, exist_ok=True)
        output_dir = os.path.join(self.run_output_dir,"Reports")
        if self.run_name is None:
            print(f"### AEM-API v1.3.0:: Plotting {y} v/s {x} from {report_number} for Run {self.run_id}...")
        else:
            print(f"### AEM-API v1.3.0:: Plotting {y} v/s {x} from {report_number} for Run {self.run_name}...")
        run = aem_run()
        run.parse_run(output_dir)
        fig, ax = plt.subplots(figsize=(20, 6))
        report = getattr(run, report_number.lower())  # Access report dynamically based on input
        for s in report.items:
            x_plot = [d[x] for d in s.data]
            y_plot = [d[y] for d in s.data]
            # Generate label with information about solvents, salts, and temperature
            label = (f"Solvent(s): {s.solvents_str_no_comma()}\n"
                     f"Salt(s): {s.salts_str_no_comma()}\n"
                     f"Temperature: {s.temperature_str()}")
            # Plot with scientific formatting
            ax.plot(x_plot, y_plot, label=label)
        # Setting titles and labels
        ax.set_title(f"{y} v/s {x}", fontsize=18, weight='bold')
        ax.set_xlabel(f"{x}", fontsize=12, fontstyle="italic")
        ax.set_ylabel(f"{y}", fontsize=12, fontstyle="italic")
        # Add grid, legend, and scientific format for tick labels
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend(fontsize=10, loc="upper left", bbox_to_anchor=(1, 1))
        # Set scientific notation for axes if needed
        ax.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
        plt.tight_layout()
        plt.savefig(plot_path, bbox_inches='tight')
        plt.show()
        plt.close()
        if self.run_name is None:
            print(f"### AEM-API v1.3.0:: {y} v/s {x} from {report_number} for Run {self.run_id} saved as a data plot to '{plot_path}'")
        else:
            print(f"### AEM-API v1.3.0:: {y} v/s {x} from {report_number} for Run {self.run_name} saved as a data plot to '{plot_path}'")
        print(f"### AEM-API v1.3.0:: End of Program! (© 2024 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved)")

