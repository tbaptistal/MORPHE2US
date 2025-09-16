import copy
from itertools import chain
from dataclasses import dataclass, field
from typing import List

@dataclass
class Municipality:
    name: str
    districts: List = field(default_factory=list)  # List of districts in the municipality
    nodes: List = field(default_factory=list)  # List of nodes in the municipality
    connections: List = field(default_factory=list)  # List of connections in the municipality

    def add_district(self, district):
        # Add a district to the municipality.
        self.districts.append(district)

    def export_json(self, data: dict, scenario_name: str):
        for item in chain(self.districts, self.nodes, self.connections):
            data = item.export_json(data, scenario_name)
        return data
    
    def add_CO2_connection(self, connection, commodity):
        for node in self.nodes:
            if node.name == commodity:
                connection.set_node_to(node)
        for district in self.districts:
            for node in district.nodes:
                if node.name == commodity:
                    connection.set_node_from(node)
                    connection.set_location_name(f"_D-LVL_{node.full_name}")
                    self.connections.append(copy.deepcopy(connection))
            for building in district.buildings:
                for node in building.nodes:
                    if node.name == commodity:
                        connection.set_node_from(node)
                        connection.set_location_name(f"_B-LVL_{node.full_name}")
                        self.connections.append(copy.deepcopy(connection))
   
    def add_district_interconnection(self, connection, commodity, district_from_name, district_to_name):
        for district in self.districts:
            if district.get_name() == district_to_name:
                for node in district.nodes:
                    if node.name == commodity:
                        connection.set_node_to(node)
                for district in self.districts:
                    if district.get_name() == district_from_name:
                        for node in district.nodes:
                            if node.get_name() == commodity:
                                connection.set_node_from(node)
                        connection.set_location_name(f"_M-LVL_{district_from_name}_{district_to_name}")
                        self.connections.append(copy.deepcopy(connection))
                       
    def add_node(self, node):
        node.set_location_name(f"_M-LVL")
        self.nodes.append(node)

    def add_unit_parameter(self, target_parameter, district_target, building_target, unit_target, data, data_type):
        for district in self.districts:
            district.add_unit_parameter(target_parameter, district_target, building_target, unit_target, data, data_type)

    def add_node_parameter(self, target_parameter, district_target, building_target, commodity_target, data, data_type, quantitative_flag):
        for district in self.districts:
            district.add_node_parameter(target_parameter, district_target, building_target, commodity_target, data, data_type, quantitative_flag)
