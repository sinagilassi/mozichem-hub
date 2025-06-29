# import libs

# local

MCP_MODULES = [
    {
        'name': 'eos-models-mcp',
        'version': '0.1.0',
        'description': 'The module for calculating thermodynamic properties using different EOS models.',
        'package': 'PyThermoModels',
        'class': 'MCP_PTMCore',
        'descriptor': 'ptmcore.yml',
        'resources': [],
        'prompts': [],
        'tools': [
            {
                'name': 'cal_fugacity',
                'description': 'Calculates the fugacity of a component at given temperature and pressure.',
            },
            {
                'name': 'cal_fugacity_mixture',
                'description': 'Calculates the fugacity of a mixture of components at given temperature and pressure.',
            }
        ],
    }
]
