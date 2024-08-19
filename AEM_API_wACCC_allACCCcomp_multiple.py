# ============================================================================
"""               Advanced Electrolyte Model (AEM) API Demo                """
""" © 2024 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## Import Libraries and AEM API Classes
import os
import sys
from AEM_API import ElectrolyteComposition, ACCCElectrolyteComposition, AEM_API

## AEM Directories
homedir = os.path.expanduser("~")
AEM_HOME_PATH = rf'{homedir}\Documents\AEM\CLI'   # Path to AEM/CLI/ (Update path if different!)
AEM_PROGRAM_NAME = "aem-2242m-d-accc-dlm.exe"     # aem-2242m-d-accc-dlm.exe or aem-2241ml.exe

## Define ACCC Electrolyte Composition - Solvents and Salts
solvents = {'EC_EMC': (70, 30)}
salts = {'LiPF6_w_EC_EMC': 100}
accc_electrolyte = ACCCElectrolyteComposition(solvents=solvents, salts=salts)

## Define Input Parameters
output_dir = 'AEM-API-Output\\Demos'          # Output Directory for AEM API Runs
run_name = 'w_ACCC_allACCCcomp_multiple'      # Run Name

useACCC = True                 # Input to use ACCC: Yes = True or No = False

solventcomp = 1                # Solvent Composition: 1 (Single Fixed Composition) or 2 (Larger Matrix)
solventcomppropbasis = 2       # Solvent Composition Proportionality Basis: 1 (Volume) or 2 (Mass)
saltcomp = 1                   # Salt Composition [Salts > 1]: 1 (Single Fixed Composition) or 2 (Several Proportions)
totalsaltconc = 1              # Max. Total Salt Concentration of Interest
tmin = 10                      # Minimum Temperature: -30deg to 60 deg (Do not exceed 100deg)
tmax = 60                      # Maximum Temperature: -30deg to 60 deg (Do not exceed 100deg)
stepsize = 10                  # Temperature Stepsize: 5deg or 10deg
tis = 1                        # Triple-Ion Stability Method: 1 (default) or 2 (inequalities are automatically determined)
contactangle = 90              # Contact Angle: 0deg to 90deg
porelength = 50                # Pore Length: 0.1um to 50um
saltconc = 0.1                 # Input Salt Concentration of Interest: 0.1 to Max. Salt Conc.
scaep = 0                      # Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations: 0 (No) or 1 (Yes)
dl = 0                         # Double Layer (DL) Calculations: 0 (No) or 1 (Yes)

## Initialize the AEM-API Object
aem = AEM_API(accc_electrolyte=accc_electrolyte,
              useACCC=useACCC,
              solventcomp=solventcomp,
              solventcomppropbasis=solventcomppropbasis,
              saltcomp=saltcomp,
              totalsaltconc=totalsaltconc, 
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
              run_name=run_name,
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