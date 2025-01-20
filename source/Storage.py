from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Storage(Entity):
    def __init__(self):
        super().__init__("storage")

    def export_json(self, data: dict):
        data = add_entity(data, "node", self.full_name)
        data = add_entity(data, "unit", self.full_name)

        data = add_entity(data, "unit__to_node", [self.full_name, self.full_name])
        data = add_entity(data, "unit__from_node", [self.full_name, self.full_name])

        # NaM_stored_commodity
        node__commodity = f"{self.direct_parameters['NaM_stored_commodity']['value']}{self.location_name}"
        data = add_entity(data, "unit__to_node", [self.full_name, node__commodity])
        data = add_entity(data, "unit__from_node", [self.full_name, node__commodity])

        data = add_entity(data, "unit__node__node", [self.full_name, self.full_name, node__commodity])
        data = add_entity(data, "unit__node__node", [self.full_name, node__commodity, self.full_name])

        data = add_entity(data, "investment_group", self.full_name)
        data = add_entity(data, "unit__investment_group", [self.full_name, self.full_name])
        data = add_entity(data, "node__investment_group", [self.full_name, self.full_name])
        data = add_parameter_value(data, "investment_group", self.full_name, "equal_investments", True, "bool")

        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM"):
                if "(node)" in key:
                    data = add_parameter_value(data, "node", self.full_name, key.split("(")[0], values["value"], values["type"])
                elif "(unit)" in key:
                    data = add_parameter_value(data, "unit", self.full_name, key.split("(")[0], values["value"], values["type"])
                elif "(unit_or_node)" in key:
                    data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split("(")[0]}", values["value"], values["type"])
                    data = add_parameter_value(data, "node", self.full_name, f"storage{key.split("(")[0]}", 0, "float")
                elif "(unit_and_node)" in key:
                    if values["type"] == "string_special":
                        data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split("(")[0]}", f"unit{values['value']}", values["type"])
                        data = add_parameter_value(data, "node", self.full_name, f"storage{key.split("(")[0]}", f"storage{values['value']}", values["type"])
                    else:
                        data = add_parameter_value(data, "unit", self.full_name, f"unit{key.split("(")[0]}", values["value"], values["type"])
                        data = add_parameter_value(data, "node", self.full_name, f"storage{key.split("(")[0]}", values["value"], values["type"])
                elif "(unit__from_commodity)" in key:
                    data = add_parameter_value(data, "unit__from_node", [self.full_name, node__commodity], key.split("(")[0], values["value"], values["type"])
                elif "(unit__to_commodity)" in key:
                    data = add_parameter_value(data, "unit__to_node", [self.full_name, node__commodity], key.split("(")[0], values["value"], values["type"])
                elif "(unit__node__node)" in key:
                    data = add_parameter_value(data, "unit__node__node", [self.full_name, node__commodity, self.full_name], key.split("(")[0], values["value"], values["type"])
                elif key == "number_of_units" or key == "candidate_units":
                    data = add_parameter_value(data, "unit", self.full_name, key, values["value"], values["type"])
                    data = add_parameter_value(data, "node", self.full_name, key.replace("units", "storages"), values["value"], values["type"])
                else:
                    print(f"Error, key {key} not recognized in Storage")
        return data