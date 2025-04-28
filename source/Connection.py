from source.Entity import Entity
from source.helpers.filling_json_functions import add_entity, add_parameter_value

class Connection(Entity):
    def __init__(self):
        # Initialize the Connection class as a subclass of Entity with the type "connection"
        super().__init__("connection")

    def set_node_from(self, node_from):
        # Set the source node of the connection
        self.node_from = node_from

    def set_node_to(self, node_to):
        # Set the destination node of the connection
        self.node_to = node_to

    def export_json(self, data: dict):
        # Export the connection data to a JSON-compatible dictionary
        # First, link the nodes and then add the connection entity and its parameters
        data = self.link_nodes(data)
        data = add_entity(data, "connection", self.full_name)
        for key, values in self.direct_parameters.items():
            # Skip parameters that are not directly usable in SpineOpt (e.g., marked as "NaM")
            # or have specific meanings handled elsewhere (e.g., parameters with parentheses)
            if not key.startswith("NaM") and "(" not in key:
                data = add_parameter_value(data, "connection", self.full_name, key, values["value"], values["type"])
        return data

    def link_nodes(self, data: dict):
        # Link the connection to its source and destination nodes in the data dictionary
        data = add_entity(data, "connection__from_node", [self.full_name, self.node_from.full_name])
        data = add_entity(data, "connection__to_node", [self.full_name, self.node_to.full_name])
        data = add_entity(data, "connection__node__node", [self.full_name, self.node_to.full_name, self.node_from.full_name])

        # Process parameters that are specific to the connection's nodes
        for parameter in self.direct_parameters:
            if parameter.startswith("NaM"):
                # Skip parameters marked as "NaM" (Not a Model)
                continue
            if "(from_node)" in parameter:
                # Handle parameters specific to the source node
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__from_node", [self.full_name, self.node_from.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
            if "(to_node)" in parameter:
                # Handle parameters specific to the destination node
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__to_node", [self.full_name, self.node_to.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
            if "(from_node_to_node)" in parameter:
                # Handle parameters specific to the relationship between the source and destination nodes
                parameter_name = parameter.split("(")[0]
                data = add_parameter_value(data, "connection__node__node", [self.full_name, self.node_to.full_name, self.node_from.full_name], parameter_name, self.direct_parameters[parameter]["value"], self.direct_parameters[parameter]["type"])
        return data