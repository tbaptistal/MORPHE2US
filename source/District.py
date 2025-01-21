import copy

class District:
    def __init__(self, name: str):
        self.name = name
        self.nodes = []
        self.units = []
        self.buildings = []
        self.connections = []
        self.storages = []
    
    def add_unit(self, unit):
        self.units.append(unit)
        self.units[-1].set_location_name(f"_D-LVL_{self.name}")

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes[-1].set_location_name(f"_D-LVL_{self.name}")

    def add_building(self, building):
        self.buildings.append(building)
        self.buildings[-1].set_district_name(f"{self.name}")
        self.buildings[-1].create_building_retrofit_mode()

    def add_storage(self, storage):
        self.storages.append(storage)
        self.storages[-1].set_location_name(f"_D-LVL_{self.name}")

    def get_name(self):
        return self.name

    def add_connection(self, connection):
        self.connections.append(connection)
    
    def add_building_connection(self, connection, comodity, building_name, flag_direction_building = "to"): # To Building as default
        for node in self.nodes:
            if node.name == comodity:
                if flag_direction_building == "from": # From Building here to it's to the District's node
                    connection.set_node_to(node)
                else:
                    connection.set_node_from(node)

        for building in self.buildings:
            if building.get_name() == building_name or (building_name == "All" and building.get_name() != building_name):
                for node in building.nodes:
                    if node.name == comodity:
                        if flag_direction_building == "from":
                            connection.set_node_from(node)
                            connection.set_location_name(f"_D-LVL_{building.get_name()}_{self.name}")
                        else:
                            connection.set_node_to(node)
                            connection.set_location_name(f"_D-LVL_{self.name}_{building.get_name()}")

                        self.connections.append(copy.deepcopy(connection))

    def add_availability_factor(self, district_target, building_target, unit_target, time_serie, type_):
        if district_target == "All" or self.name in district_target:
            if building_target == None: # No building to assign so only assign to unit at district level
                for unit in self.units:
                    unit.add_availability_factor(unit_target, time_serie, type_)   
            else:
                for building in self.buildings:
                    building.add_availability_factor(building_target, unit_target, time_serie, type_)

    def add_local_demand(self, commodity_target, district_target, building_target, time_serie, type_):
        if district_target == "All" or self.name in district_target:
            if building_target == None: # No building to assign so only assign to nodes at district level
                for node in building.nodes:
                    node.add_local_demand(commodity_target, time_serie, type_)
            else:
                for building in self.buildings:
                    building.add_local_demand(commodity_target, building_target, time_serie, type_)

    def export_json(self, data):
        for node in self.nodes:
            data = node.export_json(data)
        for unit in self.units:
            data = unit.export_json(data)
        for building in self.buildings:
            data = building.export_json(data)
        for connection in self.connections:
            data = connection.export_json(data)
        for storage in self.storages:
            data = storage.export_json(data)
        return data