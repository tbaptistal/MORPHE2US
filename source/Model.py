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

    def export_json(self, data: dict):
        data = add_entity(data, "temporal_block", self.name)
        for key, values in self.direct_parameters.items():
            # NaM: Not a model (not usable directly in SpineOpt)
            # "(" refers that the code of the parameter has a specific meaning, here in the method link_nodes
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "temporal_block", self.name, key, values["value"], values["type"])

        if self.is_investment:
            data = add_entity(data, f"model__default_investment_temporal_block", [self.model_name, self.name])
        else: 
            data = add_entity(data, f"model__default_temporal_block", [self.model_name, self.name])
        return data
    

@dataclass
class Report:
    name: str
    output_list: List[str] = field(default_factory=list)
    model_name: str = "model"

    def add_output(self, output: str):
        self.output_list.append(output)

    def set_model_name(self, model_name: str):
        self.model_name = model_name

    def export_json(self, data: dict) -> dict:
        data = add_entity(data, "report", self.name)
        data = add_entity(data, "model__report", [self.model_name, self.name])
        for output in self.output_list:
            data = add_entity(data, "report__output", [self.name, output])
        return data
    
    def get_output_list_length(self):
        return len(self.output_list)

@dataclass
class Stochastic_Scenario:
    name: str
    name_stochastic_structure: str = ""

    def set_name(self, name):
        self.name = name

    def set_name_stochastic_structure(self, name_stochastic_structure):
        self.name_stochastic_structure = name_stochastic_structure

    def export_json(self, data: dict) -> dict:
        data = add_entity(data, "stochastic_scenario", self.name)
        data = add_entity(data, "stochastic_structure__stochastic_scenario", [self.name_stochastic_structure, self.name])
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
        super().__init__("model")

    def export_json(self, data: dict):
        data = add_entity(data, "model", self.name)

        data = add_entity(data, "stochastic_structure", self.name_stochastic_structure)
        data = add_entity(data, "model__default_stochastic_structure", [self.name, self.name_stochastic_structure])
        # If at least one investment is defined, we add the default investment structure
        if len(self.investments) > 0:
            data = add_entity(data, "model__default_investment_stochastic_structure", [self.name, self.name_stochastic_structure])

        
        for key, values in self.direct_parameters.items():
            # NaM: Not a model (not usable directly in SpineOpt)
            # "(" refers that the code of the parameter has a specific meaning, here in the method link_nodes
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "model", self.name, key, values["value"], values["type"])

        for item in chain(self.modelisation_structures, self.operations, self.investments, self.reports, self.stochastic_scenarios):
            data = item.export_json(data)
        return data

    
    def add_modelisation_structure(self, modelisation_structure):
        self.modelisation_structures.append(modelisation_structure)

    def add_operation(self, operation):
        operation.set_model_name(self.name)
        self.operations.append(operation)

    def add_report(self, report):
        report.set_model_name(self.name)
        self.reports.append(report)
    
    def add_investment(self, investment):
        investment.set_model_name(self.name)
        investment.set_investment(True)
        self.investments.append(investment)

    def add_stochastic_scenario(self, stochastic_scenario):
        stochastic_scenario.set_name_stochastic_structure(self.name_stochastic_structure)
        self.stochastic_scenarios.append(stochastic_scenario)
        

    def update_scenario_structure(self):
        if "NaM_scenario_name" in self.direct_parameters:
            self.add_stochastic_scenario(Stochastic_Scenario(self.direct_parameters["NaM_scenario_name"]["value"]))
        else:
            self.add_stochastic_scenario(Stochastic_Scenario("default_scenario"))

        if "NaM_bool_multiple_scenarios" in self.direct_parameters:
            if self.direct_parameters["NaM_bool_multiple_scenarios"]["value"]:
                if "NaM_add_scenarios" in self.direct_parameters:
                    for scenario in self.direct_parameters["NaM_add_scenarios"]["value"].split(";"):
                        self.add_stochastic_scenario(Stochastic_Scenario(scenario.replace(' ', '')))