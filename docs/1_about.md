# About

**MORPHE2US** stands for **Municipal Optimization for Renewable Projects in Hydrogen & Energy Efficient Utility Solutions**.

It is a powerful, Excel-based techno-economic modeling framework designed to support **municipalities** in making **sustainable, cost-effective energy investment decisions**. The model is built around the key principles of the **UN Sustainable Development Goal 7**:  
> *"Ensure access to affordable, reliable, sustainable and modern energy for all."*

## Purpose

MORPHE2US helps cities and regions plan for a **net-zero future by 2050** by providing an optimization-based approach to:

- Assessing renewable energy and storage technologies
- Modeling current and future energy demand
- Planning infrastructure investments across buildings and districts
- Managing CO₂ emissions over time

## Key Features

- ✅ **Integration of Renewable Energy Sources**: Model PV, heat pumps, wind, biomass, geothermal, etc.
- 🧩 **Technology Competition**: Simulate competing investment options (e.g. storage, connections, retrofits)
- 🏘 **Decentralized Energy Management**: Model DERs (rooftop solar, batteries, heat pumps, etc.)
- 🗓 **Multi-Year Optimization**: Plan long-term energy transitions over decades to reach global goals such as net-0 CO2 by 2050.
- 🏗 **Scalable**: From single buildings to entire districts or municipalities
- 💡 **Sector Coupling**: Gas, electricity, heat, and hydrogen in a single optimization
- 📚 **Community-Driven**: Active SpineOpt GitHub forum for bug reports, improvements, and knowledge sharing

## Architecture

The excel model outputs a `.json` file that can be imported directly into a Spine database to run simulations using the open-source **SpineOpt** energy modeling framework. 
MORPHE2US consists of three main components:

1. **Excel Workbook**: User-friendly input interface for defining model specifications
2. **Python Pipeline**: Parses Excel and `.json` data into a model-ready format
3. **SpineToolBox + SpineOpt**: Executes the optimization and visualizes results