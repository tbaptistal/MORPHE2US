# Building a Model

This guide walks you through the process of building a model using MORPHE2US — from preparing input data to generating a structured Spine-compatible database for optimization.

---

## 🧰 Step 1: Prepare Your Input Files

MORPHE2US requires two key input files:

### 1. Excel File (`.xlsx`)

This file defines:

- 💡 Technologies (names, efficiencies, costs, emissions)
- 🧱 Nodes and carriers (e.g., electricity, heat, gas)
- 📈 Demands and capacity limits
- 📆 Simulation timeline (years and time slices)
- 🌍 Geographical zones (if any)
- 📏 Constraints (e.g., emissions limits)

> 📌 You can start from a template which can be provided.

### 2. Time Series File (`.json`)

This file provides time-dependent data, such as:

- Electricity demand profiles
- Heat demand
- Wind capacity factors
- Solar irradiation
- Dynamic pricing (if applicable)

📁 **Organize your input files like this:**

```
morpheus_project/
├── data/
│ ├── heatdemand_timeserie.json
│ ├── ...
│ └── timeseries.json
└── MORPHE2US.xlsx
```

# JSON Data Structure

The `.json` file should follow this structure:

## Example: `example.json`

```json
[
    {
        "parameter_name": "unit_availability_factor",
        "commodity": null,
        "building": null,
        "district": "All",
        "unit": "Wind Turbine (onshore-3.3MW)",
        "connection": null,
        "quantitative": false,
        "data": {
            "data": [
                0.002,
                0.011,
                0.014
            ],
            "index": {
                "start": "2025-01-01T00:00:00",
                "repeat": false,
                "ignore_year": true,
                "resolution": "1h"
            },
            "type": "time_series"
        }
        // OR
        "data": {
            "index": {
                "repeat": false,
                "ignore_year": true
            },
            "data": {
                "2025-01-01T00:00:00": 0.001964,
                "2025-01-01T01:00:00": 0.001718
            },
            "type": "time_series"
        }
    },
    {
        "parameter_name": "fix_ratio_out_in_unit_flow(from_node1to_node1)",
        // Efficiency from electricity (input node 1) to hydrogen (output node 1)
        "commodity": null,
        "building": "All",
        "district": "All",
        "unit": "H2-SO Electrolyzer 1MW",
        "connection": null,
        "quantitative": false,
        "data": {
            "data": {
                "2020-01-01T00:00:00": 0.659685420459087,
                "2025-01-01T00:00:00": 0.673892756549928,
                "2030-01-01T00:00:00": 0.69585900160386,
                "2040-01-01T00:00:00": 0.705409007987765,
                "2050-01-01T00:00:00": 0.724649458131531
            },
            "type": "time_series"
        }
    },
    {
        "parameter_name": "demand",
        "commodity": "Electricity",
        "building": "SFH",
        "district": "Kreis1",
        "unit": null,
        "connection": null,
        "quantitative": true,
        "data": {
            "index": {
                "repeat": false,
                "ignore_year": true
            },
            "data": {
                ...
            },
            "type": "time_series"
        }
    }
]


```
---

## ⚙️ Step 2: Generate the Model

Use the MORPHE2US parser script to convert your input files into a SpineToolbox-compatible database.

### 🔧 Command

Run the following command from your project root:

```bash
python morpheus_pipeline/generate_spine_model.py \
    --excel input/morphe2us_input.xlsx \
    --timeseries input/timeseries.json \
    --output output/morphe2us_model.json
```

This script:

- ✅ Validates and parses the Excel/JSON files
- 🔁 Converts the structure into Spine-compatible format
- 🧱 Creates a .json database ready to be loaded into SpineToolbox
- 💡 You can re-run the parser any time you update your input files.

---

## 🧩 Step 3: Load the Model into SpineToolbox

Now that the .json database has been created, you can open it using SpineToolbox.

### 📝 Steps

- Launch SpineToolbox
- Create or open a MORPHE2US project
- Add the `morphe2us_model.json` as a SpineDB item
- Optionally open it in SpineInterface to browse its contents

---

## 🔍 Step 4: Verify and Validate

Before running the model, verify that:

- All technologies are correctly listed
- Time series match the required resolution (hourly, daily, etc.)
- Parameters like costs, efficiencies, emissions, and capacities are filled
- Scenarios and temporal layers (years and slices) are in place

Use the interface to browse:

- objects
- object_links
- parameters
- timeseries
- scenarios

---

## ✅ Step 5: Ready to Run

Your MORPHE2US model is now fully structured and loaded into SpineToolbox.

You can now proceed to the next step:

👉 [Running the Model](5_running_a_model.md)
