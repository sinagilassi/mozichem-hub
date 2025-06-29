# import libs
from typing import Dict, List
from .models import ComponentPropertySource
# locals

# SECTION: default reference config
REFERENCE_CONFIG: Dict[str, ComponentPropertySource] = {
    'heat-capacity': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='ideal-gas-molar-heat-capacity',
        label='Cp_IG',
        labels=None
    ),
    'vapor-pressure': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='vapor-pressure',
        label='VaPr',
        labels=None
    ),
    'general': ComponentPropertySource(
        databook='CUSTOM-REF-1',
        table='general-data',
        label=None,
        labels={
            'Pc': 'Pc',
            'Tc': 'Tc',
            'AcFa': 'AcFa',
        }
    )
}

REFERENCE_CONFIGS: Dict[str, Dict[str, ComponentPropertySource]] = {
    "ALL": REFERENCE_CONFIG,
}
