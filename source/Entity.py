import datetime 

class Entity:
    def __init__(self, entity_type = None):
        self.direct_parameters : dict = {}
        # Generate a default name for the entity based on its type and the current timestamp
        if entity_type is not None:
            self.name = "default_name_" + entity_type + "_" + str(datetime.datetime.now().timestamp())[5:]
        else:
            self.name = "default_name_entity_" +  str(datetime.datetime.now().timestamp())[5:]
        self.location_name = ""
    
    def set_name(self, name: str):
        # Set the name of the entity
        self.name = name
    
    def set_location_name(self, name: str):
        # Set the location name of the entity
        self.location_name = name

    @property
    def full_name(self):
        # Combine the entity's name and location name into a full name
        return self.name + self.location_name

    def add_direct_parameter(self, key: str, data, data_type = None):
        # Add a parameter to the entity's direct_parameters dictionary
        if key == "name":
            # Special case: if the key is "name", update the entity's name
            self.name = data
        elif data_type == "Special":
            # Handle special data types
            self.direct_parameters[key] = {"value": data, "type": "string_special"}
        elif type(data) is str and "=" in data:
            # Handle time series data in the format year=value;year=value;...
            data = data.split(";")
            dict_timeserie = {}
            for i in range(len(data)):
                year = data[i].split("=")[0]
                value = data[i].split("=")[1]
                # Convert year to a datetime string
                year_datetime = datetime.datetime(int(year), 1, 1, 0, 0, 0).strftime("%Y-%m-%dT%H:%M:%S")
                dict_timeserie[year_datetime] = float(value)
            timeserie_data = {
                "data": dict_timeserie,
                "type": "time_series",
            }
            # Store the time series data in direct_parameters
            self.direct_parameters[key] = {"value": timeserie_data, "type": "time_series"}
        else:
            # Store other types of data in direct_parameters
            self.direct_parameters[key] = {"value": data, "type": data_type}

    def get_name(self):
        # Retrieve the name of the entity
        return self.name
    
    def has_investment(self):
        # Check if the entity has an investment by looking for specific keys in direct_parameters
        for key in self.direct_parameters.keys():
            if "investment_econ_lifetime" in key:
                return True
        return False
