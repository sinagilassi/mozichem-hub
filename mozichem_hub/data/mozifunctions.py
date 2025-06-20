# import libs
from typing import List, Dict, Annotated, Literal
from pydantic import Field
import pyThermoModels as ptm
# locals
from .datamodels import Temperature, Pressure, Component


class MoziFunctions:
    """
    MoziFunctions class for defining functions in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(self, datasource: dict):
        """
        Initialize the MoziFunctions instance.
        """
        # SECTION: Initialize the datasource
        # datasource
        self.datasource = datasource

        # SECTION: Initialize the ThermoModels instance
        # eos
        self.eos = ptm.eos()

    def cal_fugacity(
        self,
        component: Annotated[
            Component,
            Field(description="Component name and properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ],
    ) -> dict:
        """Calculates the fugacity of a component at given temperature and pressure"""
        try:
            # NOTE: extract component name
            (
                component_name, component_formula, component_state
            ) = component.name, component.formula, component.state

            # model input
            model_inputs = {
                # "phase": phase,
                "component": component_name,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }

            # NOTE: build component thermodb
            component_thermodb = ptdb.build_component_thermodb(
                component_name=component_name,
                property_source=property_source,
                custom_reference=ref)

            # NOTE: add component thermodb
            thub1.add_thermodb(component_name, component_thermodb)

            # standard thermodb config
            thub1.config_thermodb_rule(thermodb_config_content)

            # NOTE: build datasource & equationsource
            datasource, equationsource = thub1.build()

            model_source = {
                "datasource": datasource,
                "equationsource": equationsource
            }

            # NOTE: calc
            res = eos.cal_fugacity(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source
            )

            return res
        except Exception as e:
            raise ValueError(f"Failed to calculate fugacity: {e}") from e
