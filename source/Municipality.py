import copy

class Municipality:
    def __init__(self, name: str):
        self.name = name
        self.districts = []
        self.nodes = []
        self.connections = []

    def add_district(self, district):
        self.districts.append(district)

    def export_json(self, data: dict):
        for district in self.districts:
            data = district.export_json(data)
        for node in self.nodes:
            data = node.export_json(data)
        for connection in self.connections:
            data = connection.export_json(data)
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
            if district.get_name() == district_to_name or (district_to_name == "All" and district.get_name() != district_from_name):
                for node in district.nodes:
                    if node.name == commodity:
                        connection.set_node_to(node)
                for district in self.districts:
                    if  district.get_name() == district_from_name or (district_from_name == "All" and district.get_name() != district_to_name):
                        for node in district.nodes:
                            if node.get_name() == commodity:
                                connection.set_node_from(node)
                        connection.set_location_name(f"_M-LVL_{district_from_name}_{district_to_name}") ## Change here if you wanna create multiple connections when "All" or multiple districts are used
                        self.connections.append(copy.deepcopy(connection))
                        # print(f"Connection {connection.get_name()} added to district {district.get_name()} -- {commodity}")

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes[-1].set_location_name(f"_M-LVL")

    def add_availability_factor(self, district_target, building_target, unit_target, time_serie, type_):
        for district in self.districts:
            district.add_availability_factor(district_target, building_target, unit_target, time_serie, type_)

    def add_local_demand(self, commodity_target, district_target, building_target, time_serie, type_):
        for district in self.districts:
            district.add_local_demand(commodity_target, district_target, building_target, time_serie, type_)
            