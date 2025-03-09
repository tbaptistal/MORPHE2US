from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Unit(Entity):
    def __init__(self):
        super().__init__("unit")

    def add_unit_parameter(self, target_parameter, unit_target, data, data_type):
        if unit_target in self.get_name():
            # print(f"Adding parameter {target_parameter} to {self.get_name()}")
            self.add_direct_parameter(target_parameter, data, data_type)
    
    def add_co2(self):
        from_node = len([parameter for parameter in self.direct_parameters if parameter.startswith("NaM_unit__from_node")])
        to_node = len([parameter for parameter in self.direct_parameters if parameter.startswith("NaM_unit__to_node")])
        if "NaM_emission" not in self.direct_parameters:
            return
        if self.direct_parameters["NaM_emission"]["value"] > 0:
            # Generate CO2 (to node) -> Check if there is a unit_from_node (to link it to the CO2)
            self.add_direct_parameter(f"NaM_unit__to_node{to_node+1}", "CO2")
            if from_node == 0: # There is NOT a unit__from_node so the CO2 is related to the other unit__to_node
                self.add_direct_parameter(f"fix_ratio_out_out_unit_flow(to_node1to_node{to_node+1})", 1/self.direct_parameters["NaM_emission"]["value"])
            else: # There is a unit__from_node so the ratio is related to this node (te first one)
                self.add_direct_parameter(f"fix_ratio_out_in_unit_flow(from_node1to_node{to_node+1})", self.direct_parameters["NaM_emission"]["value"])
        elif self.direct_parameters["NaM_emission"]["value"] < 0:
            self.add_direct_parameter(f"NaM_unit__from_node{from_node+1}", "CO2")
            self.add_direct_parameter(f"fix_ratio_in_in_unit_flow(from_node1from_node{from_node+1})", abs(1/self.direct_parameters["NaM_emission"]["value"]))

    def export_json(self, data: dict):
        data = add_entity(data, "unit", self.full_name)

        dict__link_nodes = {}
        for parameter in self.direct_parameters:
            if parameter.startswith("NaM_unit__"):
                dict__link_nodes[parameter.split("NaM_")[1]] = f"{self.direct_parameters[parameter]["value"]}{self.location_name}"
                entity_name = f"{parameter.split("NaM_")[1].split('node')[0]}node"
                entity_linked_to = f"{self.direct_parameters[parameter]["value"]}{self.location_name}"
                data = add_entity(data, entity_name , [self.full_name, entity_linked_to])
        to_node = len([key for key in dict__link_nodes if key.startswith("unit__to_node")])
        from_node = len([key for key in dict__link_nodes if key.startswith("unit__from_node")])


        # Creating the special linkes unit__node__node only if we have at least 1 input node AND 1 output node
        for i in range(to_node):
            for j in range(from_node):
                data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__to_node{i+1}']}", f"{dict__link_nodes[f'unit__from_node{j+1}']}"])
        # If we have 2 input nodes (like CO2 and electricity for a carbon capture unit), we create a link
        if to_node == 0 and from_node == 2:
            data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__from_node1']}", f"{dict__link_nodes[f'unit__from_node2']}"])
        # If we have 2 output nodes (like CO2 and electricity from grid import with grid CO2 intensity), we create a link
        if to_node == 2 and from_node == 0:
            data = add_entity(data, "unit__node__node", [self.full_name, f"{dict__link_nodes[f'unit__to_node1']}", f"{dict__link_nodes[f'unit__to_node2']}"])



        for parameter, values in self.direct_parameters.items():
            if not parameter.startswith("NaM"):
                match parameter:
                    case p if "unit__from_node" in p:
                        node_name = f'{dict__link_nodes[p.split(")")[0].split("(")[1]]}'
                        data = add_parameter_value(data, "unit__from_node", [self.full_name, node_name], p.split("(")[0], values["value"], values["type"])
                    case p if "unit__to_node" in p:
                        node_name = f'{dict__link_nodes[p.split(")")[0].split("(")[1]]}'
                        data = add_parameter_value(data, "unit__to_node", [self.full_name, node_name], p.split("(")[0], values["value"], values["type"])
                    case p if "from_node" in p and "to_node" in p:
                        node_from = f'{dict__link_nodes[f"unit__from_node{p.split("to_node")[0].split("from_node")[1]}"]}'
                        node_to = f'{dict__link_nodes[f"unit__to_node{p.split(")")[0].split("to_node")[1]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_to, node_from], p.split("(")[0], values["value"], values["type"])
                    case p if "from_node" in p and "to_node" not in p:
                        node_1 = f'{dict__link_nodes[f"unit__from_node{p.split("from_node")[1]}"]}'
                        node_2 = f'{dict__link_nodes[f"unit__from_node{p.split(")")[0].split("from_node")[2]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_1, node_2], p.split("(")[0], values["value"], values["type"])
                    case p if "from_node" not in p and "to_node" in p:
                        node_1 = f'{dict__link_nodes[f"unit__to_node{p.split("to_node")[1]}"]}'
                        node_2 = f'{dict__link_nodes[f"unit__to_node{p.split(")")[0].split("to_node")[2]}"]}'
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node_1, node_2], p.split("(")[0], values["value"], values["type"])
                    case _:
                        data = add_parameter_value(data, "unit", self.full_name, parameter, values["value"], values["type"])
        return data
    



            