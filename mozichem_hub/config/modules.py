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
                'name': 'verify_component_thermodynamic_properties_availability',
                'description': 'Verify the availability of thermodynamic properties for a given component in the database. It returns a list of available properties and their sources.'
            }
        ]
    }
]
