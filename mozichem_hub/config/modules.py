# import libs

# local

MCP_MODULES = [
    {
        'name': 'eos-models-mcp',
        'version': '0.1.0',
        'description': 'The module for calculating thermodynamic properties using different EOS models.',
        'instructions': 'This module provides tools for calculating the fugacity of components in gas and liquid phases using various EOS models.',
        'package': 'PyThermoModels',
        'id': 'PTMCore',
        'class': 'MCP_PTMCore',
        'descriptor': 'ptmcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
            {
                'name': 'get_method_reference_inputs',
                'description': 'Retrieves the reference inputs required for a specific method, including data and equations.'
            },
            {
                'name': 'calc_gas_component_fugacity',
                'description': 'Calculates the fugacity of a gas-phase component at given temperature and pressure.',
            },
            {
                'name': 'calc_liquid_component_fugacity',
                'description': 'Calculates the fugacity of a liquid-phase component at given temperature and pressure.'
            },
            {
                'name': 'calc_fugacity_gas_mixture',
                'description': 'Calculates the fugacity of a gaseous mixture of components at given temperature and pressure.',
            },
            {
                'name': 'component_eos_roots_analysis',
                'description': 'Analyzes the roots of the EOS for a given component at specified temperature and pressure.'
            },
            {
                'name': 'multi_component_eos_roots_analysis',
                'description': 'Analyzes the roots of the EOS for a mixture of components at specified temperature and pressure.'
            }
        ],
    },
    {
        'name': 'flash-calculations-mcp',
        'version': '0.1.0',
        'description': 'The module for performing flash calculations using pyThermoFlash.',
        'instructions': 'This module provides tools for performing flash calculations using pyThermoFlash. Bubble pressure, dew pressure, bubble temperature, dew temperature, and flash calculations are all supported.',
        'package': 'PyThermoFlash',
        'id': 'PTFCore',
        'class': 'MCP_PTFCore',
        'descriptor': 'ptfcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
            {
                'name': 'calc_bubble_pressure_ideal_vapor_ideal_liquid',
                'description': 'Calculates the bubble pressure of a mixture at a given temperature using raoult`s law (ideal vapor and ideal liquid).'
            },
            {
                'name': 'calc_dew_pressure_ideal_vapor_ideal_liquid',
                'description': 'Calculates the dew pressure of a mixture at a given temperature using raoult`s law (ideal vapor and ideal liquid).'
            },
            {
                'name': 'calc_bubble_temperature_ideal_vapor_ideal_liquid',
                'description': 'Calculates the bubble temperature of a mixture at a given pressure using raoult`s law (ideal vapor and ideal liquid).'
            },
            {
                'name': 'calc_dew_temperature_ideal_vapor_ideal_liquid',
                'description': 'Calculates the dew temperature of a mixture at a given pressure using raoult`s law (ideal vapor and ideal liquid).'
            },
            {
                'name': 'calc_flash_isothermal_ideal_vapor_ideal_liquid',
                'description': 'Calculates the flash calculation for a liquid mixture at a specified temperature, determining the vapor and liquid phase compositions using Raoult\'s law for ideal vapor and ideal liquid.'
            }
        ],
    },
    {
        'name': 'thermodynamic-properties-mcp',
        'version': '0.1.0',
        'description': 'The module for accessing thermodynamic properties of components from different sources.',
        'instructions': 'This module provides tools for accessing thermodynamic properties of components from different sources. It includes properties from different thermodynamic books and databases.',
        'package': 'PyThermoDB',
        'id': 'PTDBCore',
        'class': 'MCP_PTDBCore',
        'descriptor': 'ptdbcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
            {
                'name': 'search_component_for_thermodynamic_properties',
                'description': 'This tool checks if the thermodynamic properties of a specified chemical component are available in the database. It returns a string indicating the availability status of the component\'s properties. Normally, it returns a list of available properties with its name, symbol, databook, and table name.'
            },
            {
                'name': 'get_databook_descriptions',
                'description': 'Get the descriptions of all available databooks in the PTDB database.'
            },
            {
                'name': 'get_databooks_descriptions',
                'description': 'Get information about a specific databook.'
            },
            {
                'name': 'verify_component_availability',
                'description': 'Verify if a component is available in the PTDB database for a specific databook and table.'
            },
            {
                'name': 'get_list_databooks',
                'description': 'Get the list of all available databooks in the PTDB database.'
            },
            {
                'name': 'get_list_tables',
                'description': 'Get the list of all tables in a specific databook.'
            },
            {
                'name': 'get_table_information',
                'description': 'Get information about a specific table in a databook. It returns the table type including Equations, Data, Matrix-Equations, and Matrix-Data. Moreover, it returns the number of each type of data in the table.'
            },
            {
                'name': 'get_table_structure',
                'description': 'Get the structure of a specific table in a databook.'
            },
            {
                'name': 'get_table_data',
                'description': 'Get the data of a specific table in a databook.'
            },
            {
                'name': 'get_databook_id',
                'description': 'Get the ID of a specific databook.'
            },
            {
                'name': 'get_table_id',
                'description': 'Get the ID of a specific table in a databook.'
            },
            {
                'name': 'get_table_description',
                'description': 'Get the description of a specific table in a databook.'
            },
            {
                'name': 'get_equation_structure',
                'description': 'Get the equation structure of a specific table in a databook.'
            }
        ]
    }
]
