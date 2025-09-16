from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Node(Entity):
    def __init__(self):
        # Initialize the Node class by calling the parent Entity class constructor with "node" as the type
        super().__init__("node")
    
    def export_json(self, data: dict, scenario_name: str):
        # Export the Node's data to a JSON-compatible dictionary.
        
        data = add_entity(data, "node", self.full_name, scenario_name)
        
        # Iterate through the Node's direct parameters and add them to the JSON data
        for key, values in self.direct_parameters.items():
            # Skip parameters that start with "NaM", contain "(", or are in the exclusion list
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "node", self.full_name, key, values["value"], values["type"], scenario_name)

        return data
    
    def add_node_parameter(self, target_parameter, target_commodity, data, data_type, quantity=1):
        # Add a special parameter to the Node, modifying the data if a quantity is specified.
        
        # Check if the target commodity is part of the Node's name
        if target_commodity in self.get_name():
            # If quantity is not 1, modify the data values accordingly
            if quantity != 1: 
                if "data" in data:
                    if type(data["data"]) == list:
                        # Multiply each value in the list by the quantity
                        data["data"] = [value * quantity for value in data["data"]]
                    elif type(data["data"]) == dict:
                        # Multiply each value in the dictionary by the quantity
                        data["data"] = {key: value * quantity for key, value in data["data"].items()}
                    else:
                        # Print the data if its type is unexpected
                        print(data["data"])
                else: 
                    # Print the data if the "data" key is missing
                    print(data)           
            # Add the parameter to the Node's direct parameters
            self.add_direct_parameter(target_parameter, data, data_type)

    def get_value(self, parameter):
        return self.direct_parameters[parameter]