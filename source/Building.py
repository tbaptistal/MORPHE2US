import copy
from source.Connection import Connection  
from dataclasses import dataclass
from itertools import chain
from dataclasses import dataclass, field

@dataclass
class Retrofit:
    name: str
    commodity: str
    price: float
    decrease_to_normal: float


@dataclass
class Building:
    name: str
    building_type: str
    construction_year: str
    units: list = field(default_factory=list)
    nodes: list = field(default_factory=list)
    quantity: int = 1
    district_name: str = ""
    connections: list = field(default_factory=list)
    storages: list = field(default_factory=list)
    retrofit_list: list = field(default_factory=list)
    nodes_to_retrofit: list = field(default_factory=list)

    def add_unit(self, unit):
        unit.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
        self.units.append(unit)

    def add_node(self, node):
        node.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
        self.nodes.append(node)

    def add_storage(self, storage):
        storage.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
        self.storages.append(storage)

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_name(self):
        return self.name

    def add_retrofit(self, name, commodity_to_retrofit, increase_performance, price):
        if commodity_to_retrofit not in self.nodes_to_retrofit:
            self.nodes_to_retrofit.append(commodity_to_retrofit)
        self.retrofit_list.append(Retrofit(name, commodity_to_retrofit, price * self.quantity, increase_performance))

    def create_building_retrofit_mode(self):
        for node in self.nodes:
            if node.get_name() in self.nodes_to_retrofit:
                new_node = copy.deepcopy(node)
                old_demand = 0
                if "demand" in new_node.direct_parameters:
                    old_demand = new_node.get_value("demand")
                    node.add_direct_parameter("demand", 0)
                   
                new_node.set_name(f"Retrofit_{node.get_name()}")
                self.nodes.append(new_node)
                

                new_connection = Connection()
                new_connection.name = f"Base_connection_{node.get_name()}_{self.name}_{self.district_name}"
                new_connection.set_node_from(node)
                new_connection.set_node_to(new_node)
                new_connection.add_direct_parameter("fix_ratio_out_in_connection_flow(from_node_to_node)", 1)
                self.connections.append(new_connection)

                for retrofit in self.retrofit_list:
                    if retrofit.commodity == node.get_name():
                        new_connection = Connection()
                        new_connection.name = f"{retrofit.name}_{self.name}_{self.district_name}"
                        new_connection.set_node_from(node)
                        new_connection.set_node_to(new_node)
                        new_connection.add_direct_parameter("connection_investment_cost", retrofit.price)
                        new_connection.add_direct_parameter("connection_investment_variable_type", "connection_investment_variable_type_continuous", "string")
                        if (1 - retrofit.decrease_to_normal) == 0:
                            raise ValueError("The retrofit cannot cancel out a demand: Here the decrease_to_normal is 100%")
                        ratio = 1 / (1 - retrofit.decrease_to_normal)
                        new_connection.add_direct_parameter("fix_ratio_out_in_connection_flow(from_node_to_node)", ratio)
                        new_connection.add_direct_parameter("number_of_connections", 0)
                        new_demand = copy.deepcopy(old_demand)
                        for key in new_demand["value"]["data"]:
                            new_demand["value"]["data"][key] = new_demand["value"]["data"][key] / self.quantity
                        new_connection.add_direct_parameter("connection_capacity(to_node)", new_demand["value"])
                        new_connection.add_direct_parameter("candidate_connections", self.quantity)
                        self.connections.append(new_connection)

    def add_unit_parameter(self, target_parameter, building_target, unit_target, data, data_type):
        if building_target == "All" or self.get_name() in building_target:
            for unit in self.units:
                unit.add_unit_parameter(target_parameter, unit_target, data, data_type)
            for storage in self.storages:
                storage.add_storage_parameter(target_parameter, unit_target, data, data_type)

    def add_node_parameter(self, target_parameter, building_target, commodity_target, data, data_type, quantitative_flag):
        if building_target == "All" or self.get_name() in building_target:
            for node in self.nodes:
                if quantitative_flag:
                    node.add_node_parameter(target_parameter, commodity_target, data, data_type, self.quantity)
                else:
                    node.add_node_parameter(target_parameter, commodity_target, data, data_type)

    def set_district_name(self, district_name: str):
        self.district_name = district_name
        for item in chain(self.nodes, self.units, self.storages):
            item.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")

    def export_json(self, data: dict):
        for item in chain(self.nodes, self.units, self.connections, self.storages):
            data = item.export_json(data)
        return data

