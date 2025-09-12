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


```{mermaid}
flowchart TD
    A[Techno-economic inputs: <br> Prepare technologies, demands, costs, etc...]
    A --> B[Excel Interface:  <br> Define commodities, units, storages, connections, etc...]
    B --> C[Python parser: <br> Reads Excel + external time series JSON/CSV <br> -> Outputs SpineOpt JSON]
    C --> D[Spine Toolbox: <br> Import JSON <br> Manage database]
    D --> E[SpineOpt Optimization: <br> Solves model]
    E --> F[Results & external visualization: <br> Python/Excel, limited Spine GUI]
  
```

**TODO**: shift workflow here and align with steps (input prep in 3, python parser/spine toolbox/optimization in 4, model running in 5, post-processing in 6, rest is here) +----------------------------------+ | Collect techno-economic data | | (technologies, demands, etc.) | +----------------------------------+ | v +----------------------------------+ | Excel interface (MORPHE2US) | | Define commodities, units, | | storages, connections, etc. | +----------------------------------+ | v +----------------------------------+ | Python parser | | (MORPHE2US_pipeline.py) | | Reads Excel + external time | | series (.json / .csv) | | → outputs SpineOpt JSON | +----------------------------------+ | v +----------------------------------+ | Spine Toolbox | | Import JSON, manage database | +----------------------------------+ | v +----------------------------------+ | SpineOpt Optimization | | Solve model | +----------------------------------+ | v +----------------------------------+ | Results & external visualization| | (Python/Excel, limited Spine GUI)| +----------------------------------+


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