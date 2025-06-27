# import libs
from pyThermoDB.references import ReferenceConfig
from mozichem_hub.references import ReferencesAdapter
from rich import print

# NOTE:
reference_config = {
    "CO2":
    {
        'heat-capacity': {
            'databook': 'CUSTOM-REF-1',
            'table': 'Ideal-Gas-Molar-Heat-Capacity',
        },
        'vapor-pressure': {
            'databook': 'CUSTOM-REF-1',
            'table': 'Vapor-Pressure',
        },
        'general': {
            'databook': 'CUSTOM-REF-1',
            'table': 'General-Data',
        },
    }
}

reference_config_yml = """
CO2:
  heat-capacity:
    databook: CUSTOM-REF-1
    table: Ideal-Gas-Molar-Heat-Capacity
    label: Cp_IG
  vapor-pressure:
    databook: CUSTOM-REF-1
    table: Vapor-Pressure
    label: VaPr
  general:
    databook: CUSTOM-REF-1
    table: General-Data
    labels:
      Pc: Pc
      Tc: Tc
      AcFa: AcFa
CO:
  heat-capacity:
    databook: CUSTOM-REF-1
    table: Ideal-Gas-Molar-Heat-Capacity
    label: Cp_IG
  vapor-pressure:
    databook: CUSTOM-REF-1
    table: Vapor-Pressure
    label: VaPr
  general:
    databook: CUSTOM-REF-1
    table: General-Data
    labels:
      Pc: Pc
      Tc: Tc
      AcFa: AcFa
"""


# SECTION: Create a ReferenceConfig instance
# ref_config = ReferenceConfig().set_reference_config(
#     reference_config=reference_config_yml,)
# print(ref_config)

# SECTION: Create a ReferencesAdapter instance
ref_adapter = ReferencesAdapter()

adapted_config = ref_adapter.adapt_reference_config(
    reference_config=reference_config_yml,
)
print(adapted_config)
