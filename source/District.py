import copy
from dataclasses import dataclass, field
from typing import List
from itertools import chain

@dataclass
class District:
    name: str
    nodes: List = field(default_factory=list)
    units: List = field(default_factory=list)
    buildings: List = field(default_factory=list)
    connections: List = field(default_factory=list)
    storages: List = field(default_factory=list)

    def add_unit(self, unit):
        unit.set_location_name(f"_D-LVL_{self.name}")
        self.units.append(unit)

    def add_node(self, node):
        node.set_location_name(f"_D-LVL_{self.name}")
        self.nodes.append(node)

    def add_building(self, building):
        building.set_district_name(f"{self.name}")
        building.create_building_retrofit_mode()
        self.buildings.append(building)

    def add_storage(self, storage):
        storage.set_location_name(f"_D-LVL_{self.name}")
        self.storages.append(storage)

    def get_name(self):
        return self.name

    def add_connection(self, connection):
        self.connections.append(connection)

    def add_building_connection(self, connection, commodity, building_name, flag_direction_building="to"):
        if flag_direction_building == "from":
            self.add_building_connection_from(connection, commodity, building_name)
        elif flag_direction_building == "to":
            self.add_building_connection_to(connection, commodity, building_name)
        else:
            print("Error: Wrong flag_direction_building")

    def add_building_connection_to(self, connection, commodity, building_name):
        for node in self.nodes:
            if node.name == commodity:
                connection.set_node_from(node)

        for building in self.buildings:
            if building.get_name() == building_name or (building_name == "All" and building.get_name() != building_name):
                for node in building.nodes:
                    if node.name == commodity:
                        connection.set_node_to(node)
                        connection.set_location_name(f"_D-LVL_{self.name}_{building.get_name()}")
                        self.connections.append(copy.deepcopy(connection))

    def add_building_connection_from(self, connection, commodity, building_name):
        for node in self.nodes:
            if node.name == commodity:
                connection.set_node_to(node)

        for building in self.buildings:
            if building.get_name() == building_name or (building_name == "All" and building.get_name() != building_name):
                for node in building.nodes:
                    if node.name == commodity:
                        connection.set_node_from(node)
                        connection.set_location_name(f"_D-LVL_{building.get_name()}_{self.name}")
                        self.connections.append(copy.deepcopy(connection))

    def add_unit_parameter(self, target_parameter, district_target, building_target, unit_target, data, data_type):
        if district_target == "All" or self.name in district_target:
            if building_target is None:
                self.add_unit_parameter_self(target_parameter, unit_target, data, data_type)
            else:
                self.add_unit_parameter_building(target_parameter, building_target, unit_target, data, data_type)

    def add_unit_parameter_self(self, target_parameter, unit_target, data, data_type):
        for unit in self.units:
            unit.add_unit_parameter(target_parameter, unit_target, data, data_type)

    def add_unit_parameter_building(self,  target_parameter, building_target, unit_target, data, data_type):
        for building in self.buildings:
            building.add_unit_parameter( target_parameter,building_target, unit_target, data, data_type)

    def add_node_parameter(self, target_parameter, district_target, building_target, commodity_target, data, data_type):
        if district_target == "All" or self.name in district_target:
            if building_target is None:
                self.add_node_parameter_self(target_parameter, commodity_target, data, data_type)
            else:
                self.add_node_parameter_building(target_parameter, building_target, commodity_target, data, data_type)

    def add_node_parameter_self(self, target_parameter, commodity_target, data, data_type):
        for node in self.nodes:
            node.add_node_parameter(target_parameter, commodity_target, data, data_type)

    def add_node_parameter_building(self,target_parameter, building_target, commodity_target, data, data_type):
        for building in self.buildings:
            building.add_node_parameter(target_parameter, building_target, commodity_target, data, data_type)

    def export_json(self, data):
        for item in chain(self.nodes, self.units, self.buildings, self.connections, self.storages):
            data = item.export_json(data)
        return data
