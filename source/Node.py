from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Node(Entity):
    def __init__(self):
        super().__init__("node")
    
    def export_json(self, data: dict, parameter_to_not_export: list = []):
        data = add_entity(data, "node", self.full_name)
        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM") and not key.__contains__("(") and not parameter_to_not_export.__contains__(key):
                data = add_parameter_value(data, "node", self.full_name, key, values["value"], values["type"])
        return data
    
    def add_local_demand(self, target_commodity, time_serie, type_):
        if self.get_name() == target_commodity:
            self.add_direct_parameter("demand", time_serie, type_)