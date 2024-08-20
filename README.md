# Advanced Electrolyte Model (AEM) API

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<p align="center">
  <img src="https://github.com/RidgetopGroupInc/AEM-API/assets/134314322/ae32d001-0d1a-4e53-a9f8-dff35e1bdab5" alt="AEM-API" width="400" height="200">
</p>

The **Advanced Electrolyte Model (AEM) Application Program Interface (API)** is a supporting software toolbox to the AEM CLI executable, designed to analyze and predict the properties of electrolyte compositions used in various applications. Developed by Ridgetop Group, Inc. and in collaboration with Adarsh Dave (Carnegie Mellon University), this API allows users to create, manage, and simulate electrolyte compositions with Python scripts, leveraging the extensive databases of solvents and salts with the AEM compound library. Additionally, the API combines results from AEM output Report 1, saves that to a .csv file, and provides detailed insights into example key properties such as density, viscosity, conductivity, and ion association populations through graphical plots.

****Link to Repository:** [https://github.com/RidgetopGroupInc/AEM-API](https://github.com/RidgetopGroupInc/AEM-API)**

<!-- TABLE OF CONTENTS -->
## Table of Contents
- [About the AEM API](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

<!-- ABOUT THE AEM API -->
## About the AEM API
Shown in the figure below is a block diagram of the AEM API architecture. The diagram is divided into several sections, each elaborating on different aspects of the AEM API, from input parameters to outputs, classes, and reports.

- On the **user level**, there are two major inputs - **Electrolyte Composition** and **Input Parameters**. In the Electrolyte Composition, the user can define up to 10 solvents and up to two salts. It outlines how the solvents and salts are categorized and the parameters that are considered for each. Next, Input Parameters lists the various inputs required for running AEM CLI executable. These inputs are essential for configuring AEM simulation runs and determining the specific conditions under which the model operates.
- Within the **API itself (AEM_API.py)** there are two classes - the **ElectrolyteComposition Class** and the **AEM_API Class**. The ElectrolyteComposition Class includes functions for managing file dumps, naming compositions, calculating volumes, molarity, concentrations, and other properties. The AEM_API Class contains functions for reading inputs, generating compositions, running simulations using the AEM CLI program, saving logs, exporting files and results, processing data, and saving processed data.
- The **Outputs** from the API are organized into the **AEM_API_Output** directory in run directories with the name **AEMRun-RunID-RunDate-RunTime**. Each run directory includes the **Reports** and **Plots** folders along with the combined processed data .csv file **(RunID-CPD.csv)** and a run log .json file **(AEMRun-RunID-RunDate-RunTime-Log.json)**. The Reports folder contains different types of reports that the AEM CLI program can generate. These reports cover a wide range of analyses, from key properties summaries and thermodynamic terms to density, viscosity, conductivity, and cation desolvation. Other reports focus on dielectric analysis, transport properties, molar volume, ion-pair formation, self-diffusion coefficients, and ligand-wise analyses, among others. Each report provides detailed insights into specific aspects of the electrolyte compositions and their behaviors under various conditions. The Plots folder contains visual plots for various electrolyte properties.

![AEM-API Architecture](https://github.com/RidgetopGroupInc/AEM-API/assets/134314322/d8c554a3-ddc2-45b8-a696-0f14d55cd593)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/RidgetopGroupInc/AEM-API.git
   ```
2. Install the required dependencies
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->
## Usage

### Initialize the Electrolyte Composition
Define the composition of the solvents and salts.

```python
from AEM_API import ElectrolyteComposition, AEM_API

solvents = {'EMC': 0.7, 'EC': 0.3}
salts = {'LiPF6': 1}
electrolyte_comp = ElectrolyteComposition.by_mass_fraction_and_molality(solvents=solvents, salts=salts)
```

### Run the AEM Model
Set up the necessary parameters and execute the AEM model.

```python
import os

# AEM Directories
homedir = os.path.expanduser("~")
AEM_HOME_PATH = rf'{homedir}\Documents\AEM\CLI'
AEM_PROGRAM_NAME = "aem-2242m-d-accc-dlm.exe"

aem_api = AEM_API(
    electrolyte=electrolyte_comp, 
    solventcomp=1, 
    solventcomppropbasis=2, 
    tmin=20, 
    tmax=60, 
    stepsize=10, 
    tis=1, 
    contactangle=90, 
    porelength=50, 
    saltconc=0.1, 
    scaep=0, 
    dl=0, 
    output_dir='output', 
    AEMHomePath=AEM_HOME_PATH, 
    AEMProgramName=AEM_PROGRAM_NAME
)

aem_api.generate_cues()
aem_api.runAEM(quiet=True)
```

### Process and Plot Data
Process the output data and generate plots.

```python
aem_api.process()
all_data = aem_api.save_processed_data()
aem_api.plot_processed_data(all_data)
```

<!-- ROADMAP -->
## Roadmap
See the [open issues](https://github.com/RidgetopGroupInc/AEM-API/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License
Distributed under the GNU GPL-3.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact
![RGIPrimary](https://github.com/RidgetopGroupInc/AEM-API/assets/134314322/418a1214-676c-4bdc-a09d-1a319725874e)

### For Scientific Enquiries
- **Dr. Kevin Gering** (Distinguished Scientist, Idaho National Laboratory) - [kevin.gering@inl.gov](mailto:kevin.gering@inl.gov)
  
### For Technical Enquiries & Assistance
**_AEM API_**
- **Arsh Nadkarni** (Applications Engineer, Ridgetop) - [anadkarni@ridgetopgroup.com](mailto:anadkarni@ridgetopgroup.com)
- **Dr. Basab Goswami** (Battery Simulations Engineer, Ridgetop) - [brdgoswami@ridgetopgroup.com](mailto:brdgoswami@ridgetopgroup.com)

**_AEM GUI/CLI_**
- **Christopher Curti** (Senior Software Engineer, Ridgetop) - [ccurti@ridgetopgroup.com](mailto:ccurti@ridgetopgroup.com)

### For Business & Licensing Enquiries
- **Wyatt Pena** (VP of Operations, Ridgetop) - [wpena@ridgetopgroup.com](mailto:wpena@ridgetopgroup.com)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
- **Dr. Adarsh Dave** (Research Staff, Carnegie Mellon University) - [ardave@andrew.cmu.edu](mailto:ardave@andrew.cmu.edu)
- **[othneildrew's Best-README-Template](https://github.com/othneildrew/Best-README-Template)**

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/RidgetopGroupInc/AEM-API.svg?style=for-the-badge
[contributors-url]: https://github.com/RidgetopGroupInc/AEM-API/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RidgetopGroupInc/AEM-API.svg?style=for-the-badge
[forks-url]: https://github.com/RidgetopGroupInc/AEM-API/network/members
[stars-shield]: https://img.shields.io/github/stars/RidgetopGroupInc/AEM-API.svg?style=for-the-badge
[stars-url]: https://github.com/RidgetopGroupInc/AEM-API/stargazers
[issues-shield]: https://img.shields.io/github/issues/RidgetopGroupInc/AEM-API.svg?style=for-the-badge
[issues-url]: https://github.com/RidgetopGroupInc/AEM-API/issues
[license-shield]: https://img.shields.io/github/license/RidgetopGroupInc/AEM-API.svg?style=for-the-badge
[license-url]: https://github.com/RidgetopGroupInc/AEM-API/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/yourlinkedin
