# import libs
from typing import Dict, Any, Callable, List
import inspect
from typing import Annotated, Literal
from pydantic import Field
import pyThermoModels as ptm
# local
from .models import (
    Temperature,
    Pressure,
    Component,
)
from .utils import set_feed_specification
from .hub import Hub


class PTMCore:
    """
    Core class for managing pyThermoModels (PTM) functionalities.
    This class serves as a central point for PTM-related operations.
    """
    # NOTE: attributes
    id = "PTMCore"

    def __init__(self, hub: Hub):
        """
        Initialize the PTMCore instance.
        """
        # NOTE: store the hub instance
        self.hub = hub

        # SECTION: build eos
        self.eos = ptm.eos()

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

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

            # component name - state
            component_ = f"{component_name}-{component.state}"

            # SECTION: build model source
            model_source = self.hub.build_component_model_source(
                component=component
            )

            # SECTION: model input
            model_inputs = {
                "component": component_,
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

    def cal_fugacity_mixture(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
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
            # SECTION: set feed specification
            N0s = set_feed_specification(
                components=components,
                feed_mode="formula"
            )

            # SECTION: build model source
            model_source = self.hub.build_components_model_source(
                components=components
            )

            # SECTION: model input
            model_inputs = {
                "feed-specification": N0s,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }

            # SECTION: calc
            res = self.eos.cal_fugacity_mixture(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to calculate fugacity: {e}") from e
