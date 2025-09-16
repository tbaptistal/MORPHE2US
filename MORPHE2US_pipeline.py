# %%


# %%
import pandas as pd 
import copy
import numpy as np
import datetime as datetime
import json
import os
import argparse
from source.Node import Node
from source.Unit import Unit
from source.Municipality import Municipality
from source.District import District
from source.Building import Building
from source.Model import Model, Temporal_block, Report
from source.Connection import Connection
from source.Storage import Storage

def process_files(excel_filename, output_filename):
    print(f"Reading from: {excel_filename}")
    print(f"Writing to: {output_filename}")

    df_alternative = pd.read_excel(excel_filename, sheet_name='Specifications', header=1)
    df_alternative = df_alternative.loc[:, ~df_alternative.columns.str.contains('^Unnamed')]
    scenarios = (list(df_alternative.columns[1:]))
    print(f"Scenarios found: {scenarios}")
 
    df_specifications = pd.read_excel(excel_filename, sheet_name='Specifications')
    
    for i in range(len(scenarios)):
        scenario_name = scenarios[i]    
        df_specs = df_specifications.iloc[:, [0, 1, 2, 3, i+4]]  # Columns: type, name, and values
        print(f"Filling the model for scenario: {scenario_name}")

        # Removes the caracters in column if it's value.1 or value.2: replace it to value
        df_specs.columns = df_specs.columns.str.replace(r'value\.\d+', 'value', regex=True)




        # %%
        ## GENERAL COMMODITIES IN THE DICTIONARY ##

        df_commodities = pd.read_excel(excel_filename, sheet_name='Commodities', header=1)
        commodities_names = [col for col in df_commodities.columns if not col.startswith("Unnamed") and not col.startswith("Name") and not col.startswith("code")]
        df_commodities_NaM = df_commodities.set_index("code")

        # Initialize dictionaries to store general nodes and mandatory units
        dict__general_nodes = {}
        dict__mandatory_units = {}

        # Iterate through each commodity to create nodes and mandatory units (overflow units are mandatory once the commodity has overflow lost)
        for commodity in commodities_names:
            new_node = Node()
            new_node.set_name(commodity)
            
            # Check if the commodity has overflow lost and add the corresponding parameter and unit
            if "NaM_overflow_lost" in df_commodities_NaM.index:
                if df_commodities_NaM.loc["NaM_overflow_lost", commodity] == True:
                    print(f"Overflow {commodity}")
                    new_node.add_direct_parameter('NaM_overflow_lost', True, 'boolean')
                    unit = Unit()
                    unit.set_name(f"Overflow_{commodity}")
                    unit.add_direct_parameter("NaM_unit__from_node1", commodity, 'string')
                    dict__mandatory_units[f"Overflow_{commodity}"] = unit
            
            # Check if the commodity has a balance type and add the corresponding parameter
            if "NaM_balance_type" in df_commodities_NaM.index:
                if df_commodities_NaM.loc["NaM_balance_type", commodity] == True:
                    print(f"Balance type None for {commodity}")
                    new_node.add_direct_parameter('balance_type', "balance_type_none", 'string')
            
            # Add the node to the general nodes dictionary
            dict__general_nodes[commodity] = new_node


        # Special node for CO2
        new_node = Node()
        new_node.set_name('CO2')
        dict__general_nodes['CO2'] = new_node

        # %%
        ## GENERAL UNITS IN THE DICTIONARY ##


        df_units = pd.read_excel(excel_filename, sheet_name='Units', header=2)
        df_units = df_units.loc[:, ~df_units.columns.str.contains('^Unnamed')]

        # Magic number: 3 from the total number of columns 3 columns are known to be non-unit
        nb_units = df_units.shape[1] - 3


        df_units = pd.read_excel(excel_filename, sheet_name='Units')
        dict__general_units = {}

        # Iterate through each unit to create and populate unit objects
        for i in range(nb_units):
            df_unit = df_units.iloc[:, [1, 2, i+3]]  # 1, 2, i+3 are magic numbers for the columns 
            df_unit = df_unit.dropna()

            # Create a new unit object and fill the parameters
            new_unit = Unit()
            for index, row in df_unit.iterrows():
                type_ = row.iloc[0]  # Parameter type
                tech_name = row.iloc[1]  # Parameter name
                value = row.iloc[2]  # Parameter value
                new_unit.add_direct_parameter(tech_name, value, type_)

            # Activate CO2 relations within the unit
            new_unit.add_co2()

            # Check if the unit has investment options, the lifetime sense needs to be set to ==
            if new_unit.has_investment():
                new_unit.add_direct_parameter("unit_investment_lifetime_sense", "==", "Special")

            dict__general_units[new_unit.get_name()] = new_unit

        # %%
        ## GENERAL STORAGES IN THE DICTIONARY ##


        df_storages = pd.read_excel(excel_filename, sheet_name='Storages', header=2)
        df_storages = df_storages.loc[:, ~df_storages.columns.str.contains('^Unnamed')]

        # Magic number: 3
        nb_storages = df_storages.shape[1] - 3


        df_storages = pd.read_excel(excel_filename, sheet_name='Storages')
        dict__general_storages = {}

        # Iterate through each storage column to create and populate storage objects
        for i in range(nb_storages):
            # Extract one by one each storage column
            df_storage = df_storages.iloc[:, [1, 2, i+3]]
            df_storage = df_storage.dropna()

            
            new_storage = Storage()
            new_storage.add_direct_parameter("initial_node_state(node)", 0, "float")

            # Add parameters to the storage object from the DataFrame
            for index, row in df_storage.iterrows():
                type_ = row.iloc[0]  # Parameter type
                tech_name = row.iloc[1]  # Parameter name
                value = row.iloc[2]  # Parameter value
                new_storage.add_direct_parameter(tech_name, value, type_)

            # Add a special investment lifetime sense parameter if the storage has investment options
            if new_storage.has_investment():
                new_storage.add_direct_parameter("_investment_lifetime_sense(unit_and_node)", "==", "Special")

            dict__general_storages[new_storage.get_name()] = new_storage

        # %%
        ## GENERAL BUILDING TYPES IN THE DICTIONARY ##

        # Read the 'Building types' sheet from the Excel file and remove unnamed columns
        df_buildings = pd.read_excel(excel_filename, sheet_name='Building types', header=1)
        df_buildings = df_buildings.loc[:, ~df_buildings.columns.str.contains('^Unnamed')]
        nb_buildings = df_buildings.shape[1] - 1

        dict__general_building_types = {}

        # Iterate through each building type to create and populate building objects
        for i in range(nb_buildings):
            df_building = df_buildings.iloc[:, [0, i+1]]
            type_ = df_building.iloc[0, 1]  # Extract building type
            construction_year = df_building.iloc[1, 1]  # Extract construction year
            new_building = Building(str(df_building.columns[1]), type_, construction_year)  # Create a new building object

            # Extract retrofit information for the building
            df_retrofits = df_building.loc[df_building[df_building["name"] == "Retrofits"].index[0]:]
            indexes = df_retrofits[df_retrofits["name"] == "Commodity"].index

            # Iterate through each retrofit and add it to the building
            for index in indexes:
                df_retrofit = df_retrofits.loc[index-1:index+3].dropna()
                if df_retrofit.empty:
                    break
                name = df_retrofit.iloc[0, 1]  # Retrofit name
                commodity_to_invest = df_retrofit.iloc[1, 1]  # Commodity to invest in
                retrofit_increase_performance = df_retrofit.iloc[2, 1]  # Performance increase due to retrofit
                retrofit_cost = df_retrofit.iloc[3, 1]  # Cost of the retrofit
                new_building.add_retrofit(name, commodity_to_invest, retrofit_increase_performance, retrofit_cost)

            # Add general nodes and mandatory units to the building
            for key in dict__general_nodes.keys():
                new_building.add_node(copy.deepcopy(dict__general_nodes[key]))
            for key in dict__mandatory_units.keys():
                new_building.add_unit(copy.deepcopy(dict__mandatory_units[key]))

            dict__general_building_types[new_building.name] = new_building

        # %%
        ## GENERAL CONNECTIONS TYPES IN THE DICTIONARY ##	

        # Read the 'Connections' sheet from the Excel file and remove unnamed columns
        df_connections = pd.read_excel(excel_filename, sheet_name='Connections', header=2)
        df_connections = df_connections.loc[:, ~df_connections.columns.str.contains('^Unnamed')]

        # Calculate the number of connections by excluding the first 3 known non-connection columns
        nb_connections = df_connections.shape[1] - 3

        # Reload the 'Connections' sheet to ensure all data is available
        df_connections = pd.read_excel(excel_filename, sheet_name='Connections')

        # Initialize a dictionary to store general connection objects
        dict__general_connections = {}

        # Iterate through each connection to create and populate connection objects
        for i in range(nb_connections):
            # Extract relevant columns for the current connection
            df_connection = df_connections.iloc[:, [1, 2, i+3]]  # Columns: type, name, and values
            df_connection = df_connection.dropna()

            # Create a new connection object and populate its parameters
            new_connection = Connection()
            for index, row in df_connection.iterrows():
                type_ = row.iloc[0]  # Parameter type
                tech_name = row.iloc[1]  # Parameter name
                value = row.iloc[2]  # Parameter value
                new_connection.add_direct_parameter(tech_name, value, type_)

            # Add a special investment lifetime sense parameter if the connection has investment options
            if new_connection.has_investment():
                new_connection.add_direct_parameter("connection_investment_lifetime_sense", "==", "Special")

            dict__general_connections[new_connection.get_name()] = new_connection

        # %%
        ## CREATING THE MUNICIPALITY AND THE DISTRICTS WITHIN IT ##

        # Create a Municipality object
        municipality = Municipality("Municipality_name")

        # Read the 'Districts' sheet from the Excel file
        df_districts = pd.read_excel(excel_filename, sheet_name='Districts', header=1)

        # Extract district names from the columns, excluding unnamed and 'Name' columns
        districts_names = [col for col in df_districts.columns if not col.startswith("Unnamed") and not col.startswith("Name")]

        start = None
        list_district = []

        # Iterate through district names to allocate parts of the dataframe to each district
        for i, district in enumerate(districts_names):
            for index, col in enumerate(df_districts.columns):
                # Identify the start column for the current district
                if col == districts_names[i]:
                    start = index
                    # If it's the last district, include all remaining columns
                    if i == len(districts_names) - 1:
                        list_index = [1] + list(range(start, df_districts.shape[1])) 
                        list_district.append(df_districts.iloc[:, list_index])
                        break
                # Identify the end column for the current district
                if start != None and col == districts_names[i+1]:
                    end = index
                    list_index = [1] + list(range(start, end)) 
                    list_district.append(df_districts.iloc[:, list_index])
                    start = None

        # Remove rows with missing 'Name' values for each district dataframe
        for index, district in enumerate(list_district):
            list_district[index] = district.dropna(subset=["Name"])

        # %%
        # Specifications sheet : Magic numbers 
        general_parameters_str = "General"
        operational_parameters_str = "Operation"
        investements_parameters_str = "Economic - Investments"
        environnmental_parameters_str = "CO2"
        MGA_parameters_str = "Modeling to Generate Alternatives (MGA)"

        # %%
        ## BUILDING THE MODEL BASE ##
        df_specs_model = df_specs.iloc[df_specs[df_specs["Model"] == general_parameters_str].index[0]: df_specs[df_specs["Model"] == operational_parameters_str].index[0], :].dropna(subset=["code", "value"])

        model = Model()
        for j, row in df_specs_model.iterrows():
            model.add_direct_parameter(row.iloc[3], row.iloc[4], row.iloc[2])

        model.update_scenario_structure(scenario_name)

        # %%

        model_date_start = model.direct_parameters["model_start"]["value"]
        model_date_end = model.direct_parameters["model_end"]["value"]


        # Functions for timeseries handling from Excel # 
        def get_new_initial_investment_datetime(duration, value): 
            # Remove the duration from the date:
            # Example: duration can be 15Y
            years_ = int(duration.split("Y")[0]) if "Y" in duration else 0
            new_date_1 = model_date_start - datetime.timedelta(days=int(years_/2*365.25))
            new_date_2 = model_date_start + datetime.timedelta(days=int(years_/2*365.25))

            if new_date_2 > model_date_end:
                new_date_2 = model_date_end

            new_date_1 = new_date_1.strftime("%Y")
            new_date_2 = new_date_2.strftime("%Y")
            return f"{new_date_1} = {value} ; {new_date_2} = 0 ; {model_date_end.strftime('%Y')} = 0"



        def get_new_number_of_units_timeseries(NoU, lifetime):
            """
            NoU is "2020 = 3;  2021 = 4; 2023=2" 
            lifetime is "12Y"
            it means that the number of units will be 3 between 2020 and 2021, 3+4 between 2021 and 2023, 3+4+2 between 2023 and 2032
            Then it will be 4+2 between 2032 and 2033, and 2 between 2033 and 2035, and then 0 after 2035 until end of the modelization
            The output should be "2020 = 3; 2021 = 7; 2023 = 9; 2032 = 6; 2033 = 8; 2035 = 2; 2036 = 0; 2050 = 0"
            """
            lifetime_year = int(lifetime.split("Y")[0]) if "Y" in lifetime else 0

            NoU = NoU.split(";")
            NoU = [x.strip() for x in NoU]
            NoU = [x.split("=") for x in NoU]
            NoU = [[int(x[0]), int(x[1])] for x in NoU]
            NoU = sorted(NoU, key=lambda x: x[0])
            
            year_end = int(model_date_end.strftime('%Y'))
            NoU_new = {}
            for i in range(year_end-NoU[0][0]+1):
                NoU_new[NoU[0][0]+i] = 0
            
            for unit in NoU:
                NoU_new[unit[0]] += unit[1]
                for i in range(1, lifetime_year):
                    if unit[0]+i <= year_end:
                        NoU_new[unit[0]+i] += unit[1]
            
            # Writting it as "2020= 5; 2021= 5; 2022= 12; 2023= 20; 2024= 20; 2025= 20; 2026= 15; 2027= 15; 2028= 8; 2029= 0; 2030= 0"
            return "; ".join([f"{key} = {value}" for key, value in NoU_new.items()])
            
        # Test the functions # 5 units implemented in 2020, 7 more in 2022, 8 more in 2023, and a lifetime of 6 years 
        get_new_number_of_units_timeseries("2020=5; 2022=7; 2023=8", "6Y")

        # %%
        # FUNCTION TO EXTRACT AND ADD ENTITIES TO DISTRICTS - BUILDINGS #

        def extract_and_add_entities(df_district, district, idx0, idx1, dict__general):
            # Find the starting index for the entity section in the dataframe
            first_idx = df_district[df_district["Name"] == idx0].index[0]
            
            # Extract the relevant portion of the dataframe for the entities
            if idx1 == -1:
                df_district_entity = df_district.loc[(first_idx+1):, :]
            else: 
                last_idx = df_district[df_district["Name"] == idx1].index[0]
                df_district_entity = df_district.loc[(first_idx+1):(last_idx-1), :]
                
            # Iterate through each entity in the extracted dataframe
            for j, row in df_district_entity.iterrows():
                entity_name = row.iloc[0]
                new_entity = copy.deepcopy(dict__general[entity_name])

                if type(row.iloc[1]) == str:
                    # Handle time series for the number of units if it's a string
                    number_of_units = row.iloc[1]
                    if new_entity.has_investment():
                        # Find the lifetime parameter for the entity
                        for key in new_entity.direct_parameters.keys():
                            if "investment_econ_lifetime" in key:
                                break
                        lifetime = new_entity.direct_parameters[key]['value']
                        number_of_units = get_new_number_of_units_timeseries(number_of_units, lifetime)
                    else:
                        print(f"Warning: {entity_name} has a time series for the number of units but no investment")
                else:
                    # Handle static number of units if it's a number
                    number_of_units = 0 if np.isnan(row.iloc[1]) else int(row.iloc[1])
                    if number_of_units != 0 and new_entity.has_investment():
                        # Find the lifetime parameter for the entity
                        for key in new_entity.direct_parameters.keys():
                            if "investment_econ_lifetime" in key:
                                break
                        number_of_units = get_new_initial_investment_datetime(new_entity.direct_parameters[key]['value'], number_of_units)

                # Handle candidate units
                if type(row.iloc[2]) == str:
                    candidate_units = row.iloc[2]
                else: 
                    candidate_units = 0 if np.isnan(row.iloc[2]) else int(row.iloc[2])

                # Add parameters to the entity
                new_entity.add_direct_parameter("number_of_units", number_of_units)
                new_entity.add_direct_parameter("candidate_units", candidate_units)
                
                # Add the entity to the district if it has units or candidates
                if not (number_of_units == 0 and candidate_units == 0):
                    if isinstance(new_entity, Storage):
                        district.add_storage(new_entity)
                    if isinstance(new_entity, Unit):
                        district.add_unit(new_entity)
            return district

        # %%
        ## FILLING THE UNITS & STORAGES WITHIN THE DISTRICT AT DISTRICT LEVEL ## 

        # Iterate through each district in the list
        for i in range(len(list_district)):
            df_district = list_district[i]
            new_district = District(districts_names[i])

            # Add general nodes and mandatory units to the district
            for key in dict__general_nodes.keys():
                new_district.add_node(copy.deepcopy(dict__general_nodes[key]))
            for key in dict__mandatory_units.keys():
                new_district.add_unit(copy.deepcopy(dict__mandatory_units[key]))

            # Add units and storages at the district level
            new_district = extract_and_add_entities(df_district, new_district, "Units presence (district level)", "Units presence (building level)", dict__general_units)
            new_district = extract_and_add_entities(df_district, new_district, "Storages presence (district level)", "Storages presence (building level)", dict__general_storages)

            # Extract building-related data from the district dataframe
            columns_buildings = list(df_district.iloc[0, :])
            df_district_building = df_district.loc[df_district["Name"].isin(["Building types", "Quantity of building"])].dropna(axis=1).iloc[:, 1:].T
            df_district_building = df_district_building.reset_index()
            
            # Iterate through each building in the district
            for k, row in df_district_building.iterrows():
                building_name = row.iloc[1]
                building_quantity = row.iloc[2]
                
                if building_quantity == 0:
                    continue
                new_building = copy.deepcopy(dict__general_building_types[building_name])
                new_building.set_quantity(building_quantity)
                
                # Extract unit and storage data for the building
                df_building_district_unit = (df_district.iloc[:, [0, columns_buildings.index(building_name), columns_buildings.index(building_name) + 1]])

                # Add units and storages at the building level
                new_building = extract_and_add_entities(df_building_district_unit, new_building, "Units presence (building level)", "Storages presence (district level)", dict__general_units)
                new_building = extract_and_add_entities(df_building_district_unit, new_building, "Storages presence (building level)", -1, dict__general_storages)
                
                # Add the building to the district
                new_district.add_building(new_building)
            
            # Add the district to the municipality
            municipality.add_district(new_district)

        # %%
        ## BUILD THE CONNECTIONS BETWEEN THE DISTRICTS AND WITHIN THE DISTRICT ##


        df_connections = pd.read_excel(excel_filename, sheet_name='Commodities', header=1)
        indexes_connections = df_connections[df_connections["Name"] == "Connection"].index

        for commodity_name in commodities_names:
            # Extract relevant columns for the current commodity
            df_connections_commodity = df_connections.iloc[:, [0, 1, 2, df_connections.columns.get_loc(commodity_name)]]
            
            for i, index in enumerate(indexes_connections):
                # Determine the range of rows for the current connection
                if i == len(indexes_connections) - 1:
                    df_connection_commodity = df_connections_commodity.loc[(index+1):, :].dropna(subset=[commodity_name])
                else:
                    df_connection_commodity = df_connections_commodity.loc[(index+1): indexes_connections[i+1]-2, :].dropna(subset=[commodity_name])
                
                if df_connection_commodity.empty:
                    continue
                
                # Extract the connection name
                connection_name = [row.iloc[3] for index_row, row in df_connection_commodity.iterrows() if row.iloc[2] == "name"][0]
                connection = copy.deepcopy(dict__general_connections[connection_name])
                
                # Add parameters to the connection object
                for index_row, row in df_connection_commodity.iterrows():
                    if row.iloc[2] == "candidate_connections" and float(row.iloc[3]) == 0:
                        continue
                    connection.add_direct_parameter(row.iloc[2], float(row.iloc[3]) if row.iloc[1] == "float" else row.iloc[3], row.iloc[1])

                # Extract district and building information for the connection
                district_from = connection.direct_parameters["NaM_district_lvl(from_node)"]["value"] if "NaM_district_lvl(from_node)" in connection.direct_parameters.keys() else None
                building_from = connection.direct_parameters["NaM_building_lvl(from_node)"]["value"] if "NaM_building_lvl(from_node)" in connection.direct_parameters.keys() else None
                district_to = connection.direct_parameters["NaM_district_lvl(to_node)"]["value"] if "NaM_district_lvl(to_node)" in connection.direct_parameters.keys() else None
                building_to = connection.direct_parameters["NaM_building_lvl(to_node)"]["value"] if "NaM_building_lvl(to_node)" in connection.direct_parameters.keys() else None

                # print(f"Connection: {connection_name} {commodity_name} {district_from},{building_from} {district_to},{building_to}")
                
                # This part could be done directly within the municipality class but like this it is easier to debug

                # Handle district-to-district connections
                if district_from != None and building_from == None and district_to != None and building_to == None:
                    municipality.add_district_interconnection(connection, commodity_name, district_from, district_to)

                # Handle district-to-building connections
                if district_from != None and building_from == None and district_to != None and building_to != None:
                    if district_from != district_to: 
                        print("Error in the building to district connection: It should be the same district")
                    for district in municipality.districts:
                        if district.get_name() in district_from:
                            district.add_building_connection(connection, commodity_name, building_to, flag_direction_building="to")
                        
                # Handle building-to-district connections
                if district_from != None and building_from != None and district_to != None and building_to == None:
                    if district_from != district_to: 
                        print("Error in the building to district connection: It should be the same district")
                    for district in municipality.districts:
                        if district.get_name() in district_to:
                            district.add_building_connection(connection, commodity_name, building_from, flag_direction_building="from")


        # %%
        ## BUILD THE REPORTS IN THE MODEL ##

        df_reports = pd.read_excel(excel_filename, sheet_name='Reports')
        df_reports = df_reports.loc[:, ~df_reports.columns.str.contains('^Unnamed')]
        df_reports = df_reports.iloc[:, df_reports.columns.get_loc("code"):]
        nb_reports = df_reports.shape[1] - 1 # Only 1 column (code) + all the reports  

        for i in range(nb_reports):
            df_report = df_reports.iloc[:, [0, i+1]]
            report = Report(df_report.columns[1])
            for index, row in df_report.iterrows():
                if row.iloc[1] == True:
                    report.add_output(row.iloc[0])
            if report.get_output_list_length() > 0:
                model.add_report(report)

        # %%
        ## Building the operations of the model

        # Extract the operations from the df_specs
        df_specs_operation = df_specs.iloc[df_specs[df_specs["Model"] == operational_parameters_str].index[0]: df_specs[df_specs["Model"] == investements_parameters_str].index[0], :].dropna(subset=["code", "value"])

        # Check if linear operation mode is enabled
        if (list(df_specs_operation[df_specs_operation["code"] == "NaM_linear_op"].value))[0] == True:
            # Extract the relevant rows for linear operation
            df_specs_operation = df_specs.iloc[(df_specs[df_specs["code"] == "NaM_linear_op"].index[0]+1): df_specs[df_specs["code"] == "NaM_bool_specific_year"].index[0], :].dropna(subset=["code", "value"])
            operation = Temporal_block()
            # Add parameters for the linear operation block
            for j, row in df_specs_operation.iterrows():
                operation.add_direct_parameter(row.iloc[3], row.iloc[4], row.iloc[2])
            operation.add_direct_parameter("block_start", model.direct_parameters["model_start"]["value"], model.direct_parameters["model_start"]["type"])
            operation.add_direct_parameter("block_end", model.direct_parameters["model_end"]["value"], model.direct_parameters["model_end"]["type"])
            model.add_operation(operation)

        # Check if specific year operation mode is enabled
        elif (list(df_specs_operation[df_specs_operation["code"] == "NaM_bool_specific_year"].value))[0] == True:
            # Extract the relevant rows for specific year operation
            df_specs_operation = df_specs.iloc[(df_specs[df_specs["code"] == "NaM_bool_specific_year"].index[0]+1): df_specs[df_specs["code"] == "NaM_Representative_days"].index[0], :].dropna(subset=["code", "value"])
            specific_years = (list(df_specs_operation[df_specs_operation["code"] == "NaM_specific_year"].value))[0]
            for year in specific_years.split(";"):
                year = int(year)
                start_date = datetime.datetime(year, 1, 1, 0, 0, 0)
                end_date = datetime.datetime(year+1, 1, 1, 0, 0, 0)
                model_start = model.direct_parameters["model_start"]["value"]
                model_end = model.direct_parameters["model_end"]["value"]
                operation = Temporal_block()
                # Skip years outside the model's time range
                if year > model_end.year or year < model_start.year:
                    continue
                # Adjust the block start and end dates based on the model's time range
                if start_date < model_start:
                    operation.add_direct_parameter("block_start", model_start, "date_time")
                else:
                    operation.add_direct_parameter("block_start", start_date, "date_time")
                if end_date > model_end:
                    operation.add_direct_parameter("block_end", model_end, "date_time")
                else:
                    operation.add_direct_parameter("block_end", end_date, "date_time")
                # Add resolution and name parameters for the operation block
                operation.add_direct_parameter("resolution", (list(df_specs_operation[df_specs_operation["code"] == "resolution"].value))[0], "duration")
                operation.add_direct_parameter("name", f'{(list(df_specs_operation[df_specs_operation["code"] == "name"].value))[0]}_{year}', "duration")
                model.add_operation(operation)

        # Check if representative days operation mode is enabled
        elif (list(df_specs_operation[df_specs_operation["code"] == "NaM_Representative_days"].value))[0] == True:
            print("Representative days to be implemented")


        # %%
        # Building the investments of the model

        # Read the df_specs sheet and extract the investment-related rows
        df_specs_investment = df_specs.iloc[df_specs[df_specs["Model"] == investements_parameters_str].index[0]:df_specs[df_specs["Model"] == environnmental_parameters_str].index[0], :].dropna(subset=["code", "value"])
        df_specs_investment = df_specs_investment.loc[:, ["type","code", "value"]]
        df_specs_investment.reset_index(drop=True, inplace=True)

        # Check if single investment mode is enabled
        if (list(df_specs_investment[df_specs_investment["code"] == "NaM_invstmt_sgl_bool"].value))[0] == True:
            # Extract rows for single investment
            df_specs_investment_sgl = df_specs_investment.iloc[df_specs_investment[df_specs_investment["code"] == "NaM_invstmt_sgl_bool"].index[0]+1:df_specs_investment[df_specs_investment["code"] == "NaM_invstmt_multi_bool"].index[0], :]
            investment = Temporal_block()
            # Add parameters for single investment
            for j, row in df_specs_investment_sgl.iterrows():
                investment.add_direct_parameter(row.iloc[1], row.iloc[2], row.iloc[0]) 
            investment.add_direct_parameter("block_end", model.direct_parameters["model_end"]["value"], model.direct_parameters["model_end"]["type"])
            investment.add_direct_parameter("resolution", "100Y", "duration")  # Set resolution for single investment
            model.add_investment(investment)

        # Check if multi-investment mode is enabled
        if (list(df_specs_investment[df_specs_investment["code"] == "NaM_invstmt_multi_bool"].value))[0] == True:
            # Extract rows for multi-investment
            df_specs_investment_multi = df_specs_investment.iloc[df_specs_investment[df_specs_investment["code"] == "NaM_invstmt_multi_bool"].index[0]+1:, :]
            investment = Temporal_block()
            # Add parameters for multi-investment
            for j, row in df_specs_investment_multi.iterrows():
                investment.add_direct_parameter(row.iloc[1], row.iloc[2], row.iloc[0])
            investment.add_direct_parameter("block_end", model.direct_parameters["model_end"]["value"], model.direct_parameters["model_end"]["type"])
            model.add_investment(investment)

        # Read the df_specs sheet and extract MGA-related rows
        df_specs_mga = df_specs.iloc[df_specs[df_specs["Model"] == MGA_parameters_str].index[0]:, :].dropna(subset=["code", "value"])
        df_specs_mga = df_specs_mga.loc[:, ["type", "code", "value"]]
        df_specs_mga.reset_index(drop=True, inplace=True)
        for j, row in df_specs_mga.iterrows():
            model.add_direct_parameter(row.iloc[1], row.iloc[2], row.iloc[0])

        # %%
        # Building the CO2 node and connections within the municipality 

        # Read the df_specs sheet and extract CO2-related rows
        
        df_specs_co2 = df_specs.iloc[df_specs[df_specs["Model"] == environnmental_parameters_str].index[0]:df_specs[df_specs["Model"] == MGA_parameters_str].index[0], :].dropna(subset=["code", "value"])
        df_specs_co2 = df_specs_co2.loc[:, ["type", "code", "value"]]
        df_specs_co2.reset_index(drop=True, inplace=True)

        # Check if CO2 modeling is enabled
        if (list(df_specs_co2[df_specs_co2["code"] == "NaM_CO2_bool"].value))[0] == True:
            # Extract rows for CO2
            df_specs_co2 = df_specs_co2.iloc[df_specs_co2[df_specs_co2["code"] == "NaM_CO2_bool"].index[0]+1:, :]    

            # Create and configure the CO2 node
            node_CO2 = Node()
            node_CO2.add_direct_parameter("has_state", True, "boolean")
            node_CO2.add_direct_parameter("initial_node_state", 0, "float")
            if len(list(df_specs_co2[df_specs_co2["code"] == "node_state_cap"].value)) > 0:
                node_capacity = list(df_specs_co2[df_specs_co2["code"] == "node_state_cap"].value)[0]
                node_CO2.add_direct_parameter("node_state_cap", node_capacity, "float")    
            node_CO2.add_direct_parameter("node_state_min", None)
            node_CO2.add_direct_parameter("name", "CO2")

            # Create and configure the CO2 connection
            CO2_connection = Connection()
            CO2_connection.add_direct_parameter("connection_type", "connection_type_lossless_bidirectional")
            CO2_connection.add_direct_parameter("name", "Connection_CO2_M-LVL")

            # Add the CO2 node and connection to the municipality
            municipality.add_node(node_CO2)
            municipality.add_CO2_connection(CO2_connection, "CO2")
        else:
            # If CO2 modeling is not enabled, set balance type for CO2 nodes
            for district in municipality.districts:
                for node in district.nodes:
                    if "CO2" in node.get_name():
                        node.add_direct_parameter("balance_type", "balance_type_none", "string")
                for building in district.buildings:
                    for node in building.nodes:
                        if "CO2" in node.get_name():
                            node.add_direct_parameter("balance_type", "balance_type_none", "string")


        # %%
        # Define the path to the directory containing JSON files
        path = 'data/'

        # List all files in the directory and filter for JSON files
        files = os.listdir(path)
        files = [f for f in files if f.endswith('.json')]

        vector_data_json = []

        # Load each JSON file and append its data to the vector_data_json list
        for file in files:
            with open(path + file) as f:
                data = json.load(f)
            print(f"File {file} loaded")
            vector_data_json += data

        # Iterate through the loaded JSON data
        for datajson in vector_data_json:
            if datajson["data"]["type"] == "float":
                data = datajson["data"]["data"]
            else:
                data = datajson["data"]

            # Add parameters to the municipality based on the type of data
            if datajson["commodity"] is not None:
                municipality.add_node_parameter(datajson["parameter_name"], datajson["district"], datajson["building"], datajson["commodity"], copy.deepcopy(data), datajson["data"]["type"], datajson["quantitative"])
            elif datajson["unit"] is not None:
                municipality.add_unit_parameter(datajson["parameter_name"], datajson["district"], datajson["building"], datajson["unit"], copy.deepcopy(data), datajson["data"]["type"])
            elif datajson["connection"] is not None:
                continue  # Skip connection-related data (not implemented)
            else:
                print("Error in the data")

        # %%
        # Load the template JSON file
        with open('source/template.json') as f:
            data_template = json.load(f)

        # Replace all "Base" occurrences in the template with the scenario name
        data_template = json.loads(json.dumps(data_template).replace("Base", scenario_name))


        # Check if building retrofit mode is enabled
        if (list(df_specs_investment[df_specs_investment["code"] == "NaM_building_retrofits"].value))[0] == True:
            # Add the retrofit mode for each building in all districts
            for district in municipality.districts:
                for building in district.buildings:
                    # Create retrofit mode for the building
                    building.create_building_retrofit_mode()

        # Add the municipality structure to the model
        model.add_modelisation_structure(municipality)

        # Export the updated model data to the template JSON
        data_to_export = model.export_json(data_template, scenario_name)

        
        # Save the updated template JSON to the output file
        with open(f'outputs/scenario_{scenario_name}-{output_filename}', 'w') as f:
            json.dump(data_to_export, f, indent=4)
        print(f"Export complete to scenario_{scenario_name}-{output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Excel files.")
    parser.add_argument("--excel", default="MORPHE2US.xlsx", help="Input Excel file path")
    parser.add_argument("--output", default="output.json", help="Output file path")
    args = parser.parse_args()
    process_files(args.excel, args.output)