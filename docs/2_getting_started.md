# Getting Started

This page prepares your environment so you can build and run a model.  

---

## Software Requirements

| Component     | Version (tested)          |
|---------------|---------------------------|
| Python        | 3.12                      |
| Julia         | 1.11                      |
| Spine Toolbox | 0.12.0.dev12              |
| SpineOpt      | 0.9.2                     |

> Spine Toolbox manages the project and data stores; SpineOpt is the optimization model used **inside** Spine Toolbox. Python is used to process the input data into a readable format within Spine Toolbox and Julia to run the optimization.

---

## Installation Steps

### 1. Python set-up

Download and install Python from the [official website](https://www.python.org/downloads/).
Make sure to check the option to add Python to your system PATH during installation.

#### Python libraries (installed via `requirements.txt`)
- pandas
- numpy
- openpyxl
- matplotlib
- seaborn

Install all at once:

```bash
pip install -r requirements.txt
```

---

### 2. Install Spine Toolbox

Follow the installation guide available on the [Spine Toolbox GitHub repository](https://github.com/spine-tools/Spine-Toolbox).

---

### 3. Install SpineOpt

You can install SpineOpt directly from Spine Toolbox.
For more details, refer to the [official SpineOpt documentation](https://spine-toolbox.readthedocs.io/en/stable/how_to_run_spineopt.html) or the [SpineOpt GitHub repository](https://github.com/spine-tools/SpineOpt.jl).
We recommend reviewing the documentation, especially the visual guide that explains the color coding for components (e.g., production units in red, connections in green, and physical nodes in blue).

---

### 4. Prepare project strcture

Clone or download the MORPHE2US repo (Excel workbook and Python code) from the official GitHub repository. The working folder should have the following structure:
```
morpheus_project/
├── data/                 # all time series as .json
│ ├── demand_el.json
│ ├── ...
│ └── cf_wind.json
├── MORPHE2US.xlsx        # Excel inputs (sheets define the model)
└── MORPHE2US_pipeline.py # python parser converting Excel + time series to Spine-readable .json
```

---

With the pre-requisites installed, you can now define your energy system model:

👉 [Model components](3_model_components.md)
