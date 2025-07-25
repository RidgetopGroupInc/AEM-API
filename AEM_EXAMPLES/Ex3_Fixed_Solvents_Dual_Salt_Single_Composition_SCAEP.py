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
run_name = 'Ex3_Fixed_Solvents_Dual_Salt_Single_Composition_SCAEP'            # Run Name

## Define Non-ACCC Electrolyte Composition - Solvents and Salts
solvents = {'EC': 25, 'DMC': 50, 'EP': 25} 
# solvents defines ethylene carbonate 25%, dimethyl carbonate 50%, ethyl propionate 25% 
# proportions do not need to add up to 100%, values will be normalized
salts = {'LiPF6': 0.7, 'LiBF4': 0.3}
# salts defined are LiPF6 at 0.7 (70%) and LiBF4 at 0.3 (30%), proportion really only used if multiple salts defined and
# composition proportion mode is set to single fixed proportion
electrolyte = ElectrolyteComposition.translate_electrolyte(solvents=solvents, salts=salts)
number_of_total_solvents = 3   # Total number of solvents (ACCC and Non-ACCC Solvents)
number_of_accc_solvents = 0    # Number of ACCC Solvents in ACCC Solvent Class (None used in this example)
number_of_total_salts = 2      # Total number of salts (ACCC and Non-ACCC Salts)
number_of_accc_salts = 0    # Number of ACCC Salts (None used in this example)

## Define Input Parameters
solventcomp = 1                # Solvent Composition: 1 (Single Fixed Composition) or 2 (Larger Matrix)
solventcomppropbasis = 1       # Solvent Composition Proportionality Basis: 1 (Volume) or 2 (Mass)
saltcomp = 1                   # Salt Composition [Salts > 1]: 1 (Single Fixed Composition) or 2 (Several Proportions)
saltconcmode = 1               # Salt Concentration Mode:  1 (Default: typical range covering several salt molal concentration. 2 (dilute solution conditions (molal step size 0.001) covering 0.1m total salt.))
totalsaltconc = 7              # Max. Total Salt Concentration of Interest (Required if salt concentration mode is 1)
tmin = -20                     # Minimum Temperature: -30deg to 60 deg (Do not exceed 100deg)
tmax = 50                      # Maximum Temperature: -30deg to 60 deg (Do not exceed 100deg)
stepsize = 5                   # Temperature Stepsize: 5deg or 10deg
tis = 1                        # Triple-Ion Stability Method: 1 (default) or 2 (inequalities are automatically determined)
contactangle = 35              # Contact Angle: 0deg to 90deg
porelength = 20                # Pore Length: 0.1um to 50um
saltconc = 1.5                 # Input Salt Concentration of Interest: 0.1 to Max. Salt Conc.
scaep = 1                      # Surface-Charge Attenuated Electrolyte Permittivity (SCAEP) Calculations: 0 (No) or 1 (Yes)
scaep_pulse = 1                # SCAEP Type of pulse condition 1: Discharge 2: Charge
scaep_cellvoltage = 4.2        # SCAEP Cell Voltage of Interest
scaep_bulksaltconc = 2.0       # SCAEP Bulk Salt Concentration in molal
scaep_thickness = 250          # SCAEP Thickness of Cathode(Discharge) or Anode (Charge) SEI (Angstroms)
scaep_permittivity = 12        # SCAEP Relative Permittivity of Cathode(Discharge) or Anode (Charge) SEI (%)
scaep_porosity = 0.3           # SCAEP Porosity of Cathode(Discharge) or Anode (Charge) SEI
dl = 0                         # Double Layer (DL) Calculations: 0 (No) or 1 (Yes)
print(type(scaep_pulse), scaep_pulse)
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
                scaep = scaep,
                scaep_pulse = scaep_pulse,
                scaep_cellvoltage = scaep_cellvoltage,
                scaep_bulksaltconc = scaep_bulksaltconc,
                scaep_thickness = scaep_thickness,
                scaep_permittivity= scaep_permittivity,
                scaep_porosity= scaep_porosity,
                dl = dl,
                output_dir=output_dir,
                run_name=run_name,
                AEMHomePath=AEM_HOME_PATH,
                AEMProgramName=AEM_PROGRAM_NAME
              )

aem.generate_cues()
print(aem.params, aem.cues)

aem.runAEM(quiet=True)
report_no = "Report10"   # Report01-20 
x = "r"                 # x-axis: Any column from chosen report 
y = "solution_rel_perm_electrolyte_plus_sch"     # y-axis: Any column from chosen report 
aem.plot_parsed_data(x=x, y=y, report_number=report_no)