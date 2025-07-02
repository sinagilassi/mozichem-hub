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
            }
        ],
    }
]
