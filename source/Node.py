from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Node(Entity):
    def __init__(self):
        super().__init__("node")
    
    def export_json(self, data: dict, parameter_to_not_export: list = []):
        data = add_entity(data, "node", self.full_name)
        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM") and "(" not in key and key not in parameter_to_not_export:
                data = add_parameter_value(data, "node", self.full_name, key, values["value"], values["type"])
        return data
    
    def add_node_parameter(self, target_parameter , target_commodity, data, data_type, quantity = 1):
        if target_commodity in self.get_name():
            if quantity != 1: 
                if "data" in data:
                    if type(data["data"]) == list:
                        data["data"] = [value * quantity for value in data["data"]]
                    elif type(data["data"]) == dict:
                        data["data"] = {key: value * quantity for key, value in data["data"].items()}
                    else:
                        print(data["data"])
                else: 
                    print(data)           
            self.add_direct_parameter(target_parameter, data, data_type)

    def get_value(self, parameter):
        return self.direct_parameters[parameter]