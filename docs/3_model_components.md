# Model Components

MORPHE2US uses an Excel workbook as the main interface. This workbook consists of eight different sheets, each one defining part of the model’s structure. 

## Quick navigation
- [Specifications](#specifications)
- [Commodities](#commodities)
- [Units](#units)
- [Storages](#storages)
- [Connections](#connections)
- [Building types](#building-types)
- [Districts](#districts)
- [Reports](#reports)
- [Time series preparation](#time-series-preparation)

**TODO:** are time series prepared/converted from excel/csv to .json? Expand defintions of each sheet

---

## Specifications
Define model scope and global switches.  
Typical: model start/end, operation mode (continuous vs. specific years), investment mode, CO₂ on/off, optional MGA settings.

---

## Commodities
Define energy carriers/nodes (e.g., Electricity, Heat, Gas, Hydrogen, CO₂).  
You can indicate whether surplus can be dumped (overflow) or if a commodity is bookkeeping-only.

---

## Units
Define technologies (supply, conversion, demand).  
Typical fields: input/output commodities, efficiencies, capacities, investment options, number of units.

---

## Storages
Define storage technologies (batteries, thermal tanks, etc.).  
Typical fields: energy capacity, charge/discharge power, efficiencies, losses, optional investment.

---

## Connections
Define networks (from → to) carrying a commodity (e.g., pipes, lines, inter-district links).  
Typical fields: endpoints, capacity/limits, optional investment.

---

## Building types
Define building archetypes (e.g., SFH, MFH, Office).  
May include simple retrofit options.

---

## Districts
Define spatial scope, building stock per district, and which units/storages are present at district and building levels.

---

## Reports
Choose which result tables to produce (e.g., flows, capacities, costs, emissions).  
These selections control what you can later view/export.

---

# Time series preparation

**Time series are not authored in Excel** — they live as `.json` files in `./data/` and are merged by the parser.

**TODO**: fill, considering that you start with csv/excel and how are they converted to .json? what do these files need to look like?

> 📌 **Recommendation:** Provide time series in `.json` format and fill all other data directly in the Excel file. The `.json` data should follow the format described [here](#json-input-data-structure). All `.json` files in the `morpheus_project/data` folder will be read by the Python parser and integrated into the model.


## JSON Input Data Structure

The `.json` file should follow this structure:
```json
[
    {
        "parameter_name": "unit_name",
        "commodity": "commodity_name",
        "building": "building_name", // or "All"
        "district": "district_name", // or "All"
        "unit": "unit_name",
        "connection": "connection_name",
        "quantitative": false, // true if the values need to be multiplicated. Ex: heat demand for 1 building while there are 12 buildings in the district so times 12.
        "data": {
            "data": [
                0.002,
                0.011,
                0.014
            ],
            "index": {
                "start": "yyyy-mm-ddThh:mm:ss",
                "repeat": false, // Or true if it's cyclic
                "ignore_year": true, // ignore the yyyy in the data
                "resolution": "1h" // h for hours, D for days, M for months and Y for years
            },
            "type": "time_series" 
        }
    }
]
```        

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
Once the model has been defined using the Excel template, you can prepare it for Spine:

👉 [Building a Model](4_building_a_model.md)