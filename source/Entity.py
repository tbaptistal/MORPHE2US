import datetime 

class Entity:
    def __init__(self, entity_type = None):
        self.direct_parameters : dict = {}
        if entity_type is not None:
            self.name = "default_name_" + entity_type + "_" + str(datetime.datetime.now().timestamp())[5:]
        else:
            self.name = "default_name_entity_" +  str(datetime.datetime.now().timestamp())[5:]
        self.location_name = ""
    
    def set_name(self, name: str):
        self.name = name
    
    def set_location_name(self, name: str):
        self.location_name = name

    @property
    def full_name(self):
        return self.name + self.location_name

    def add_direct_parameter(self, key: str, data, data_type = None):
        if key == "name":
            self.name = data
        else:
            self.direct_parameters[key] = {"value": data, "type": data_type}

    def get_name(self):
        return self.name
    



