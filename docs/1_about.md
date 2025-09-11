# About

**MORPHE2US** stands for **Municipal Optimization for Renewable Projects in Hydrogen & Energy Efficient Utility Solutions**.

It is an Excel-based techno-economic modeling framework designed to support **municipalities** in identifying location-specific, cost-optimal pathways to decarbonize their energy systems.

## Purpose

MORPHE2US helps cities and regions explore **decarbonization pathways** by converting techno-economic data into optimization-ready inputs for [SpineOpt](https://github.com/Spine-project/SpineOpt.jl).
The tool provides a structured Excel interface that makes it possible to define technologies, demands, and system constraints, which are parsed via Python into `.json` files compatible with Spine Toolbox and SpineOpt.
providing an optimization-based approach to:

## Key Features

- ✅ **Flexible Technology Definition**: Include supply, conversion, and storage technologies  
- 🏘 **Spatial Flexibility**: Model municipalities with multiple districts and building archetypes  
- ⏱ **Temporal Resolution**: Support for single-year snapshots or multi-year transition pathways  
- 📦 **Infrastructure Options**: Represent both existing infrastructure (brownfield) and new investments (greenfield)  
- 💡 **Sector Coupling**: Gas, electricity, heat, and hydrogen in a single optimization
- 📚 **Community-Driven**: Active SpineOpt GitHub forum for bug reports, improvements, and knowledge sharing

## Architecture

The Excel model outputs a `.json` file that can be imported directly into a Spine database to run simulations using the open-source **SpineOpt** energy modeling framework. 
MORPHE2US consists of three main components:

1. **Excel Workbook**: User-friendly input interface for defining model specifications
2. **Python Pipeline**: Parses Excel and `.json` data into a model-ready format
3. **Spine Toolbox + SpineOpt**: Executes the optimization and visualizes results

## Where to go next


```{eval-rst}
.. mermaid::

   flowchart TD

       A[1–2: Collect techno-economic data<br/>(technologies, demands, costs, etc.)]

       B[3: Excel interface (MORPHE2US)<br/>Define commodities, units,<br/>storages, connections, etc.]

       C[4: Python parser (MORPHE2US_pipeline.py)<br/>Reads Excel + external time series (.json / .csv)<br/>→ outputs SpineOpt JSON]

       D[4: Spine Toolbox<br/>Import JSON, manage database]

       E[5: SpineOpt Optimization<br/>Solve model]

       F[6: Post-processing & results<br/>External visualization (Python/Excel,<br/>limited Spine GUI)]

       A --> B --> C --> D --> E --> F
```


1. **Getting Started** — install prerequisites and set up folders:  
   → [2_getting_started.md](2_getting_started.md)
2. **Model Components** — what each Excel sheet controls:  
   → [3_model_components.md](3_model_components.md)
3. **Building a Model** — take your filled Excel + `data/*.json`, run the parser, import `output.json`:  
   → [4_building_a_model.md](4_building_a_model.md)
4. **Running a Model** — select a solver in Spine Toolbox and execute SpineOpt:  
   → [5_running_a_model.md](5_running_a_model.md)
5. **Analyzing a Model** — inspect tables, export to CSV/Excel, external plotting:  
   → [6_analyzing_a_model.md](6_analyzing_a_model.md)

> Ready to jump in? Start at **[Building a Model](4_building_a_model.md)** if your Excel and JSON files are already prepared.