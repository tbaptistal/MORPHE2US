# Workflow Overview

The MORPHE2US model follows a clear pipeline from user input to optimization results. Below is a high-level flowchart that illustrates the modeling process.

📊 **Workflow Steps**

*Excel Input + JSON Time Series*
Users define their scenario, technology assumptions, and demand profiles using:
    - Excel files (tech specs, scenario design, project info)
    - .json time series files (for hourly/daily demand and generation)

*Python Parser (`morpheus_pipeline`)*
A Python script parses and validates the input data, then converts it to a Spine-compatible format.

*Spine-readable Database (.json)*
The converted .json file is imported into SpineToolbox.

*Spinetoolbox + SpineOpt*
The core optimization is performed using SpineOpt

*Results*
Energy balances, emissions, costs, and technology uptake —
all visualizable via SpineToolbox or exported externally.


| **Excel + .json inputs**       |
|:------------------------------:|
| ↓                              |
| **Python Parser**              |
| ↓             |
| **Spine-readable Database (.json)**    |
| ↓                              |
| **Spinetool Box**              |
| ↓ *(SpineOpt)* |
| **Results**                    |
