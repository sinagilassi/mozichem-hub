# import libs
from typing import List, Dict, Annotated, Literal, Optional
from pydantic import Field
import pyThermoModels as ptm
# locals
from .datamodels import (
    Temperature, Pressure, Component, CustomReference
)
from .thermodb import ThermoDB


class MoziFunctions:
    """
    MoziFunctions class for defining functions in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(
        self,
        custom_reference: Optional[CustomReference] = None,
    ):
        """
        Initialize the MoziFunctions instance.

        Parameters
        ----------
        thermodb_rule : str
            Rule for initializing the pyThermoLinkDB instance.
        """
        # SECTION: Initialize the ThermoDB instance
        self.thermodb = ThermoDB(custom_reference)

        # SECTION: Initialize the ThermoModels instance
        # eos
        self.eos = ptm.eos()

    def cal_fugacity(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        pressure: Annotated[
            Pressure,
            Field(..., description="Pressure of the system")],
        eos_model: Annotated[
            Literal['PR', 'SRK', 'RK', 'vdW'],
            Field(description="EOS model to use, e.g., 'SRK', 'PR'", default="SRK")
        ],
    ) -> dict:
        """Calculates the fugacity of a component at given temperature and pressure"""
        try:
            # NOTE: extract component name
            (
                component_name, _, _
            ) = component.name, component.formula, component.state

            # SECTION: build model source
            model_source = self.thermodb.build_component_model_source(
                component=component
            )

            # SECTION: model input
            model_inputs = {
                "component": component_name,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }

            # SECTION: calc
            res = self.eos.cal_fugacity(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to calculate fugacity: {e}") from e
