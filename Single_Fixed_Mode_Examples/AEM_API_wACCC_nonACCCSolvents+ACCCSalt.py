# ============================================================================
"""               Advanced Electrolyte Model (AEM) API Demo                """
""" © 2025 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## Import Libraries and AEM API Classes
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from AEM_API import ElectrolyteComposition, ACCCElectrolyteComposition, AEM_API

## AEM Directories
homedir = os.path.expanduser("~")
AEM_HOME_PATH = rf'{homedir}\Documents\AEM\CLI'   # Path to AEM/CLI/ (Update path if different!)
AEM_PROGRAM_NAME = "aem-2243m-d-accc.exe"

## Define Non-ACCC Electrolyte Composition - Solvents and Salts
solvents = {'EMC': 0.7, 'EC': 0.3}
salts = {}
electrolyte = ElectrolyteComposition.by_mass_fraction_and_molality(solvents=solvents, salts=salts)

## Define ACCC Electrolyte Composition - Solvents and Salts
accc_solvents = {}
accc_salts = {'LiPF6_w_EC_EMC': 100}
accc_electrolyte = ACCCElectrolyteComposition(solvents=accc_solvents, salts=accc_salts)

## Define Input Parameters
output_dir = 'AEM-API-Output\\Demos'                   # Output Directory for AEM API Runs
run_name = 'wACCC_nonACCCSolvents+ACCCSalt'            # Run Name

solventcomp = 1                # Solvent Composition: 1 (Single Fixed Composition) or 2 (Larger Matrix)
cmfoption = None               # Set CMF for 1 Solvent if Solvents > 2: None, 0 (No) or 1 (Yes)
cmfsolventindex = None         # Set CMF Solvent Index
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
aem = AEM_API(electrolyte=electrolyte,
              accc_electrolyte=accc_electrolyte,
              solventcomp=solventcomp,
              cmfoption=cmfoption,
              cmfsolventindex=cmfsolventindex,
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

## Visualize the AEM_PARSER Parsed Data 
report_no = "Report02"   # Report01-20 
x = "c2"                 # x-axis: Any column from chosen report 
y = "gamma"              # y-axis: Any column from chosen report 
aem.plot_parsed_data(x=x, y=y, report_number=report_no)
