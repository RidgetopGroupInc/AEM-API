# ============================================================================
"""               Advanced Electrolyte Model (AEM) API Demo                """
""" © 2024 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## Import Libraries
import os
import matplotlib.pyplot as plt
import pandas as pd
from AEM_API import ElectrolyteComposition, AEM_API
import datetime
import uuid
import json

## AEM Directories
AEM_HOME_PATH = r'C:\\Users\\anadkarni\\Documents\\AEM\\CLI'
AEM_PROGRAM_NAME = "aem-2242m-d-accc-dlm.exe"

## Define Electrolyte Composition - Solvents and Salts
solvents = {'EMC': 0.7, 'EC': 0.3}
salts = {'LiPF6': 1}
electrolyte_comp = ElectrolyteComposition.by_mass_fraction_and_molality(solvents=solvents, salts=salts)

## Define Input Parameters
output_dir = 'AEM-API-Output'  # Output Directory for AEM API Runs
solventcomp = 1                # Solvent Composition: 1 (Single Fixed Composition) or 2 (Larger Matrix)
solventcomppropbasis = 2       # Solvent Composition Proportionality Basis: 1 (Volume) or 2 (Mass)
tmin = 20                      # Minimum Temperature: -30deg to 60 deg (Do not exceed 100deg)
tmax = 60                      # Maximum Temperature: -30deg to 60 deg (Do not exceed 100deg)
stepsize = 10                  # Temperature Stepsize: 5deg or 10deg
tis = 1                        # Triple-Ion Stability Method: 1 (default) or 2 (inequalities are automatically determined)
contactangle = 90              # Contact Angle: 0deg to 90deg
porelength = 50                # Pore Length: 0.1um to 50um
saltconc = 0.1                 # Input Salt Concentration of Interest: 0.1 to 4
scaep = 0                      # Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations: 0 (No) or 1 (Yes)
dl = 0                         # Double Layer (DL) Calculations: 0 (No) or 1 (Yes)

## Initialize the AEM-API Object
aem = AEM_API(electrolyte=electrolyte_comp,
              solventcomp=solventcomp,
              solventcomppropbasis=solventcomppropbasis, 
              tmin=tmin, 
              tmax=tmax, 
              stepsize=stepsize,
              tis=tis,
              contactangle=contactangle,
              porelength=porelength,
              saltconc=saltconc,
              scaep=scaep,
              dl=dl, 
              output_dir=output_dir,
              AEMHomePath=AEM_HOME_PATH,
              AEMProgramName=AEM_PROGRAM_NAME) 

## Generate Cues for AEM CLI
aem.generate_cues()

## Run AEM
aem.runAEM(quiet=True)

## Process the Output Data & Save 
aem.process()
all_data = aem.save_processed_data()

## Plot the Output Data
aem.plot_processed_data(all_data)
