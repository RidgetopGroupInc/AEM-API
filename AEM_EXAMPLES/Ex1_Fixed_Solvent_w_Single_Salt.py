# ============================================================================
"""               Advanced Electrolyte Model (AEM) API Demo                """
""" © 2025 Ridgetop Group, Inc. and Adarsh Dave (CMU), All Rights Reserved """
# ============================================================================

## Import Libraries and AEM API Classes
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from AEM_API import ElectrolyteComposition, AEM_API

## AEM Directories
homedir = os.path.expanduser("~")
AEM_HOME_PATH = rf'{homedir}\Documents\AEM\CLI'   # Path to AEM/CLI/ (Update path if different!)
AEM_PROGRAM_NAME = "AEM-2251M-D-ACCC-DLM.exe"

output_dir = 'AEM-API-Output\\Demos'              # Output Directory for AEM API Runs
run_name = 'Ex1_Fixed_Solvent_Single_Salt'        # Run Name

## Define Non-ACCC Electrolyte Composition - Solvents and Salts
solvents = {'EP': 25, 'DMC': 50, 'EC': 25} 
# solvents defines ethyl propionate 25%, dimethyl carbonate 50%, ethylene carbonate 25%
# proportions do not need to add up to 100%, values will be normalized
salts = {'LiPF6': 1.0}
# salts defined is LiPF6 at 1.0 (100%), proportion really only used if multiple salts defined and
# composition proportion mode is set to single fixed proportion
electrolyte = ElectrolyteComposition.translate_electrolyte(solvents=solvents, salts=salts)
number_of_total_solvents = 3   # Total number of solvents (ACCC and Non-ACCC Solvents)
number_of_accc_solvents = 0    # Number of ACCC Solvents in ACCC Solvent Class (None used in this example)
number_of_total_salts = 1      # Total number of salts (ACCC and Non-ACCC Salts)
number_of_accc_salts = 0       # Number of ACCC Salts (None used in this example)

## Define Input Parameters
solventcomp = 1                # Solvent Composition: 1 (Single Fixed Composition) or 2 (Larger Matrix)
solventcomppropbasis = 1       # Solvent Composition Proportionality Basis: 1 (Volume) or 2 (Mass)
saltcomp = 1                   # Salt Composition [Salts > 1]: 1 (Single Fixed Composition) or 2 (Several Proportions)
saltconcmode = 1               # Salt Concentration Mode:  1 (Default: typical range covering several salt molal concentration. 2 (dilute solution conditions (molal step size 0.001) covering 0.1m total salt.))
totalsaltconc = 5              # Max. Total Salt Concentration of Interest (Required if salt concentration mode is 1)
tmin = -30                     # Minimum Temperature: -30deg to 60 deg (Do not exceed 100deg)
tmax = 60                      # Maximum Temperature: -30deg to 60 deg (Do not exceed 100deg)
stepsize = 5                   # Temperature Stepsize: 5deg or 10deg
tis = 1                        # Triple-Ion Stability Method: 1 (default) or 2 (inequalities are automatically determined)
contactangle = 35              # Contact Angle: 0deg to 90deg
porelength = 20                # Pore Length: 0.1um to 50um
saltconc = 1.5                 # Input Salt Concentration of Interest: 0.1 to Max. Salt Conc.
scaep = 0                      # Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations: 0 (No) or 1 (Yes)
dl = 0                         # Double Layer (DL) Calculations: 0 (No) or 1 (Yes)

aem = AEM_API(  electrolyte=electrolyte,
                number_of_total_solvents = number_of_total_solvents,
                number_of_accc_solvents = number_of_accc_solvents,
                number_of_total_salts = number_of_total_salts,
                number_of_accc_salts = number_of_accc_salts,
                solventcomp = solventcomp,
                solventcomppropbasis = solventcomppropbasis, 
                saltcomp = saltcomp,
                saltconcmode = saltconcmode, 
                totalsaltconc = totalsaltconc,
                tmin = tmin, 
                tmax = tmax,
                stepsize=stepsize,
                tis = tis, 
                contactangle=contactangle, 
                porelength=porelength,
                saltconc = saltconc,
                scaep = 0,
                dl = dl,
                output_dir=output_dir,
                run_name=run_name,
                AEMHomePath=AEM_HOME_PATH,
                AEMProgramName=AEM_PROGRAM_NAME
              )

aem.generate_cues()
print(aem.params, aem.cues)

aem.runAEM(quiet=True)
report_no = "Report02"   # Report01-20 
x = "c2"                 # x-axis: Any column from chosen report 
y = "gamma"              # y-axis: Any column from chosen report 
aem.plot_parsed_data(x=x, y=y, report_number=report_no)