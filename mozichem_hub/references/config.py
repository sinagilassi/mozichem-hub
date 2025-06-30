# import libs
from typing import Dict
from .models import ComponentPropertySource
# locals

# SECTION: default reference config
REFERENCE_CONFIG: Dict[str, ComponentPropertySource] = {
    'heat-capacity': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='ideal-gas-molar-heat-capacity',
        mode='EQUATIONS',
        label='Cp_IG'
    ),
    'vapor-pressure': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='vapor-pressure',
        mode='EQUATIONS',
        label='VaPr'
    ),
    'general': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='general-data',
        mode='DATA',
        labels={
            'Pc': 'Pc',
            'Tc': 'Tc',
            'AcFa': 'AcFa',
        }
    )
}

REFERENCE_CONFIGS: Dict[str, Dict[str, ComponentPropertySource]] = {
    "ALL": REFERENCE_CONFIG,
    "carbon dioxide-g": REFERENCE_CONFIG
}
