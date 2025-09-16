from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Unit(Entity):
    def __init__(self):
        # Initialize the Unit class as a subclass of Entity with the name "unit"
        super().__init__("unit")

    def add_unit_parameter(self, target_parameter, unit_target, data, data_type):
        # Add a parameter to the unit if the unit_target matches the unit's name
        if unit_target in self.get_name():
            self.add_direct_parameter(target_parameter, data, data_type)
    
    def add_co2(self):
        # Count the number of "from_node" and "to_node" parameters in the unit
        from_node = len([parameter for parameter in self.direct_parameters if parameter.startswith("NaM_unit__from_node")])
        to_node = len([parameter for parameter in self.direct_parameters if parameter.startswith("NaM_unit__to_node")])
        
        # If "NaM_emission" is not present, exit the function
        if "NaM_emission" not in self.direct_parameters:
            return

        # Handle cases where "NaM_emission" is a dictionary
        if type(self.direct_parameters["NaM_emission"]["value"]) is dict:
            CO2_emissions = list(self.direct_parameters["NaM_emission"]["value"]["data"].values())
            
            # Check if all emission values are positive
            if all(value >= 0 for value in CO2_emissions):
                print(f"Positive emissions for {self.get_name()}: {CO2_emissions}")
                self.add_direct_parameter(f"NaM_unit__to_node{to_node+1}", "CO2")
                if from_node == 0:
                    # Adjust emission values and add a ratio parameter for output-output flow
                    for key in self.direct_parameters["NaM_emission"]["value"]["data"].keys():
                        if self.direct_parameters["NaM_emission"]["value"]["data"][key] == 0:
                            self.direct_parameters["NaM_emission"]["value"]["data"][key] = 0
                        else:
                            self.direct_parameters["NaM_emission"]["value"]["data"][key] = abs(1/self.direct_parameters["NaM_emission"]["value"]["data"][key])
                    self.add_direct_parameter(f"fix_ratio_out_out_unit_flow(to_node1to_node{to_node+1})", self.direct_parameters["NaM_emission"]["value"])
                else:
                    # Add a ratio parameter for output-input flow
                    self.add_direct_parameter(f"fix_ratio_out_in_unit_flow(from_node1to_node{to_node+1})", self.direct_parameters["NaM_emission"]["value"])

            # Check if all emission values are negative
            elif all(value <= 0 for value in CO2_emissions):
                print(f"Negative emissions for {self.get_name()}: {CO2_emissions}")
                self.add_direct_parameter(f"NaM_unit__from_node{from_node+1}", "CO2")
                # Adjust emission values and add a ratio parameter for input-input flow
                for key in self.direct_parameters["NaM_emission"]["value"]["data"].keys():
                    if self.direct_parameters["NaM_emission"]["value"]["data"][key] == 0:
                        self.direct_parameters["NaM_emission"]["value"]["data"][key] = 0
                    else:
                        self.direct_parameters["NaM_emission"]["value"]["data"][key] = abs(1/self.direct_parameters["NaM_emission"]["value"]["data"][key])
                self.add_direct_parameter(f"fix_ratio_in_in_unit_flow(from_node1from_node{from_node+1})", self.direct_parameters["NaM_emission"]["value"])

            # Handle mixed positive and negative emissions
            else:
                print(f"Warning: Mixed emissions for {self.get_name()}: {CO2_emissions}")
                print("Please check the values: The model can't handle positive & negative emissions for the same unit.")
            
            return

        # Handle cases where "NaM_emission" is a single value
        if self.direct_parameters["NaM_emission"]["value"] > 0:
            # Positive emissions: Add a "to_node" parameter and adjust ratios
            self.add_direct_parameter(f"NaM_unit__to_node{to_node+1}", "CO2")
            if from_node == 0:
                self.add_direct_parameter(f"fix_ratio_out_out_unit_flow(to_node1to_node{to_node+1})", 1/self.direct_parameters["NaM_emission"]["value"])
            else:
                self.add_direct_parameter(f"fix_ratio_out_in_unit_flow(from_node1to_node{to_node+1})", self.direct_parameters["NaM_emission"]["value"])
        elif self.direct_parameters["NaM_emission"]["value"] < 0:
            # Negative emissions: Add a "from_node" parameter and adjust ratios
            self.add_direct_parameter(f"NaM_unit__from_node{from_node+1}", "CO2")
            self.add_direct_parameter(f"fix_ratio_in_in_unit_flow(from_node1from_node{from_node+1})", abs(1/self.direct_parameters["NaM_emission"]["value"]))

    def export_json(self, data: dict, scenario_name: str):
        # Add the unit entity to the JSON data
        data = add_entity(data, "unit", self.full_name, scenario_name)

        dict__link_nodes = {}
        # Process "NaM_unit__" parameters to create links between nodes
        for parameter in self.direct_parameters:
            if parameter.startswith("NaM_unit__"):
                dict__link_nodes[parameter.split("NaM_")[1]] = f'{self.direct_parameters[parameter]["value"]}{self.location_name}'
                entity_name = f'{parameter.split("NaM_")[1].split("node")[0]}node'
                entity_linked_to = f'{self.direct_parameters[parameter]["value"]}{self.location_name}'
                data = add_entity(data, entity_name , [self.full_name, entity_linked_to], scenario_name)
        
        # Count the number of "to_node" and "from_node" parameters
        to_node = len([key for key in dict__link_nodes if key.startswith("unit__to_node")])
        from_node = len([key for key in dict__link_nodes if key.startswith("unit__from_node")])

        # Create special links between nodes if there are both input and output nodes
        for i in range(to_node):
            for j in range(from_node):
                data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__to_node{i+1}']}", f"{dict__link_nodes[f'unit__from_node{j+1}']}"], scenario_name)
        
        # Handle cases with two input nodes or two output nodes
        if to_node == 0 and from_node == 2:
            data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__from_node1']}", f"{dict__link_nodes[f'unit__from_node2']}"], scenario_name)
        if to_node == 2 and from_node == 0:
            data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__to_node1']}", f"{dict__link_nodes[f'unit__to_node2']}"], scenario_name)

        # Add parameter values to the JSON data
        for parameter, values in self.direct_parameters.items():
            if not parameter.startswith("NaM"):
                match parameter:
                    case p if "unit__from_node" in p:
                        node_name = f'{dict__link_nodes[p.split(")")[0].split("(")[1]]}'
                        data = add_parameter_value(data, "unit__from_node", [self.full_name, node_name], p.split("(")[0], values["value"], values["type"], scenario_name)
                    case p if "unit__to_node" in p:
                        node_name = f'{dict__link_nodes[p.split(")")[0].split("(")[1]]}'
                        data = add_parameter_value(data, "unit__to_node", [self.full_name, node_name], p.split("(")[0], values["value"], values["type"], scenario_name)
                    case p if "from_node" in p and "to_node" in p:
                        node_from = f'{dict__link_nodes[f"unit__from_node{p.split("to_node")[0].split("from_node")[1]}"]}'
                        node_to = f'{dict__link_nodes[f"unit__to_node{p.split(")")[0].split("to_node")[1]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_to, node_from], p.split("(")[0], values["value"], values["type"], scenario_name)
                    case p if "from_node" in p and "to_node" not in p:
                        node_1 = f'{dict__link_nodes[f"unit__from_node{p.split("from_node")[1]}"]}'
                        node_2 = f'{dict__link_nodes[f"unit__from_node{p.split(")")[0].split("from_node")[2]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_1, node_2], p.split("(")[0], values["value"], values["type"], scenario_name)
                    case p if "from_node" not in p and "to_node" in p:
                        node_1 = f'{dict__link_nodes[f"unit__to_node{p.split("to_node")[1]}"]}'
                        node_2 = f'{dict__link_nodes[f"unit__to_node{p.split(")")[0].split("to_node")[2]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_1, node_2], p.split("(")[0], values["value"], values["type"], scenario_name)
                    case _:
                        data = add_parameter_value(data, "unit", self.full_name, parameter, values["value"], values["type"], scenario_name)
        return data