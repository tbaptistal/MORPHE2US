import datetime 

def fill_dict(vector_str):
    dict_ = {}
    vector_str = vector_str[1:-1].split(",")
    
    for item in vector_str:
        key, value = item.split('":')
        key = key.strip()[1:]
        if value.strip().isdigit():
            value = int(value)
        else:
            value = value.strip()
        dict_[key] = value
    return dict_


class Entity:
    def __init__(self, type_ = None):
        self.direct_parameters : dict = {}
        if type_ != None:
            self.name = "default_name_" + type_ + "_" + str(datetime.datetime.now().timestamp())[5:]
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

    def add_direct_parameter(self, key: str, value, type_ = None):
        if key == "name":
            self.name = value
        elif str(value).startswith("{") and str(value).endswith("}"):
            print(value, type(value))
            dict_value = fill_dict(value)
            print(dict_value, type(dict_value))
            # self.direct_parameters[key] = {"value": dict_value, "type": "time_series"}
        else:
            self.direct_parameters[key] = {"value": value, "type": type_}

    def get_direct_parameter(self, key: str):
        if key not in self.direct_parameters:
            return None
        return self.direct_parameters[key]
    
    def get_name(self):
        return self.name
    



