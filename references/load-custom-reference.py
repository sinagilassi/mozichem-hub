# import libs
import os
from typing import Dict, List, Any
from rich import print
import pyThermoDB as ptdb
from pyThermoDB.references import (
    ThermoDatabook,
    ThermoReference
)

# SECTION: create a new databook instance
databook_name = "CUSTOM-REFERENCE"
databook = ThermoDatabook(databook_name)

# SECTION: sources
# current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# ! general data
# NOTE: csv file path
general_data = os.path.join(current_dir, "General Data.csv")
print(f"General data file: {general_data}")

# table name
general_data_table_name = "general-data"

# add general data table
databook.add_data_table(
    general_data_table_name,
    general_data,
    description="General data for mozichem-hub."
)

# get the table by name
general_data_table = databook.tables[general_data_table_name]
print(f"General Data Table: {general_data_table}")
# description of the table
print(f"Description: {general_data_table.description}")

# ! vapor pressure equation
# NOTE: csv file path
vapor_pressure_equation = os.path.join(current_dir, "Vapor Pressure.csv")
print(f"Vapor Pressure file: {vapor_pressure_equation}")

# equation body
equation_body = "f([vapor-pressure, VaPr, Pa] | [Temperature, T, K] | C1, C2, C3, C4, C5) = math.exp(C1 + C2/T + C3*math.log(T) + C4*(T**C5))"

# table name
vapor_pressure_table_name = "vapor-pressure"

# add vapor pressure equation table
databook.add_equation_table(
    table_name=vapor_pressure_table_name,
    data=vapor_pressure_equation,
    equations=equation_body,
    description="Vapor pressure equation for mozichem-hub."
)

# SECTION: build the databook
databook.build()
# databook
print(f"Databook built with ID: {databook.databook_id}")
# print the databook
print(f"Databook Description: {databook.description}")
# contents of the databook
databook_contents = databook.get_contents(res_format='yml')
print(f"Databook Contents: {databook_contents}")

# NOTE: save the contents to a file
# output_file = os.path.join(current_dir, "custom-databook.yml")
# databook.save_contents(output_file, res_format='yml')

# SECTION: custom reference
# custom ref
ThermoReference_ = ThermoReference()
# create a new databook
ThermoReference_.add_databook(databook)

# build references
ThermoReference_.build_references()

# NOTE: get references
references = ThermoReference_.get_references(res_format='yml')
# references = ThermoReference_.get_references(res_format='dict')
print(f"References: {references}")

# NOTE: save the references to a file
output_file = os.path.join(current_dir, "custom-references.yml")
ThermoReference_.save_references(output_file, res_format='yml')

# SECTION: initialize own thermo db
# custom ref
ref: Dict[str, Any] = {'reference': [references]}
# md ref
# ref = {'reference': [md_path]}
# yml ref
# ref = {'reference': [yml_path]}

# ====================================
# ! method 1
# NOTE: BUILD COMPONENT THERMODB
# ====================================
# property
reference_config = {
    'vapor-pressure': {
        'databook': databook_name,
        'table': vapor_pressure_table_name,
    },
    'general': {
        'databook': databook_name,
        'table': general_data_table_name,
    },
}
thermodb_component_ = ptdb.build_component_thermodb(
    component_name='carbon dioxide',
    reference_config=reference_config,
    custom_reference=ref)

#  check
print(thermodb_component_.check())
print(thermodb_component_.message)

# ====================================
# ! method 2
# NOTE: INITIALIZATION OWN THERMO DB
# ====================================
thermo_db = ptdb.init(custom_reference=ref)

# ====================================
# GET DATABOOK LIST
# ====================================
db_list = thermo_db.list_databooks()
print(db_list)

# select reference
print(thermo_db.select_reference(databook_name))

# ====================================
# SELECT A DATABOOK
# ====================================
# table list
tb_list = thermo_db.list_tables(databook_name)
print(tb_list)

# NOTE: select a component
comp1 = "Carbon Dioxide"

# ====================================
# BUILD DATA
# ====================================
# build data
comp1_data = thermo_db.build_data(
    comp1,
    databook_name,
    general_data_table_name,
)
print(comp1_data.data_structure())

print(comp1_data.get_property(6, message=f"{comp1} Enthalpy of formation"))
# by symbol
print(float(comp1_data.get_property('gibbs-energy-of-formation')['value']))

# ====================================
# BUILD EQUATION
# ====================================
# build equation
vapor_pressure_eq = thermo_db.build_equation(
    comp1,
    databook_name,
    2
)

print(vapor_pressure_eq.equation_args())
print(vapor_pressure_eq.equation_return())
VaPr = vapor_pressure_eq.cal(message=f'{comp1} Vapor Pressure', T=304.21)
VaPr = vapor_pressure_eq.cal(T=304.21)
print(VaPr)
