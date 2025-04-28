from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Storage(Entity):
    def __init__(self):
        # Initialize the Storage class as a subclass of Entity with the name "storage"
        super().__init__("storage")

    def export_json(self, data: dict):
        # Add the storage node entity to the JSON data
        data = add_entity(data, "node", self.full_name)
        # Add a parameter indicating that the node has a state
        data = add_parameter_value(data, "node", self.full_name, "has_state", True, "bool")
        # Add the storage unit entity to the JSON data
        data = add_entity(data, "unit", self.full_name)

        # Define relationships between the unit and the node
        data = add_entity(data, "unit__to_node", [self.full_name, self.full_name])
        data = add_entity(data, "unit__from_node", [self.full_name, self.full_name])

        # Handle the stored commodity relationship
        node__commodity = f"{self.direct_parameters['NaM_stored_commodity']['value']}{self.location_name}"
        data = add_entity(data, "unit__to_node", [self.full_name, node__commodity])
        data = add_entity(data, "unit__from_node", [self.full_name, node__commodity])

        # Define relationships between the unit, node, and commodity
        data = add_entity(data, "unit__node__node", [self.full_name, self.full_name, node__commodity])
        data = add_entity(data, "unit__node__node", [self.full_name, node__commodity, self.full_name])

        # Add investment group and related parameters
        data = add_entity(data, "investment_group", self.full_name)
        data = add_entity(data, "unit__investment_group", [self.full_name, self.full_name])
        data = add_entity(data, "node__investment_group", [self.full_name, self.full_name])
        data = add_parameter_value(data, "investment_group", self.full_name, "equal_investments", True, "bool")

        # Process direct parameters and add them to the JSON data
        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM"):  # Skip parameters starting with "NaM"
                match key:
                    case key if "(node)" in key:
                        # Add node-specific parameters
                        data = add_parameter_value(data, "node", self.full_name, key.split("(")[0], values["value"], values["type"])
                    case key if "(unit)" in key:
                        # Add unit-specific parameters
                        data = add_parameter_value(data, "unit", self.full_name, key.split("(")[0], values["value"], values["type"])
                    case key if "(unit_or_node)" in key:
                        # Add parameters that apply to both unit and node
                        data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split('(')[0]}", values["value"], values["type"])
                        data = add_parameter_value(data, "node", self.full_name, f"storage{key.split('(')[0]}", 0, "float")
                    case key if "(unit_and_node)" in key:
                        # Add parameters that apply to both unit and node, with special handling for autofill strings
                        if values["type"] == "autofill_string":
                            data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split('(')[0]}", f"unit{values['value']}", values["type"])
                            data = add_parameter_value(data, "node", self.full_name, f"storage{key.split('(')[0]}", f"storage{values['value']}", values["type"])
                        else:
                            data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split('(')[0]}", values["value"], values["type"])
                            data = add_parameter_value(data, "node", self.full_name, f"storage{key.split('(')[0]}", values["value"], values["type"])
                    case key if "(unit__from_commodity)" in key:
                        # Add parameters for unit-to-commodity relationships
                        data = add_parameter_value(data, "unit__from_node", [self.full_name, node__commodity], key.split("(")[0], values["value"], values["type"])
                    case key if "(unit__to_commodity)" in key:
                        # Add parameters for commodity-to-unit relationships
                        data = add_parameter_value(data, "unit__to_node", [self.full_name, node__commodity], key.split("(")[0], values["value"], values["type"])
                    case key if "(unit__node__storage)" in key:
                        # Add parameters for unit-node-storage relationships
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, node__commodity, self.full_name], key.split("(")[0], values["value"], values["type"])
                    case key if "(unit__storage__node)" in key:
                        # Add parameters for storage-unit-node relationships
                        data = add_parameter_value(data, "unit__node__node", [self.full_name, self.full_name, node__commodity], key.split("(")[0], values["value"], values["type"])
                    case "number_of_units" | "candidate_units":
                        # Add parameters for the number of units or candidate units
                        data = add_parameter_value(data, "unit", self.full_name, key, values["value"], values["type"])
                        data = add_parameter_value(data, "node", self.full_name, key.replace("units", "storages"), values["value"], values["type"])
                    case _:
                        # Handle unrecognized keys
                        print(f"Error, key {key} not recognized in Storage")
        return data

    def add_storage_parameter(self, target_parameter, unit_target, data, data_type):
        # Add a storage parameter if the unit target matches the storage name
        if unit_target in self.get_name():
            self.add_direct_parameter(target_parameter, data, data_type)