from source.helpers.filling_json_functions import add_entity, add_parameter_value
from source.Entity import Entity
from dataclasses import dataclass, field
from typing import List
from itertools import chain

@dataclass
class Temporal_block(Entity):
    is_investment: bool = False
    model_name: str = "model"

    def __init__(self):
        super().__init__()

    def set_investment(self, is_investment):
        self.is_investment = is_investment

    def set_model_name(self, model_name):
        self.model_name = model_name

    def export_json(self, data: dict, scenario_name: str):
        # Add the temporal block entity to the JSON data
        data = add_entity(data, "temporal_block", self.name, scenario_name)
        for key, values in self.direct_parameters.items():
            # Exclude parameters that are not directly usable in the model (e.g., marked with "NaM" or containing "(")
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "temporal_block", self.name, key, values["value"], values["type"], scenario_name)

        # Add the temporal block to the appropriate model structure based on whether it's an investment
        if self.is_investment:
            data = add_entity(data, f"model__default_investment_temporal_block", [self.model_name, self.name], scenario_name)
        else: 
            data = add_entity(data, f"model__default_temporal_block", [self.model_name, self.name], scenario_name)
        return data
    

@dataclass
class Report:
    name: str
    output_list: List[str] = field(default_factory=list)
    model_name: str = "model"

    def add_output(self, output: str):
        # Add an output to the report's output list
        self.output_list.append(output)

    def set_model_name(self, model_name: str):
        # Set the model name associated with the report
        self.model_name = model_name

    def export_json(self, data: dict, scenario_name: str) -> dict:
        # Add the report entity to the JSON data
        data = add_entity(data, "report", self.name, scenario_name)
        # Link the report to the model
        data = add_entity(data, "model__report", [self.model_name, self.name], scenario_name)
        # Link each output to the report
        for output in self.output_list:
            data = add_entity(data, "report__output", [self.name, output], scenario_name)
        return data
    
    def get_output_list_length(self):
        # Get the number of outputs in the report
        return len(self.output_list)

@dataclass
class Stochastic_Scenario:
    name: str
    name_stochastic_structure: str = ""

    def set_name(self, name):
        # Set the name of the stochastic scenario
        self.name = name

    def set_name_stochastic_structure(self, name_stochastic_structure):
        # Set the name of the stochastic structure associated with the scenario
        self.name_stochastic_structure = name_stochastic_structure

    def export_json(self, data: dict, scenario_name: str):
        # Add the stochastic scenario entity to the JSON data
        data = add_entity(data, "stochastic_scenario", self.name, scenario_name)
        # Link the stochastic scenario to its structure
        data = add_entity(data, "stochastic_structure__stochastic_scenario", [self.name_stochastic_structure, self.name], scenario_name)
        return data



@dataclass
class Model(Entity):
    operations: List = field(default_factory=list)
    investments: List = field(default_factory=list)
    modelisation_structures: List = field(default_factory=list)
    reports: List = field(default_factory=list)
    stochastic_scenarios: List = field(default_factory=list)
    name_stochastic_structure: str = "default_structure"

    def __post_init__(self):
        # Initialize the model entity with the name "model"
        super().__init__("model")

    def export_json(self, data: dict, scenario_name: str):
        # Add the model entity to the JSON data
        data = add_entity(data, "model", self.name, scenario_name)

        # Add the stochastic structure and link it to the model
        data = add_entity(data, "stochastic_structure", self.name_stochastic_structure, scenario_name)
        data = add_entity(data, "model__default_stochastic_structure", [self.name, self.name_stochastic_structure], scenario_name)
        # If there are investments, link the default investment structure to the model
        if len(self.investments) > 0:
            data = add_entity(data, "model__default_investment_stochastic_structure", [self.name, self.name_stochastic_structure], scenario_name)

        for key, values in self.direct_parameters.items():
            # Exclude parameters that are not directly usable in the model (e.g., marked with "NaM" or containing "(")
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "model", self.name, key, values["value"], values["type"], scenario_name)

        # Export JSON for all associated entities (operations, investments, etc.)
        for item in chain(self.modelisation_structures, self.operations, self.investments, self.reports, self.stochastic_scenarios):
            data = item.export_json(data, scenario_name)
        return data

    
    def add_modelisation_structure(self, modelisation_structure):
        # Add a modelisation structure to the model
        self.modelisation_structures.append(modelisation_structure)

    def add_operation(self, operation):
        # Set the model name for the operation and add it to the model
        operation.set_model_name(self.name)
        self.operations.append(operation)

    def add_report(self, report):
        # Set the model name for the report and add it to the model
        report.set_model_name(self.name)
        self.reports.append(report)
    
    def add_investment(self, investment):
        # Set the model name and investment flag for the investment, then add it to the model
        investment.set_model_name(self.name)
        investment.set_investment(True)
        self.investments.append(investment)

    def add_stochastic_scenario(self, stochastic_scenario):
        # Set the stochastic structure name for the scenario and add it to the model
        stochastic_scenario.set_name_stochastic_structure(self.name_stochastic_structure)
        self.stochastic_scenarios.append(stochastic_scenario)
        

    def update_scenario_structure(self, scenario_name: str):
        self.add_stochastic_scenario(Stochastic_Scenario(scenario_name))
