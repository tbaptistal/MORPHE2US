from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Connection(Entity):
    def __init__(self):
        super().__init__("connection")

    def set_node_from(self, node_from):
        self.node_from = node_from

    def set_node_to(self, node_to):
        self.node_to = node_to

    def export_json(self, data: dict):
        data = self.link_nodes(data)
        data = add_entity(data, "connection", self.full_name)
        for key, values in self.direct_parameters.items():
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "connection",  self.full_name, key, values["value"], values["type"])
        return data
    

    def link_nodes(self, data: dict):
        data = add_entity(data, "connection__from_node", [self.full_name, self.node_from.full_name])
        data = add_entity(data, "connection__to_node", [self.full_name, self.node_to.full_name])
        data = add_entity(data, "connection__node__node", [self.full_name, self.node_to.full_name, self.node_from.full_name])

        for parameter in self.direct_parameters:
            if parameter.startswith("NaM"):
                continue
            if "(from_node)" in parameter:
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__from_node", [self.full_name, self.node_from.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
            if "(to_node)" in parameter:
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__to_node", [self.full_name, self.node_to.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
            if "(from_node_to_node)" in parameter:
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__node__node", [self.full_name, self.node_to.full_name, self.node_from.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
        return data