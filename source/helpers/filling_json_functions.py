# "entity_classes" : Keep the entire
# "entities": Keep the one from template and add item as follows:
        # ["unit__from_node",["unit_a","fuel"],None]
        # ["node", "electricity", None]
        # unit__node__node...
# Need to create a key entity_alternatives and add the following:
        # ["model",["simple" ],"Base",True]
        # ["report__output",["report1","unit_flow"],"Base",True]
        # ["unit__to_node",["unit_b", "electricity"], "Base", True]
    # NOT UNIT__NODE__NODE ?? without the component using more than 2 entities like unit__node__node or connection__node__node
# parameter_value_lists : Keep the entire
# parameter_definitions : Weird...  -> Keep the entire
# parameter_values: 
        # ["node", "electricity", "demand", 150.0,"Base"]
        # ["temporal_block", "operation","resolution",{"data": "1D","type": "duration"},"Base"]
        # ["unit__node__node",["unit_a","electricity","fuel"],"fix_ratio_out_in_unit_flow", 0.7, "Base"]

# Time serie: {"index": {"start": "2000-01-01 00:00:00","resolution": "1h","ignore_year": true,"repeat": true},"data": [3.685,3.722,3.717,4.166,4.296],"type": "time_series"}
# {"data": {"2000-01-01T00:00:00": 100.0,"2000-01-01T03:00:00": 2.0,"2000-01-01T07:00:00": 150.0},"type": "time_series"}
# alternatives: Keep the entire

def add_entity(data, entity, name_s):
    data["entities"].append([entity, name_s, None])
    data["entity_alternatives"].append([entity, name_s, "Base", True])
    return data

def add_parameter_value(data, entity, name_s, tech, val, type_):
    if type_ == "duration":
        val=  {"data": val, "type": "duration"}
    elif type_ == "datetime":
        val = {"data": val.strftime("%Y-%m-%dT%H:%M:%S"), "type": "date_time"}
    elif type_ == "time_series":
        val = {"index": val[0],
                "data": val[1],
               "type": "time_series"}
    data["parameter_values"].append([entity, name_s, tech, val, "Base"])
    return data

