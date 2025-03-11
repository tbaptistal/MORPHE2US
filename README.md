# **MORPHE2US User Guide**  

## **Table of Contents**  
- [Introduction](#introduction)  
  - [System Requirements](#system-requirements)  
  - [System Overview](#system-overview)
- [Types of inputs](#types-of-inputs)
- [MORPHE2US Excel file](#morphe2us-excel-file)
  - [Specifications](#specifications)
  - [Commodities](#commodities)
  - [Units](#units)
  - [Storages](#storages)
  - [Connections](#connections)
  - [Building types](#building-types)
  - [Districts](#district)
  - [Reports](#report)
- [Key Features](#key-features)  
- [Using MORPHE2US](#using-morphe2us)  

---

## **Introduction**  
Welcome to **MORPHE2US**, a powerful and intuitive techno-economic model designed to *inform and help municipalities in their energy investments to reach net 0 by 2050*. The model's main goal is to follow the 7th Sustainable Development Goal from United Nations: **“affordable, reliable, sustainable and modern energy for all”**

This guide will help you set up, navigate, and maximize your use of MORPHE2US.  

MORPHE2US - **Municipal Optimization for Renewable Project in Hydrogen & Energy Efficient Utility Solutions** - is an Excel table coupled with a Python script that automatically generates a **SpineOpt** model in the **SpineToolBox**.  

---

### **System Requirements**  
Before installing MORPHE2US, ensure your system meets the following requirements: 

- **Operating System:** *No specifications*  
- **Processor:** *Could specify the computation time with the processor type*  
- **RAM:** *Could specify the computation time with the RAM size*   
- **SpineOpt:** *Required*
- **SpineToolBox:** *Required*  

---

### **System Overview**  
MORPHE2US consists of the following core components:  

- **Excel sheet:** Provides an overview of the municipality to model.  
- **Python pipeline:** Python code that will *translate* the model in the Excel sheet and the input datas coming from a .json file into a workable SpineToolBox file.  


---

## Types of Inputs
Each input field in the Excel sheet will have a specified **type**. Below are the types you may encounter:

- **`string`**: A sequence of characters.
- **`strings`**: A list of strings. Example: `Scenario1; Scenario2` (*Spacing doesn't matter; `;` is the delimiter*).
- **`date_time`**: A date in the format: `dd.mm.yyyy hh:mm`.
- **`float`**: A number (decimal values allowed).
- **`ints`**: A list of integers. Example: `2025; 2030; 2035` (*Spacing doesn't matter; `;` is the delimiter*).
- **`bool`**: A `TRUE` or `FALSE` value. A checkbox should already appear in Excel.
- **`duration`**: A time duration in the format `xX`, where:
  - `x` is an integer.
  - `X` is one of: `s` (seconds), `m` (minutes), `h` (hours), `D` (days), `M` (months), `Y` (years).  
  - Example: `10Y` (10 years).
- **`timeseries`**: A time series can be entered directly in Excel (not recommended). Instead, we suggest using the `.json` parser.  
  If entered in Excel, use this format:  
  `2020=15000; 2025=10000`  
  → This translates to SpineOpt as:  
  - `2020-01-01 00:00:00 → 15000`
  - `2025-01-01 00:00:00 → 10000`

--- 
## MORPHE2US Excel file
This guide explains the **Excel component** of MORPHE2US and how to correctly input data.
## Specifications

### General
- **`Name`***(string - opt)*
  The name of the block in the SpineOpt model.
- **`Start of simulation`***(datetime)*
  The start date of the simulation.
- **`End of simulation`***(datetime)*
  The end date of the simulation.

#### Economic Parameters
- **`Discount Rate`** *(float / Map)*
  The discount rate applied to all components in the simulation.  
  *(Specific technology discount rates can be set in `Unit`, `Connection`, or `Storage`.)*
- **`Discount Year of Reference`** *(datetime / Map)*
  The year to which all cash flows are discounted.
- **`Economic Representation`** *(bool / Map)*
  If `TRUE`, multi-year investments will be modeled considering discount rates.
- **`Milestone Years`** *(bool / Map)*
  If `TRUE`, operational blocks for a milestone year are scaled up to represent the full investment period.

#### Scenario Setup
- **`Base Scenario name`** *(string - opt)*
  The base scenario block name in SpineOpt.
- **`Multiple Scenarios`** *(bool)*
  Enables multiple scenario blocks, using the **Map** format (see *Types of Inputs*).  
  Must be used with `Additional Scenario names`.
- **`Additional Scenario names`** *(strings)*
  List of additional scenario names to be computed in SpineOpt.

### Operation
**`Linear operation`** and **`Multi Specific year operation`** are mutually exclusive.  
If both are `TRUE`, **`Linear operation`** takes priority.

#### Linear Operation
- **`Linear operation`** *(bool)*
  If `TRUE`, the model runs from **`Start of simulation`** to **`End of simulation`** using the specified `Resolution`.
- **`Name`** *(string - opt)*
  Optional name of the operation block in SpineOpt.
- **`Resolution`** *(duration / Map)*
  Defines the resolution of the linear operation.

#### Multi Specific Year Operation
- **`Multi Specific year operation`** *(bool)*
  If `TRUE`, the model simulates specific years within the **simulation period**.  
  _(Not recommended for seasonal storage modeling.)_
- **`Name`** *(string - opt)*
  Optional name of the operation block in SpineOpt.
- **`Resolution`** *(duration / Map)*
  Common resolution for all operational blocks.
- **`Specific years to simulate`** *(ints / Map)*
  List of years to be simulated.

#### Representative Days *(Future Development)*
- **`Representative days (opt)`** *(bool)*
  Enables representative days. *(Currently unavailable, but planned in future SpineOpt versions.)*

### Economic - Investments
MORPHE2US supports **two types of investment models**:
1. **Single-Time Investment** - Happens once at a user-specified date.
2. **Multi-Year Investment** - Repeats periodically from a start date.

#### Single-Time Investment
- **`Single time`** *(bool)*
  Enables single-time investment.
- **`Name`***(string - opt)*
  Optional name of the investment block in SpineOpt.
- **`Occurrence date`** *(date_time / Map)*
  Date of the investment.

#### Multi-Year Investment
- **`Multi year`** *(bool)*
  Enables multi-year investment.
- **`Name`***(string - opt)*
  Optional name of the investment block in SpineOpt.
- **`1st occurrence date`** *(date_time / Map)*
  Date of the first investment occurrence.
- **`Horizon of occurrences`** *(duration / Map)*
  Time interval between investment cycles.

### CO2 Management
- **`CO2 node`** *(bool)*
  If `TRUE`, enables CO2 quantification in the municipality.
- **`Maximum total CO2 emissions`** *(float / timeseries / Map - opt)*
  Defines the maximum CO2 emissions over the entire simulation.  
  _(Can be more complex if using a `Map` or `timeseries` in `.json`.)_
- **`Maximal emissions (over 1 unit of simulation time)`** *(float / timeseries / Map - opt)*
Defines the max CO2 emissions per timestep. It allows the user to set an upper boundary, e.g., `500kg/hour` of CO2.

### Examples: 
Build here examples with values that would make sense for the simulation in a table.

---

## Commodities
Commodities such as gas, electricity, hot water, space heating, hydrogen, water, heating oil, wood, wood pellet, or any other commodities are to be declared in the  **Excel sheet Commodities**.
The **`name`** of the commidity has to be declared as general. Each commodity will have nodes at building and district level. These nodes could be interconnected thanks to a **Connection** (see **Excel sheet Connections**).
2 other parameters are to be specified: 
**`Allow commodity overflow (lost cost)`**
It will creates **Overflow unit** that allow overflow of the commodity to flow outside of the model. All of the overflow is then quantified in the **Overflow unit** and can be seen in the results panel.
**`Supply node (with an infinite capacity of import)`**
A supply node with infinite capacity of import/export will act as a node with unlimited capacity of such commodity. 
Example: Gas isn't a supply node as we have to model a gas network (same for electricity). Concerning wood or heating oil, we can model them as supply node. It means that there is no network (to manage and/or simulate). A building-level unit that will consume such commodity and produce heat will just pump the commodity in the same building level supply node.

### Linking connections
After declaring the connections in the **Excel sheet Connections**, you can instantiate a specific number of connections (existing or to be available for investment) in the same **Excel sheet Commodities**.
The declaration of a new connection is as follow:
#### General
Connection from district-level to district-level and from district-level to building-level are available.

**`Connection's name`**
The name of the connections which is defined directly in the **Excel sheet Connections**. If not, then check in the Data Validation from Excel if the name of the connection is correctly linked.

**`Number of connections`**
The initial quantity of connection already in used.
**`Candidate connections`**
The quantity of connections in which the model is allowed to invest.
#### From node
**`District level`**
From which district the connection is coming from.
**`Building level`**
From which building the connection is coming from. 
If not specified, then the connection is starting from the district directly at district level.
"All" can be written as argument of this parameter. It allows to link all the building of a district to a district level. The code will generate 1 entity of connection for each type of building going to the district level.
**`Capacity`**
The maximum capacity for 1 connection. 
**`Flow Cost`**
The flow cost for 1 connection (CHF/kWh or any other currency or unit flow used in the model)
#### To node
**`District level`**
To which district the connection is going to.
**`Building level`**
To which building the connection is going to. 
If not specified, then the connection is finishing in the district directly at district level.
"All" can be written as argument of this parameter. It allows to link all the building of a district to a district level. The code will generate 1 entity of connection for each type of building going to the district level.
**`Capacity`**
See 'Capacity' definition above for reference.
**`Flow Cost`**
See 'Flow Cost' definition above for reference.

---

## Units
Defining a unit in the **Excel sheet** does not automatically include it in the model.  
Each unit must be assigned to a **District** or a **Building** to be included.

### General
- **`Name`** *(string)*
Naming convention:
*Building Level:* `Name` + `district_name` + `B-LVL` + `building_name`
*District Level:* `Name` + `D-LVL` + `district_name`
- **`Input commodity x`** *(Excel Data Validation)*
_Each unit can consume up to 3 commodities._
- **`Output commodity x`** *(Excel Data Validation)*
_Each unit can generate up to 3 commodities._
- **`District / Building scale`** *(Excel Data Validation)*
_Specifies whether the unit operates at district or building scale._
- **`CO2 production`** *(float - optional)*
_Quantity of CO2 produced (positive value) or consumed (negative value) with Input commodity 1 as reference._
- **`Fixed yearly operation/maintenance costs`** *(float - optional)*
_Yearly OPEX per kW installed._
- **`Fixed hourly operation/maintenance costs (SpineOpt)`** *(automatic calculation)*
_SpineOpt requires hourly OPEX, which Excel calculates automatically._

---

### Investments
Some parameters are **optional**. If a unit is not intended for investment, these fields can be left blank.

- **`Investment Cost per kW`** *(float - optional)*
- **`Investment Cost`** *(automatic OR float)*
- **`Economic lifetime`** *(duration)*
- **`Technical lifetime`** *(duration)*
- **`Investment type`** *(Excel Data Validation: Integer/Continuous)*
_"Continuous" is recommended for better computation performance._
- **`Investment type (SpineOpt)`** *(automatic calculation)*
- **`Discount rate (technology specific)`** *(float - optional)*
- **`Decommissioning cost`** *(float - optional)*
- **`Decommissioning time`** *(duration - optional)*
- **`Lead time`** *(duration - optional)*
_Time required to commission the unit._

---

### Efficiencies  
Efficiency from **input commodity** to **output commodity**:

- **`Efficiency x → y`** *(float/array)*
_Defines efficiency. Can be set as an array for operating points._

---

### Capacities
- **`Capacity INPUT x`** *(float)*
_Defines input capacity._
- **`Capacity OUTPUT y`** *(float)*
_Defines output capacity._

---

### Advanced Parameters (Optional)
These parameters **fine-tune** unit operation.

#### Costs
- **`Start-up cost`** *(float)*
_Cost incurred each time the unit starts up._
- **`Shutdown cost`** *(float)*
_Cost incurred each time the unit shuts down._
- **`Variable fuel costs INPUT x`** *(float)*
- **`Variable fuel costs OUTPUT y`** *(float)*
- **`Variable operating costs of INPUT x`** *(float)*
- **`Variable operating costs of OUTPUT y`** *(float)*
- **`Procurement cost for reserves`** *(float - not implemented yet)*

#### Time Constraints
- **`Minimum up time`** *(duration)*
_Minimum time the unit must stay ON._
- **`Minimum down time`** *(duration)*
_Minimum time the unit must stay OFF._
- **`Ramp up limit OUTPUT y`** *(float)*
- **`Ramp down limit OUTPUT y`** *(float)*

#### Flow Constraints
- **`Maximal cumulated unit flow from INPUT x`** *(float)*
- **`Maximal cumulated unit flow to OUTPUT y`** *(float)*
- **`Minimal cumulated unit flow from INPUT x`** *(float)*
- **`Minimal cumulated unit flow to OUTPUT y`** *(float)*

#### Ramping
- **`Maximum ramp-down of INPUT x`** *(float)*
- **`Maximum ramp-down of OUTPUT y`** *(float)*
- **`Maximum ramp up of INPUT x`** *(float)*
- **`Maximum ramp-up of OUTPUT y`** *(float)*
---

## Storages
Defining a storage in the **Excel sheet** does not automatically include it in the model.  
Each storage must be assigned to a **District** or a **Building** to be included.

In SpineOpt, a storage is modeled as both a **node** and a **unit**.  
Storages can **only store one commodity at a time**.

---

### General
- **`Name`** *(string)*
_Naming convention:_  
  *Building Level:* `Name` + `district_name` + `B-LVL` + `building_name`  
  *District Level:* `Name` + `D-LVL` + `district_name`
- **`Commodity`** *(Excel Data Validation)*
_Specifies the commodity stored._  
- **`District / Building scale`** *(Excel Data Validation)*
_Specifies whether the storage operates at district or building scale._  
- **`Capacity`** *(float)*
_Maximum storage capacity._  
- **`Efficiency to storage`** *(float)*
_Efficiency when storing the commodity._  
- **`Efficiency from storage`** *(float)*
_Efficiency when retrieving the commodity._  
- **`Self-discharge`** *(float - optional)*
_Represents storage losses over time._  
- **`Initial storage level`** *(float - optional)*
_Defines the initial stored quantity._  
- **`Fixed yearly operation/maintenance costs`** *(float - optional)*
_Yearly OPEX per unit of capacity._  
- **`Fixed hourly operation/maintenance costs (SpineOpt)`** *(automatic calculation)*
_SpineOpt requires hourly OPEX, which Excel calculates automatically._  

---

### Rating Power
- **`Capacity INPUT`** *(float)*
_Defines the maximum charge rate._  
- **`Capacity OUTPUT`** *(float)*
_Defines the maximum discharge rate._  

---

### Investments
Some parameters are **optional**. If a storage is not intended for investment, these fields can be left blank.

- **`Investment Cost per kWh`** *(float - optional)*
- **`Investment Cost`** *(automatic OR float)*
- **`Economic lifetime`** *(duration)*
- **`Technical lifetime`** *(duration)*
- **`Investment type`** *(Excel Data Validation: Integer/Continuous)*
_"Continuous" is recommended for better computation performance._  
- **`Investment type (SpineOpt)`** *(automatic calculation)*
- **`Discount rate (technology specific)`** *(float - optional)*
- **`Decommissioning cost`** *(float - optional)*
- **`Decommissioning time`** *(duration - optional)*
- **`Lead time`** *(duration - optional)*
_Time required to commission the storage._  

---

### Advanced Parameters (Optional)
These parameters **fine-tune** storage operation.

#### Costs
- **`Start-up cost`** *(float - optional)*
_Cost incurred each time the storage starts charging._  
- **`Shutdown cost`** *(float - optional)*
_Cost incurred each time the storage stops discharging._  

#### Time Constraints
- **`Minimum up time`** *(duration - optional)*
_Minimum time the storage must stay active._  
- **`Minimum down time`** *(duration - optional)*
_Minimum time the storage must stay inactive._  

#### Ramping
- **`Ramp up limit (INPUT)`** *(float - optional)*
- **`Ramp down limit (INPUT)`** *(float - optional)*
- **`Ramp up limit (OUTPUT)`** *(float - optional)*
- **`Ramp down limit (OUTPUT)`** *(float - optional)*

## Connections
Defining a connection in the **Connection Excel sheet** does not automatically include it in the model.  
Each connection must be assigned in the **Commodities sheet**.

Connections represent the transfer of a **commodity** between different locations or components in the model. 

---

### General
- **`Name`** *(string)*
_Report here the naming convention for connection_  
- **`Commodity`** *(Excel Data Validation)*
_Specifies the commodity being transferred._  
- **`Type`** *(Excel Data Validation)*
_Defines the type of connection (e.g., Lossless Bidirectional,	normal)._  
- **`Efficiency`** *(float)*
_Represents losses or conversion factors during transfer._  
- **`Length (not used in the model)`**
The total length of the connection. Parameter not used in the model. 


---

### Investments
Some parameters are **optional**. If a connection is not intended for investment, these fields can be left blank.

- **`Investment Cost per unit length`** *(float - optional)*
Could be used to define **`Investment Cost`** automatically using a formula with the **`length`** parameter.
- **`Investment Cost`** *(automatic OR float)*
- **`Economic lifetime`** *(duration)*
- **`Technical lifetime`** *(duration)*
- **`Investment type`** *(Excel Data Validation: Integer/Continuous)*
_"Continuous" is recommended for better computation performance._  
- **`Discount rate (technology specific)`** *(float - optional)*
- **`Decommissioning cost`** *(float - optional)*
- **`Decommissioning time`** *(duration - optional)*
- **`Lead time`** *(duration - optional)*
_Time required to commission the connection._  


## Building types
Building type are registered in the **Building Excel sheet** using:
- **`name`**
- **`type`**
- **`date of construction`**

Only the name is used as a reference to this building type in the model. Load shapes (timeseries) are to be registered directly in the .json according to the aforementioned format.
The pre-existing utilities for the specific building (heating system, rooftop pv...) are to be specified in the **District Excel sheet**.

### Retrofits
**Demand timeseries** can't be modified directly in SpineOpt if the model invested in retrofit. To pass through this, retrofit are done using **connection entities** 

- **`Name`**
Name of the retrofit. The naming convention is ... 
- **`Commodity`**
The commodity in which the retrofit is acting.
- **`Decrease in consumption [%]`**
The decrease in consumption. Example: Smart lighting would reduce by 8% of total electricity demand. Led would reduce by 4%. All smart appliances would reduce by 12%.
- **`Price for 1 building [CHF]`**
WARNING
WARNING
WARNING
Should check again if that's true. WARNING
WARNING
WARNING
WARNING

## District
District are defined in the **District Excel sheet**. This sheet (and the **Commodities Excel sheet**) are the ones which should be updated for each new municipalities. The other **Excel sheets (units, storages, connections, Specifications and Report)** are general sheet and are just defining general components. The **Building type Excel sheet** could be adapted to each municipality but could also be re-used at the user's preferences.

First, each district which should be incorporated within the model has to be named.
Then, for each district, the **`Quantity of building`** from the **`Building types`** are to be specified. It will determine the load demand for each node at district level (all building with the same building type at a district level are aggregated).

The user has then to fill all of the tables: 
- _**`Units presence (district level)`**_
- _**`Units presence (building level)`**_
- _**`Storages presence (district level)`**_
- _**`Storages presence (building level)`**_

Each unit/storage should appear directly in the good category according to whether it's available in building or in district level. 
Each unit/storage should be filled with **`number of units`** and **`candidate units`** (blue zone). If a unit/storage isn't filled (or with both 0 for **`number of units`** and **`candidate units`**), then the unit/storage won't appear in the model for the specified building type in the specified district (building level) or specified district (district level).


## Report
Report can be created in the **Report Excel sheet**. Outputs can be assigned to a specific report. Each output are already generated by the template from SpineOpt within the SpineToolBox.


---

## **Key Features**  
- **Feature 1:** *[Brief description & add an image to illustrate]*  
- **Feature 2:** *[Brief description & add an image to illustrate]*  
- **Feature 3:** *[Brief description & add an image to illustrate]*  
- **Feature 4:** *[Brief description & add an image to illustrate]*

---


## **Using MORPHE2US**
... 
### **Creating a New Project**
#### **Creating a New Municipality**
... 
#### **Creating a New Scenario with the same Municipality**
... 

### **Saving & Exporting**
... 

### Debugging the python pipeline
... 