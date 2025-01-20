import copy
from source.Connection import Connection

class Retrofit:
    def __init__(self, name, commodity, price, decrease_to_normal):
        self.name = name
        self.commodity = commodity
        self.price = price
        self.decrease_to_normal = decrease_to_normal    


class Building:
    def __init__(self, name:str, type_: str, construction_year: str):
        self.units = []
        self.nodes = []
        self.name = name
        self.construction_year : str = construction_year
        self.type_SF_MF : str = type_
        self.quantity : int = 1
        self.district_name = ""
        self.connections = []
        self.storages = []
        self.retrofit_list = []
        self.nodes_to_retrofit = []

    def add_unit(self, unit):
        self.units.append(unit)
        self.units[-1].set_location_name(f"_{self.district_name}_B-LVL_{self.name}")

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes[-1].set_location_name(f"_{self.district_name}_B-LVL_{self.name}")

    def add_storage(self, storage):
        self.storages.append(storage)
        self.storages[-1].set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
    
    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def add_connection(self, connection):
        self.connections.append(connection)

    def get_name(self):
        return self.name
    
    def add_retrofit(self, name, commodity_to_retrofit, increase_performance, price):
        if commodity_to_retrofit not in self.nodes_to_retrofit:
            self.nodes_to_retrofit.append(commodity_to_retrofit)
        self.retrofit_list.append(Retrofit(name, commodity_to_retrofit, price*self.quantity, increase_performance))

    def create_building_retrofit_mode(self):
        for node in self.nodes:
            if node.get_name() in self.nodes_to_retrofit:
                ## Create a new node only for the building retrofit investment ## 
                new_node = copy.deepcopy(node)
                if "demand" in new_node.direct_parameters:
                    node.add_direct_parameter("demand", 0)
                new_node.set_name(f"Retrofit_{node.get_name()}") # 
                self.nodes.append(new_node)

                ## Add the connections ##
                new_connection = Connection()
                new_connection.name = f"Base_connection_{node.get_name()}_{self.name}_{self.district_name}"
                new_connection.set_node_from(node)
                new_connection.set_node_to(new_node)
                new_connection.add_direct_parameter("fix_ratio_out_in_connection_flow(from_node_to_node)", 1)
                new_connection.add_direct_parameter("connection_capacity(to_node)", 1e15)
                self.connections.append(new_connection)
                ## Add the connections ##
                for retrofit in self.retrofit_list:
                    if retrofit.commodity == node.get_name():
                        new_connection = Connection()
                        new_connection.name = f"{retrofit.name}_{self.name}_{self.district_name}"
                        new_connection.set_node_from(node)
                        new_connection.set_node_to(new_node)
                        new_connection.add_direct_parameter("connection_investment_cost", retrofit.price)
                        new_connection.add_direct_parameter("fix_ratio_out_in_connection_flow(from_node_to_node)", 1/retrofit.decrease_to_normal)
                        new_connection.add_direct_parameter("number_of_connections", 0)
                        new_connection.add_direct_parameter("candidate_connections", 1)
                        new_connection.add_direct_parameter("connection_capacity(to_node)", 1e15)
                        self.connections.append(new_connection)
 
    def add_availability_factor(self, building_target, unit_target, time_serie, type_):
        if building_target == "All" or self.get_name() in building_target:
            for unit in self.units:
                unit.add_availability_factor(unit_target, time_serie, type_)

    def add_local_demand(self, commodity_target, building_target, time_serie, type_):
        if building_target == "All" or self.get_name() in building_target:
            for node in self.nodes:
                if type(time_serie[1]) == dict:
                    for key in time_serie[1]:
                        time_serie[1][key] = time_serie[1][key]*self.quantity
                else:
                    time_serie[1] = time_serie[1]*self.quantity
                node.add_local_demand(commodity_target, time_serie, type_)

    def set_district_name(self, district_name: str):
        self.district_name = district_name
        for node in self.nodes:
            node.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
        for unit in self.units:
            unit.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")
        for storage in self.storages:
            storage.set_location_name(f"_{self.district_name}_B-LVL_{self.name}")

    def export_json(self, data: dict):
        for node in self.nodes:
            data = node.export_json(data)
        for unit in self.units:
            data = unit.export_json(data)
        for connection in self.connections:
            data = connection.export_json(data)
        for storage in self.storages:
            data = storage.export_json(data)
        return data

