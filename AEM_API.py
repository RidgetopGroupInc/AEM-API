# ============================================================================
"""      Advanced Electrolyte Model (AEM) [v2.1.0] API v1.1.0 (w/ACCC)     """
""" © 2024 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## IMPORT LIBRARIES AND DEPENDENCIES
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
    # Constructor to initialize Electrolyte Composition
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
        self.specified_from = "" if specified_from is None else specified_from  # Info from class method used to create
        self.solvent_DB = self.load_solvent_DB() if solvent_DB is None else solvent_DB
        self.salt_DB = self.load_salt_DB() if salt_DB is None else salt_DB
        self.CompositionID = "" if CompositionID is None else CompositionID
        self.solvent_precision = solvent_precision
        self.salt_decimals = salt_decimals
        self.date = datetime.datetime.now().strftime("%m/%d/%Y")  # Get date of composition creation
        if len(salts) > 1:
            raise NotImplementedError("Binary salts not implemented yet - Ady")
    # Function to dump information about Solvents and Salts
    def dump_info(self):
        filt_solvent_info = self.solvent_DB[self.solvent_DB.name.isin(self.solvents.keys())].to_json(orient="records")
        filt_salt_info = self.salt_DB[self.salt_DB.name.isin(self.salts.keys())].to_json(orient="records")
        return {"solvents": filt_solvent_info, "salts": filt_salt_info}
    # Function to generate a Composition Name
    def name_composition(self):
        rep = self.CompositionID.replace("_", "")
        return rep.replace("|", "")
    # Placeholder function for solution volume conversion (TBD)
    def to_solution_volume(self):
        return
    # Static Method Function to convert CompositionID into a parsable format
    @staticmethod
    def cid_to_parsable(cid):
        rep = cid.replace("_", "")
        return rep.replace("|", "")
    # Static Method Function to normalize the Solvent dictionary
    @staticmethod
    def normalize_solvent_dictionary(solvents, solvent_precision):
        total = float(sum(solvents.values()))
        _solvents = {solvent: int(round(solvents[solvent] / total * solvent_precision)) for solvent in solvents.keys()}
        _solvents_nonzero = {solvent: _solvents[solvent] for solvent in _solvents.keys() if _solvents[solvent] != 0}
        ordered_solvents = OrderedDict(sorted(_solvents_nonzero.items(), key=lambda tup: tup[0]))
        return ordered_solvents
    # Static Method Function to normalize the Salt dictionary
    @staticmethod
    def normalize_salt_dictionary(salts, salt_decimal):
        _salts = {salt: round(salts[salt], salt_decimal) for salt in salts.keys()}
        _salts_nonzero = {salt: _salts[salt] for salt in _salts.keys() if _salts[salt] != 0.0}
        ordered_salts = OrderedDict(sorted(_salts.items(), key=lambda tup: tup[0]))
        return ordered_salts
    # Static Method Function to load the Solvent Database
    @staticmethod
    def load_solvent_DB(data_path=API_HOME_PATH, filename=SOLVENT_DB):
        path = os.path.join(API_HOME_PATH, filename)
        return pd.read_csv(path)
    # Static Method Function to load the Salt Database
    @staticmethod
    def load_salt_DB(data_path=API_HOME_PATH, filename=SALT_DB):
        path = os.path.join(API_HOME_PATH, filename)
        return pd.read_csv(path)
    # Static Method Function to create a CompositionID from dictionaries
    @staticmethod
    def dicts_to_CompositionID(solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents_normalized = ElectrolyteComposition.normalize_solvent_dictionary(solvents, solvent_precision)
        if len(salts) != 0:
            salts_normalized = ElectrolyteComposition.normalize_salt_dictionary(salts, salt_decimals)
            return delim1.join([delim2.join(x) for x in [solvents_normalized.keys(), vals2str(solvents_normalized.values()), salts_normalized.keys(), vals2str(salts_normalized.values())]])
        else:
            return delim1.join([delim2.join(x) for x in [solvents_normalized.keys(), vals2str(solvents_normalized.values())]])
    # Static Method Function to convert CompositionID to dictionaries
    @staticmethod
    def CompositionID_to_dicts(CompositionID):
        ls = CompositionID.split(delim1)
        solvent_names = ls[0].split(delim2)
        solvent_mfs = [i for i in ls[1].split(delim2)]
        assert len(solvent_names) == len(solvent_mfs), "CompositionID is invalid, different lengths for solvent_names vs solvent_mfs"
        assert 0 not in solvent_mfs, "Zeros not allowed in defining composition"
        solvent_mfs_precisions = list(set([len(i) if len(i) > 1 else 2 for i in solvent_mfs]))
        assert len(solvent_mfs_precisions) == 1, "Length (precision) of solvent mass fractions must be identical: {}".format(solvent_mfs_precisions)
        solvent_precision = int(10 ** int(solvent_mfs_precisions[0]))
        solvent_mfs = [float(i) for i in solvent_mfs]
        solvents = ElectrolyteComposition.normalize_solvent_dictionary({solvent_names[i]: solvent_mfs[i] for i in range(len(solvent_names))}, solvent_precision)
        salt_decimals = default_salt_decimals
        if len(ls) > 2:
            assert len(ls) == 4, "If salts are added, must define molality"
            salt_names = ls[2].split(delim2)
            molality = [float(i) for i in ls[3].split(delim2)]
            assert len(salt_names) == len(molality), "CompositionID is invalid, different lengths for salt_names vs molality"
            salts = ElectrolyteComposition.normalize_salt_dictionary({salt_names[i]: molality[i] for i in range(len(salt_names))}, salt_decimals)
        else:
            salts = {}
        return {"solvents": solvents, "salts": salts, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
    # Class Method Functions to create an instance from a CompositionID
    @classmethod
    def by_CompositionID(cls, CompositionID):
        dicts = cls.CompositionID_to_dicts(CompositionID)
        return cls(**dicts, CompositionID=CompositionID, specified_from=json.dumps({"CompositionID": CompositionID}))
    # Class Method Function to create an instance by Mass (To be verified with Ady or other AEM Staff)
    @classmethod
    def by_mass(cls, solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents_orig = solvents.copy()
        salts_orig = salts.copy()
        total_solvent_mass = sum(solvents.values())
        solvents_normalized = {solvent: (mass / total_solvent_mass) for solvent, mass in solvents.items()}
        solvents_normalized = cls.normalize_solvent_dictionary(solvents_normalized, solvent_precision)
        if len(salts) != 0:
            total_solvent_mass_kg = total_solvent_mass / 1000.0  # Convert to kilograms
            salts_normalized = {salt: (mass / total_solvent_mass_kg) for salt, mass in salts.items()}
            salts_normalized = cls.normalize_salt_dictionary(salts_normalized, salt_decimals)
        else:
            salts_normalized = salts
        cid = cls.dicts_to_CompositionID(solvents=solvents_normalized, salts=salts_normalized, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents_normalized, "salts": salts_normalized, "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        return cls(**d, specified_from=json.dumps({"by_mass": {"solvents": solvents_orig, "salts": salts_orig}}))
    # Class Method Function to create an instance by Mass Fraction and Molality
    @classmethod
    def by_mass_fraction_and_molality(cls, solvents={}, salts={}, solvent_precision=default_solvent_precision, salt_decimals=default_salt_decimals):
        solvents_orig = solvents.copy()
        salts_orig = salts.copy()
        solvents_normalized = cls.normalize_solvent_dictionary(solvents, solvent_precision)
        if len(salts) != 0:
            salts_normalized = cls.normalize_salt_dictionary(salts, salt_decimals)
        else:
            salts_normalized = salts
        cid = cls.dicts_to_CompositionID(solvents=solvents_normalized, salts=salts_normalized, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents_normalized, "salts": salts_normalized, "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        return cls(**d, specified_from=json.dumps({"by_mass_fraction_and_molality": {"solvents": solvents_orig, "salts": salts_orig}}))
    # Class Method Function to create an instance by Solution Volume
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
        total_dose_masses = {solution: volumes[solution] / 1000 * densities[solution] for solution in volumes.keys()}  # this is in grams
        for solution in total_dose_masses.keys():
            solution_comp = cls.CompositionID_to_dicts(solution)  # solution_comp["solvents"] is m.f.; '' ["salts"] is molal
            source_solvent_precision = int(solution_comp["solvent_precision"])
            # BOTTLE LEVEL
            solution_total_salt_mass = 0
            if len(solution_comp["salts"]) != 0:
                for salt in solution_comp["salts"].keys():
                    assert salt in salt_DB.name.values, "Salt proposed that is not in salt_DB, please check! - {}".format(salt)
                    mm = float(salt_DB[salt_DB.name == salt]["molar mass"].iloc[0])
                    m = solution_comp["salts"][salt]
                    solution_total_salt_mass += mm * m  # g/mol * molality of single salt = mass of this salt in bottle
            solution_salt_mass_fraction = solution_total_salt_mass / (solution_total_salt_mass + 1000)
            solution_solvent_mass_fraction = 1 - solution_salt_mass_fraction
            # DOSE LEVEL
            dose_total_solvent_mass = solution_solvent_mass_fraction * total_dose_masses[solution]
            for solvent in solution_comp["solvents"].keys():
                if solvent not in solvents_mass:
                    solvents_mass[solvent] = dose_total_solvent_mass * solution_comp["solvents"][solvent] / source_solvent_precision
                else:
                    solvents_mass[solvent] += dose_total_solvent_mass * solution_comp["solvents"][solvent] / source_solvent_precision
            if len(solution_comp["salts"]) != 0:
                for salt in solution_comp["salts"].keys():
                    m = solution_comp["salts"][salt]
                    if salt not in salts_moles:
                        salts_moles[salt] = m * dose_total_solvent_mass / 1000
                    else:
                        salts_moles[salt] += m * dose_total_solvent_mass / 1000
        # EVERYTHING HAS BEEN TOTALED
        solvents = cls.normalize_solvent_dictionary(solvents_mass, solvent_precision)
        salts = cls.normalize_salt_dictionary({salt: salts_moles[salt] / (sum(list(solvents_mass.values()))) * 1000 for salt in salts_moles}, salt_decimals)
        cid = cls.dicts_to_CompositionID(solvents=solvents, salts=salts, solvent_precision=solvent_precision, salt_decimals=salt_decimals)
        d = {"solvents": solvents, "salts": salts, "CompositionID": cid, "solvent_precision": solvent_precision, "salt_decimals": salt_decimals}
        print(f"### AEM-API v1.1.0:: CompositionID: {cid}")
        return cls(**d, specified_from=specified_from)

## ACCCElectrolyteComposition CLASS
class ACCCElectrolyteComposition:
    def __init__(self, solvents=None, salts=None, solvent_file=None, salt_file=None):
        self.solvents = solvents if solvents else {}
        self.salts = salts if salts else {}
        self.solvent_file = self.load_solvent_file() if solvent_file is None else solvent_file
        self.salt_file = self.load_salt_file() if salt_file is None else salt_file
        self.validate_components()
        self.composition_info = self.get_composition_info()
        self.CompositionID = self.format_accc_composition()

    def validate_components(self):
        self.solvents = self.filter_components(self.solvents, self.solvent_file, "solvent")
        self.salts = self.filter_components(self.salts, self.salt_file, "salt")

    def get_composition_info(self):
        filt_solvent_info = {}
        for solvent, composition in self.solvents.items():
            if isinstance(composition, dict):
                for subsolvent, percentage in composition.items():
                    if subsolvent in self.solvent_file['name'].values:
                        filt_solvent_info[subsolvent] = percentage
            elif solvent in self.solvent_file['name'].values:
                filt_solvent_info[solvent] = composition
        filt_salt_info = {k: v for k, v in self.salts.items() if k in self.salt_file['name'].values}
        return {"solvents": filt_solvent_info, "salts": filt_salt_info}

    def format_accc_composition(self):
        solvents_part = []
        for solvent, composition in self.solvents.items():
            if isinstance(composition, dict):  # Multiple components
                composition_str = '_'.join(str(composition[comp]) for comp in composition)
            else:  # Single component
                composition_str = str(composition)
            solvents_part.append(f"{solvent}|{composition_str}")
        
        solvents_part = '|'.join(solvents_part)
        salts_part = '|'.join([
            f"{salt}|{self.salts[salt]}" for salt in self.salts
        ])
        # Combine solvents and salts
        return f"{solvents_part}|{salts_part}"
        
    @staticmethod
    def filter_components(components, db, component_type):
        filtered_components = {}
        for component, fraction in components.items():
            if isinstance(fraction, tuple):  # Check for mixed solvents
                sub_components = component.split('_')
                if all(sub in db['name'].values for sub in sub_components):
                    filtered_components[component] = {sub: frac for sub, frac in zip(sub_components, fraction)}
                else:
                    print(f"{component} contains invalid {component_type} names.")
            elif component in db['name'].values:
                filtered_components[component] = fraction
            else:
                print(f"{component} is not a valid {component_type} name.")
        return filtered_components

    @staticmethod
    def load_solvent_file(data_path=API_HOME_PATH, filename=AEM_ACCC_SOLVENTS):
        path = os.path.join(data_path, filename)
        return pd.read_csv(path)

    @staticmethod
    def load_salt_file(data_path=API_HOME_PATH, filename=AEM_ACCC_SALTS):
        path = os.path.join(data_path, filename)
        return pd.read_csv(path)

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
                 accc_electrolyte=None, 
                 salt_csv=AEM_SALTS, 
                 solvent_csv=AEM_SOLVENTS,
                 solventcomp=None,
                 solventcomppropbasis=None,
                 saltcomp=None,
                 totalsaltconc=None, 
                 tmin=None, 
                 tmax=None, 
                 stepsize=None,
                 tis=None,
                 contactangle=None,
                 porelength=None,
                 saltconc=None,
                 scaep=None,
                 dl=None,
                 output_dir=None,
                 run_name=None,
                 AEMHomePath=None,
                 AEMProgramName=None):
        self.AEMHomePath = AEMHomePath
        DLMout = self.runDLMExecutable()
        if DLMout == '1':
            self.read_AEM_data(salt_csv, solvent_csv)
        if DLMout == '6':
            if accc_electrolyte is None and electrolyte is not None:
                self.read_AEM_data(salt_csv, solvent_csv)
            if accc_electrolyte is not None and electrolyte is None:
                self.read_AEM_ACCC_data(accc_electrolyte)
            if accc_electrolyte is not None and electrolyte is not None:
                self.read_AEM_data(salt_csv, solvent_csv)
                self.read_AEM_ACCC_data(accc_electrolyte)
        self.electrolyte = electrolyte
        self.accc_electrolyte = accc_electrolyte
        self.AEM_ACCC_solvents = accc_electrolyte.solvents if accc_electrolyte else None
        self.AEM_ACCC_salts = accc_electrolyte.salts if accc_electrolyte else None
        self.cues = False
        self.run_yet = False
        self.data_processed = False
        self.aem_exe_filename = AEMProgramName  
        self.report_string = os.path.join(AEMHomePath,"Report1 -- Summary of Key Properties")
        self.dlmout = DLMout
        self.solventcomp = solventcomp
        self.solventcomppropbasis = solventcomppropbasis
        self.saltcomp = saltcomp
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
        self.dl = dl
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
    print(f"### AEM-API v1.1.0:: Starting Program!")
    
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
        print(f"### AEM-API v1.1.0:: Checking ACCC Access from DLM ...")
        fp = os.path.join(API_HOME_PATH, DLM_EXECUTABLE)
        # Run the executable with the 'check' argument
        p = sp.Popen([fp, 'check'], shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, cwd=self.AEMHomePath)
        # Capture the output
        stdout, _ = p.communicate()  # Capture output
        stdout = stdout.decode('utf-8').strip()  # Decode and strip any extra whitespace/newlines
        # Log the output and return it
        if stdout == '1':
            print(f"### AEM-API v1.1.0:: ACCC Access Invalid!")
        elif stdout == '6':
            print(f"### AEM-API v1.1.0:: ACCC Access Valid")
        else:
            print(f"### AEM-API v1.1.0:: Unknown output: {stdout}")
        print(f"### AEM-API v1.1.0:: ACCC Access Check Complete!")
        return stdout

    # Method to generate input cues for the AEM model
    def generate_cues(self):
        self.cues = []
        self.params = {}  # Dictionary to store parameter names and their corresponding values
        # w/o ACCC Case
        if self.dlmout == '1':
            self.cues.append(self.solventcomp)
            self.params["Solvent Composition"] = self.solventcomp
            self.cues.append(self.solventcomppropbasis)
            self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
            number_of_solvents = len(self.electrolyte.solvents)
            assert number_of_solvents <= 10, "Number of solvents must be no greater than 10"
            self.cues.append(number_of_solvents)
            self.params["Number of Solvents"] = number_of_solvents
            for solvent in self.electrolyte.solvents.keys():
                self.cues.append(self.AEM_solvents[solvent][0])  # append cues
            if len(self.electrolyte.solvents.keys()) > 1:  # check if not pure
                for solvent in self.electrolyte.solvents:
                    # append masses
                    self.cues.append(self.electrolyte.solvents[solvent])
            number_of_salts = len(self.electrolyte.salts)
            assert number_of_solvents <= 2, "Number of solvents must be no greater than 2"
            self.cues.append(number_of_salts)
            self.params["Number of Salts"] = number_of_salts
            for salt in self.electrolyte.salts.keys():
                self.cues.append(self.AEM_salts[salt][0])  # append self.cues
            if number_of_salts > 1:
                self.cues.append(self.saltcomp)  # specify single fixed salt prop
                self.params["Salt Composition Proportion Mode"] = self.saltcomp
                for salt in self.electrolyte.salts:
                    # append molalities
                    self.cues.append(self.electrolyte.salts[salt])
            self.cues.append(self.totalsaltconc)
            self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
            self.cues.append(self.tmin)
            self.params["Minimum Temperature"] = self.tmin
            self.cues.append(self.tmax)
            self.params["Maximum Temperature"] = self.tmax
            self.cues.append(self.stepsize)
            self.params["Temperature Step Size"] = self.stepsize
            self.cues.append(self.tis)
            self.params["Method for Triple-Ion Stability"] = self.tis
            self.cues.append(self.contactangle)
            self.params["Contact Angle"] = self.contactangle
            self.cues.append(self.porelength)
            self.params["Pore Length"] = self.porelength
            self.cues.append(self.saltconc)
            self.params["Salt Concentration of Interest"] = self.saltconc
            self.cues.append(self.scaep)
            self.params["Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations"] = self.scaep
            self.cues.append(self.dl)
            self.params["Double Layer (DL) Calculations"] = self.dl
            self.cues.append(0)
            print(f"### AEM-API v1.1.0:: Input Parameters: {self.params}")
        # w/ ACCC case
        elif self.dlmout == '6':
            # Non-ACCC Composition Case
            if self.accc_electrolyte is None:
                self.cues.append(self.solventcomp)
                self.params["Solvent Composition"] = self.solventcomp
                self.cues.append(self.solventcomppropbasis)
                self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
                accc_solvents = 0
                accc_salts = 0
                non_accc_solvents = len(self.electrolyte.solvents)
                non_accc_salts = len(self.electrolyte.salts)
                number_of_solvents = non_accc_solvents + accc_solvents
                number_of_salts = non_accc_salts + accc_salts
                assert number_of_solvents <= 10, "Number of solvents must be no greater than 10"
                assert number_of_salts <= 2, "Number of solvents must be no greater than 2"
                self.cues.append(number_of_solvents)
                self.params["Number of Solvents"] = number_of_solvents
                self.cues.append(accc_solvents)
                self.params["Number of ACCC Solvents"] = accc_solvents
                for solvent in self.electrolyte.solvents.keys():
                    self.cues.append(self.AEM_solvents[solvent][0])
                if len(self.electrolyte.solvents.keys()) > 1:  # check if not pure
                    for solvent in self.electrolyte.solvents:
                        self.cues.append(self.electrolyte.solvents[solvent]) # append masses
                self.cues.append(number_of_salts)
                self.params["Number of Salts"] = number_of_salts
                self.cues.append(accc_salts)
                self.params["Number of ACCC Salts"] = accc_salts
                for salt in self.electrolyte.salts.keys():
                    self.cues.append(self.AEM_salts[salt][0])  # append self.cues
                if number_of_salts > 1:
                    self.cues.append(self.saltcomp)
                    self.params["Salt Composition Proportion Mode"] = self.saltcomp
                    for salt in self.electrolyte.salts:
                        self.cues.append(self.electrolyte.salts[salt]) # append molalities/molarities
                self.cues.append(self.totalsaltconc)
                self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
                self.cues.append(self.tmin)
                self.params["Minimum Temperature"] = self.tmin
                self.cues.append(self.tmax)
                self.params["Maximum Temperature"] = self.tmax
                self.cues.append(self.stepsize)
                self.params["Temperature Step Size"] = self.stepsize
                self.cues.append(self.tis)
                self.params["Method for Triple-Ion Stability"] = self.tis
                self.cues.append(self.contactangle)
                self.params["Contact Angle"] = self.contactangle
                self.cues.append(self.porelength)
                self.params["Pore Length"] = self.porelength
                self.cues.append(self.saltconc)
                self.params["Salt Concentration of Interest"] = self.saltconc
                self.cues.append(self.scaep)
                self.params["Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations"] = self.scaep
                self.cues.append(self.dl)
                self.params["Double Layer (DL) Calculations"] = self.dl
                self.cues.append(0) # End
            # ACCC Composition Case
            elif self.accc_electrolyte is not None:
                # All ACCC 
                if self.electrolyte is None:
                    self.cues.append(self.solventcomp)
                    self.params["Solvent Composition"] = self.solventcomp
                    self.cues.append(self.solventcomppropbasis)
                    self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
                    for components in self.AEM_ACCC_solvents.values():
                        if isinstance(components, dict):
                            accc_solvents = len(components)  # Multiple components
                        else:
                            accc_solvents = 1  # Single component
                    accc_salts =  len(self.AEM_ACCC_salts)
                    non_accc_solvents = 0
                    non_accc_salts = 0
                    number_of_solvents = non_accc_solvents + accc_solvents
                    number_of_salts = non_accc_salts + accc_salts
                    assert number_of_solvents <= 10, "Number of solvents must be no greater than 10"
                    assert number_of_salts <= 2, "Number of solvents must be no greater than 2"
                    self.cues.append(number_of_solvents)
                    self.params["Number of Solvents"] = number_of_solvents
                    self.cues.append(accc_solvents)
                    self.params["Number of ACCC Solvents"] = accc_solvents
                    solvent_cue = '_'.join(self.AEM_ACCC_solvents.keys())
                    self.matchACCCComp()
                    self.cues.append(solvent_cue)
                    if number_of_solvents > 1:  # check if not pure
                            for solvent, composition in self.AEM_ACCC_solvents.items():
                                if isinstance(composition, dict):
                                    for component, proportion in composition.items():
                                            self.cues.append(proportion) # append masses
                    self.cues.append(accc_salts)
                    self.params["Number of ACCC Salts"] = accc_salts
                    for salt in self.AEM_ACCC_salts:
                        self.cues.append(salt)
                    self.cues.append(self.totalsaltconc)
                    self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
                    self.cues.append(self.tmin)
                    self.params["Minimum Temperature"] = self.tmin
                    self.cues.append(self.tmax)
                    self.params["Maximum Temperature"] = self.tmax
                    self.cues.append(self.stepsize)
                    self.params["Temperature Step Size"] = self.stepsize
                    self.cues.append(self.tis)
                    self.params["Method for Triple-Ion Stability"] = self.tis
                    self.cues.append(self.contactangle)
                    self.params["Contact Angle"] = self.contactangle
                    self.cues.append(self.porelength)
                    self.params["Pore Length"] = self.porelength
                    self.cues.append(self.saltconc)
                    self.params["Salt Concentration of Interest"] = self.saltconc
                    self.cues.append(self.scaep)
                    self.params["Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations"] = self.scaep
                    self.cues.append(self.dl)
                    self.params["Double Layer (DL) Calculations"] = self.dl
                    self.cues.append(0) # End
                # ACCC with Non-ACCC 
                if self.electrolyte is not None:
                    self.cues.append(self.solventcomp)
                    self.params["Solvent Composition"] = self.solventcomp
                    self.cues.append(self.solventcomppropbasis)
                    self.params["Solvent Composition Proportionality Basis"] = self.solventcomppropbasis
                    accc_solvents = 0
                    for components in self.AEM_ACCC_solvents.values():
                            if components is None or components==0:
                                accc_solvents = 0
                            elif isinstance(components, dict):
                                accc_solvents = len(components)  # Multiple components
                            else:
                                accc_solvents = 1  # Single component
                    accc_salts =  len(self.AEM_ACCC_salts)
                    non_accc_solvents = len(self.electrolyte.solvents)
                    non_accc_salts = len(self.electrolyte.salts)
                    number_of_solvents = non_accc_solvents + accc_solvents
                    number_of_salts = non_accc_salts + accc_salts
                    self.cues.append(number_of_solvents)
                    self.params["Number of Solvents"] = number_of_solvents
                    self.cues.append(accc_solvents)
                    self.params["Number of ACCC Solvents"] = accc_solvents
                    # ACCC Solvents + Non-ACCC Salt
                    if non_accc_solvents == 0 and accc_salts == 0:
                        solvent_cue = '_'.join(self.AEM_ACCC_solvents.keys())
                        self.matchACCCComp()
                        self.cues.append(solvent_cue)
                        if number_of_solvents > 1:  # check if not pure
                            for solvent, composition in self.AEM_ACCC_solvents.items():
                                if isinstance(composition, dict):
                                    for component, proportion in composition.items():
                                            self.cues.append(proportion) # append masses
                        self.cues.append(accc_salts)
                        self.params["Number of ACCC Salts"] = accc_salts
                        for salt in self.electrolyte.salts.keys():
                            self.cues.append(self.AEM_salts[salt][0])  # append self.cues
                    # Non-ACCC Solvents + ACCC Salt
                    if accc_solvents == 0 and non_accc_salts == 0:
                        for solvent in self.electrolyte.solvents.keys():
                            self.cues.append(self.AEM_solvents[solvent][0])  # append cues
                        if number_of_solvents > 1:  # check if not pure
                            for solvent in self.electrolyte.solvents:
                                # append masses
                                self.cues.append(self.electrolyte.solvents[solvent])
                        self.cues.append(number_of_salts)
                        self.params["Number of Salts"] = number_of_salts
                        self.cues.append(accc_salts)
                        self.params["Number of ACCC Salts"] = accc_salts
                        for salt in self.AEM_ACCC_salts:
                            self.cues.append(salt)       
                    self.cues.append(self.totalsaltconc)
                    self.params["Max. Total Salt Concentration of Interest"] = self.totalsaltconc
                    self.cues.append(self.tmin)
                    self.params["Minimum Temperature"] = self.tmin
                    self.cues.append(self.tmax)
                    self.params["Maximum Temperature"] = self.tmax
                    self.cues.append(self.stepsize)
                    self.params["Temperature Step Size"] = self.stepsize
                    self.cues.append(self.tis)
                    self.params["Method for Triple-Ion Stability"] = self.tis
                    self.cues.append(self.contactangle)
                    self.params["Contact Angle"] = self.contactangle
                    self.cues.append(self.porelength)
                    self.params["Pore Length"] = self.porelength
                    self.cues.append(self.saltconc)
                    self.params["Salt Concentration of Interest"] = self.saltconc
                    self.cues.append(self.scaep)
                    self.params["Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations"] = self.scaep
                    self.cues.append(self.dl)
                    self.params["Double Layer (DL) Calculations"] = self.dl
                    self.cues.append(0) # End
            print(f"### AEM-API v1.1.0:: Input Parameters: {self.params}")
    
    # Method to run the AEM model
    def runAEM(self, quiet=True):
        print(f"### AEM-API v1.1.0:: Starting Run {self.run_id}...")
        if not self.cues:
            raise ValueError("cues not populated, run generate_cues first")
        # generate input byte string
        inp = [str(cue) for cue in self.cues]
        inpb = bytes('\n'.join(inp) + '\n\n', encoding="ascii")
        # launch AEM and pass input byte string
        if quiet:
            out = sp.DEVNULL
        else:
            out = sys.stdout
        fp = os.path.join(self.AEMHomePath, self.aem_exe_filename)
        p = sp.Popen(fp, stdin=sp.PIPE, stdout=out, stderr=sp.STDOUT, cwd=self.AEMHomePath)
        print(f"### AEM-API v1.1.0:: Run {self.run_id} Complete!")
        p.communicate(inpb)
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
            print(f"### AEM-API v1.1.0:: Run {self.run_id}: Log saved to {log_file}")
        else:
            log_data = {
                "run_name": self.run_name,
                "run_id": self.run_id,
                "run_date": self.run_date,
                "run_time": self.run_time,
                "electrolyte_composition": self.electrolyte.CompositionID if self.electrolyte is not None else None,
                "ACCC_electrolyte_composition": self.accc_electrolyte.CompositionID if self.accc_electrolyte is not None else None,
                "input_params": self.params
            }
            log_file = os.path.join(self.run_output_dir, f"AEMRun-{self.run_name}-{self.run_date}-{self.run_time}-Log.json")
            print(f"### AEM-API v1.1.0:: Run {self.run_name}: Log saved to {log_file}")
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=4)
        return None
    
    # Function to copy report files to run_output_dir
    def copy_report_files(self):
        dstfolder = os.path.join(self.run_output_dir,"Reports")
        os.makedirs(dstfolder, exist_ok=True)
        for report_file in self.report_files:
            src = os.path.join(self.AEMHomePath, report_file)
            dst = os.path.join(dstfolder, f"{report_file}.txt")
            if os.path.exists(src):
                shutil.copy(src, dst)
            else:
                print(f"### AEM-API v1.1.0:: Run {self.run_id}: Report file {report_file} not found.")
        print(f"### AEM-API v1.1.0:: Run {self.run_id}: Copied generated Report files to {dstfolder}")
        print(f"### AEM-API v1.1.0:: Run {self.run_id}: Running AEM-PARSER on Report files and converting to .csv and .json...")
        aem_convert_to_csv(dstfolder)
        print(f"### AEM-API v1.1.0:: Run {self.run_id}: AEM-PARSER converted Report files to .csv and saved to {dstfolder}\\csv")
        aem_convert_to_json(dstfolder)
        print(f"### AEM-API v1.1.0:: Run {self.run_id}: AEM-PARSER converted Report files to .json and saved to {dstfolder}\\json")
    
    # Function to preview data from parsed report files
    def plot_parsed_data(self, x, y, report_number):
        output_dir = os.path.join(self.run_output_dir,"Reports")
        run = aem_run()
        run.parse_run(output_dir)
        fig, ax = plt.subplots(figsize=(20, 6))
        report = getattr(run, report_number.lower())  # Access report dynamically based on input
        for s in report.items:
            x_plot = [d[x] for d in s.data]
            y_plot = [d[y] for d in s.data]
            # Generate label with information about solvents, salts, and temperature
            label = f"Solvents: {s.solvents_str_no_comma()}\nSalts: {s.salts_str_no_comma()}\nTemperature: {s.temperature_str()}"
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
        plt.show()

    # Method to process the output from the AEM model
    def process(self):
        if not self.run_yet:
            raise ValueError("Run AEM first for this Electrolyte object")
        with open(self.report_string, 'r') as f:
            lines = f.readlines()
        d = {}
        for num1, line in enumerate(lines):
            if "Results" in line:
                num2 = num1 + 1
                arr = []
                reading = True
                while reading:
                    if "TI Stability" in lines[num2]:
                        reading = False
                    else:
                        arr.append(lines[num2])
                        num2 += 1
                d[line] = arr
        # process keys down to temperature
        def get_key_single(string):
            string_in_list = string.strip().split()
            return float(string_in_list[string_in_list.index('Temp.') + 2])  # TEMP ONLY
        def get_key_binary(string):
            k = string.strip().split()
            i = k.index("+")
            t = (k[i - 1], k[i + 2], float(k[i - 2]), float(k[i + 1]))  # (salt1,salt2,frac1,frac2)
            T = float(k[k.index('Temp.') + 2])
            return t + (T,)  # (salt1,salt2,frac1,frac2,Temp)
        def find_data_in_txt(list_of_lines):
            expr = r'\-{75,}'
            p = re.compile(expr)
            table_indices = []
            for ind, line in enumerate(list_of_lines):
                if p.match(line.strip()):
                    table_indices.append(ind)
            string_data = list_of_lines[table_indices[0] + 1:table_indices[1]]
            def floator(val):
                try:
                    x = float(val)
                except ValueError:
                    x = '>10000'
                return x
            return [[floator(val) for val in line.strip().split()] for line in string_data]
        # process values to pandas dataframe
        def data_lines_to_dataframe(list_of_lines, columns):
            return pd.DataFrame(list_of_lines, columns=columns)
        columns = ["m", "c", "c_eff_trans", "wt fr salt", "mole fr salt", "density (g/mL)", "cP_mean", "sig1 (eff)", "sig2 (eff)", "S(+)",
                   "Rational Act.Coef. y+-", "Diff. Coeff. cm^2/s", "Cond (mS) 2", "t+(a)", "t+(b)",
                   "dissoc (SI)", "dissoc (TI)"]
        salts_count = len(self.electrolyte.salts) if self.electrolyte and self.electrolyte.salts else 0
        accc_salts_count = len(self.AEM_ACCC_salts) if self.AEM_ACCC_salts else 0
        if salts_count == 1 or accc_salts_count == 1:
            self.data = {get_key_single(k): data_lines_to_dataframe(find_data_in_txt(v), columns) for k, v in d.items()}
        elif salts_count == 2 or accc_salts_count == 2:
            self.data = {get_key_binary(k): data_lines_to_dataframe(find_data_in_txt(v), columns) for k, v in d.items()}    
        self.data_processed = True
    
    # Function to save processed data  
    def save_processed_data(self):
        if self.run_name is None:
            print(f"### AEM-API v1.1.0:: Saving Combined and Processed Data for Run {self.run_id}...")
        else:
            print(f"### AEM-API v1.1.0:: Saving Combined and Processed Data for Run {self.run_name}...")
        # Initialize an empty DataFrame to store all processed data
        all_data = pd.DataFrame()
        # Access, display, and save the processed data
        for key, df in self.data.items():
            #print(f"Key: {key}")
            #print(df)
            #print("DataFrame Columns:", df.columns)  # Print the DataFrame columns for debugging
            # Add a new column to indicate the temperature (previously 'Key')
            df['Temperature'] = key
            # Append the DataFrame to the combined DataFrame
            all_data = pd.concat([all_data, df])
        # Save the combined DataFrame to a single CSV file
        if self.run_name is None:
            combined_csv_path = os.path.join(self.run_output_dir, f"{self.run_id}_CPD.csv")
        else:
            combined_csv_path = os.path.join(self.run_output_dir, f"{self.run_name}_CPD.csv")
        all_data.to_csv(combined_csv_path, index=False)
        if self.run_name is None:
            print(f"### AEM-API v1.1.0:: Combined and Processed Data for Run {self.run_id} saved to {combined_csv_path}")
        else:
            print(f"### AEM-API v1.1.0:: Combined and Processed Data for Run {self.run_name} saved to {combined_csv_path}")
        return all_data
    
    # Function to plot processed data
    def plot_processed_data(self, all_data):
        plot_path = os.path.join(self.run_output_dir, "Plots")
        os.makedirs(plot_path, exist_ok=True)
        if self.run_name is None:
            print(f"### AEM-API v1.1.0:: Plotting Combined and Processed Data for Run {self.run_id}...")
        else:
            print(f"### AEM-API v1.1.0:: Plotting Combined and Processed Data for Run {self.run_name}...")
        # Density vs m,c
        fig, axs = plt.subplots(2, 1, figsize=(10, 12))
        # Plot Density vs. m
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[0].plot(subset['m'], subset['density (g/mL)'], label=f'{temp}°C', marker='o')
            axs[0].set_xlabel('m (mol/kg)', fontweight="bold")
        axs[0].set_ylabel('Density (g/mL)', fontweight='bold')
        axs[0].set_title('Density vs. Molal Salt Concentration (m)')
        axs[0].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[0].grid(True)
        # Plot Density vs. c
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[1].plot(subset['c'], subset['density (g/mL)'], label=f'{temp}°C', marker='o')
            axs[1].set_xlabel('c (mol/L)', fontweight="bold")
        axs[1].set_ylabel('Density (g/mL)', fontweight='bold')
        axs[1].set_title('Density vs. Molar Salt Concentration (c)')
        axs[1].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[1].grid(True)
        # Save the combined plot
        density_plot_path = os.path.join(plot_path, "Density.png")
        plt.savefig(density_plot_path, bbox_inches='tight')
        plt.close()
        # Combined Conductivity vs. m, c
        fig, axs = plt.subplots(2, 1, figsize=(10, 12))
        # Plot CC vs. m
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[0].plot(subset['m'], subset['Cond (mS) 2'], label=f'{temp}°C', marker='o')
            axs[0].set_xlabel('m (mol/kg)', fontweight="bold")
        axs[0].set_ylabel('Combined Conductivity (mS)', fontweight="bold")
        axs[0].set_title('Combined Conductivity vs. Molal Salt Concentration (m)')
        axs[0].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[0].grid(True)
        # Plot CC vs. c
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[1].plot(subset['c'], subset['Cond (mS) 2'], label=f'{temp}°C', marker='o')
            axs[1].set_xlabel('c (mol/L)', fontweight="bold")
        axs[1].set_ylabel('Combined Conductivity (mS)', fontweight='bold')
        axs[1].set_title('Combined Conductivity vs. Molar Salt Concentration (c)')
        axs[1].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[1].grid(True)
        # Save the combined plot
        cc_plot_path = os.path.join(plot_path, "CombinedConductivity.png")
        plt.savefig(cc_plot_path, bbox_inches='tight')
        plt.close()
        # Mean Viscosity vs. m, c
        fig, axs = plt.subplots(2, 1, figsize=(10, 12))
        # Plot MV vs. m
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[0].plot(subset['m'], subset['cP_mean'], label=f'{temp}°C', marker='o')
            axs[0].set_xlabel('m (mol/kg)', fontweight="bold")
        axs[0].set_ylabel('Mean Viscosity (cP)', fontweight='bold')
        axs[0].set_title('Mean Viscosity vs. Molal Salt Concentration (m)')
        axs[0].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[0].grid(True)
        # Plot MV vs. c
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[1].plot(subset['c'], subset['cP_mean'], label=f'{temp}°C', marker='o')
            axs[1].set_xlabel('c (mol/L)', fontweight="bold")
        axs[1].set_ylabel('Mean Viscosity (cP)', fontweight='bold')
        axs[1].set_title('Mean Viscosity vs. Molar Salt Concentration (c)')
        axs[1].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[1].grid(True)
        # Save the combined plot
        mv_plot_path = os.path.join(plot_path, "MeanViscosity.png")
        plt.savefig(mv_plot_path, bbox_inches='tight')
        plt.close()
        # Cation Transference Number vs. m, c
        fig, axs = plt.subplots(2, 1, figsize=(10, 12))
        # Plot Cation Transference Number vs. m
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[0].plot(subset['m'], subset['t+(a)'], label=f't+(a) {temp}°C', marker='.')
                    axs[0].plot(subset['m'], subset['t+(b)'], label=f't+(b) {temp}°C', marker='o')
            axs[0].set_xlabel('m (mol/kg)', fontweight="bold")
        axs[0].set_ylabel('Cation Transference Number', fontweight='bold')
        axs[0].set_title('Cation Transference Number vs. Molal Salt Concentration (m)')
        axs[0].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[0].grid(True)
        # Plot Cation Transference Number vs. c
        if 'Temperature' in all_data.columns:
            for temp in all_data['Temperature'].unique():
                if self.tmin <= temp <= self.tmax:
                    subset = all_data[all_data['Temperature'] == temp]
                    axs[1].plot(subset['c'], subset['t+(a)'], label=f't+(a) {temp}°C', marker='.')
                    axs[1].plot(subset['c'], subset['t+(b)'], label=f't+(b) {temp}°C', marker='o')
            axs[1].set_xlabel('c (mol/L)', fontweight="bold")
        axs[1].set_ylabel('Cation Transference Number', fontweight="bold")
        axs[1].set_title('Cation Transference Number vs. Molar Salt Concentration (c)')
        axs[1].legend(title='Temperature', bbox_to_anchor=(1.02, 1))
        axs[1].grid(True)
        # Save the plot
        ctn_plot_path = os.path.join(plot_path, "CationTransferenceNumber.png")
        plt.savefig(ctn_plot_path, bbox_inches='tight')
        plt.close()
        if self.run_name is None:
            print(f"### AEM-API v1.1.0:: Combined and Processed Data Plots for Run {self.run_id} saved to '{plot_path}'")
        else:
            print(f"### AEM-API v1.1.0:: Combined and Processed Data Plots for Run {self.run_name} saved to '{plot_path}'")
        print(f"### AEM-API v1.1.0:: End of Program! (© 2024 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved)")