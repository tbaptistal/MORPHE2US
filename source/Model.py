from source.helpers.filling_json_functions import add_entity, add_parameter_value
from source.Entity import Entity
from dataclasses import dataclass, field
from typing import List



class Temporal_block(Entity):
    def __init__(self):
        super().__init__()

    def export_json(self, data: dict, model_name, investment_link = ""):
        data = add_entity(data, "temporal_block", self.name)
        for key, values in self.direct_parameters.items():
            # NaM: Not a model (not usable directly in SpineOpt)
            # "(" refers that the code of the parameter has a specific meaning, here in the method link_nodes
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "temporal_block", self.name, key, values["value"], values["type"])
        data = add_entity(data, f"model__default_{investment_link}temporal_block", [model_name, self.name])
        return data
        
@dataclass
class Model(Entity):
    operation_list: List = field(default_factory=list)
    investment_list: List = field(default_factory=list)
    modelisation_structure: List = field(default_factory=list)
    report_list: List = field(default_factory=list)

    def __post_init__(self):
        super().__init__("model")

    def add_modelisation_structure(self, modelisation_structure):
        self.modelisation_structure.append(modelisation_structure)

    def export_json(self, data: dict):
        for modelisation_structure in self.modelisation_structure:
            data = modelisation_structure.export_json(data)
            
        for report in self.report_list:
            data = report.export_json(data)
            data = add_entity(data, "model__report", [self.name, report.name])
        data = add_entity(data, "model", self.name)
        data = self.add_stochastic_scenario_json(data, "default_scenario", "default_structure")
        data = self.add_operations_json(data)
        data = self.add_investment_json(data)
        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "model", self.name, key, values["value"], values["type"])
        return data
    
    def add_stochastic_scenario_json(self, data, name_scenario, name_structure):
        data = add_entity(data, "stochastic_scenario", name_scenario)
        data = add_entity(data, "stochastic_structure", name_structure)
        data = add_entity(data, "model__default_stochastic_structure", [self.name, name_structure])
        data = add_entity(data, "stochastic_structure__stochastic_scenario", [name_structure, name_scenario])
        if len(self.investment_list) > 0:
            data = add_entity(data, "model__default_investment_stochastic_structure", [self.name, name_structure])
        return data
    
    def add_operation(self, operation):
        self.operation_list.append(operation)

    def add_report(self, report):
        self.report_list.append(report)

    def add_operations_json(self, data):
        for operation in self.operation_list:
            data = operation.export_json(data, self.name)
        return data
    
    def add_investment_json(self, data):
        for investment in self.investment_list:
            data = investment.export_json(data, self.name, "investment_")
        return data
    
    def add_investment(self, investment):
        self.investment_list.append(investment)
        

@dataclass
class Report:
    name: str
    output_list: List[str] = field(default_factory=list)

    def add_output(self, output: str):
        self.output_list.append(output)

    def export_json(self, data: dict) -> dict:
        data = add_entity(data, "report", self.name)
        for output in self.output_list:
            data = add_entity(data, "report__output", [self.name, output])
        return data

    def get_output_list_length(self):
        return len(self.output_list)