# import libs
from typing import Dict
from .models import ComponentProperty

# SECTION: default reference config
REFERENCE_CONFIG: Dict[str, ComponentProperty] = {
    'heat-capacity': ComponentProperty(
        databook='CUSTOM-REF-1',
        table='ideal-gas-molar-heat-capacity',
        label='Cp_IG',
        labels=None
    ),
    'vapor-pressure': ComponentProperty(
        databook='CUSTOM-REF-1',
        table='vapor-pressure',
        label='VaPr',
        labels=None
    ),
    'general': ComponentProperty(
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

REFERENCE_CONFIGS: Dict[str, Dict[str, ComponentProperty]] = {
    "ALL": REFERENCE_CONFIG,
    "CO2": {
        'heat-capacity': ComponentProperty(
            databook='CUSTOM-REF-1',
            table='ideal-gas-molar-heat-capacity',
            label='Cp_IG',
            labels=None
        ),
        'vapor-pressure': ComponentProperty(
            databook='CUSTOM-REF-1',
            table='vapor-pressure',
            label='VaPr',
            labels=None
        ),
        'general': ComponentProperty(
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
}
