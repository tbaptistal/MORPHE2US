# Building a MORPHE2US Model

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

> 📌 You can start from a template provided by the MORPHE2US team.

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
├── input/
│ ├── morphe2us_input.xlsx
│ └── timeseries.json
└── output/
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
