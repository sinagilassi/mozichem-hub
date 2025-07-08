# import libs

# local

MCP_MODULES = [
    {
        'name': 'eos-models-mcp',
        'version': '0.1.0',
        'description': 'The module for calculating thermodynamic properties using different EOS models.',
        'instructions': 'This module provides tools for calculating the fugacity of components in gas and liquid phases using various EOS models.',
        'package': 'PyThermoModels',
        'class': 'MCP_PTMCore',
        'descriptor': 'ptmcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
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
        'class': 'MCP_PTFCore',
        'descriptor': 'ptfcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
            {
                'name': 'calc_bubble_pressure',
                'description': 'Calculates the bubble pressure of a mixture at a given temperature using specified equilibrium model.'
            },
            # {
            #     'name': 'calc_dew_pressure',
            #     'description': 'Calculates the dew pressure of a mixture at a given temperature using specified equilibrium model.'
            # },
            # {
            #     'name': 'calc_bubble_temperature',
            #     'description': 'Calculates the bubble temperature of a mixture at a given pressure using specified equilibrium model.'
            # },
            # {
            #     'name': 'calc_dew_temperature',
            #     'description': 'Calculates the dew temperature of a mixture at a given pressure using specified equilibrium model.'
            # },
            # {
            #     'name': 'flash_calculation',
            #     'description': 'Performs flash calculations for a mixture at given temperature and pressure.'
            # }
        ],
    }
]
