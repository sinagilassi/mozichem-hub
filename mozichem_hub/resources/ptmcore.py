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

    def calc_gas_component_fugacity(
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
        solver_method: Annotated[
            Literal['ls', 'fsolve', 'root'],
            Field(
                description="Solver method for fugacity calculation, e.g., 'least-square method', 'fsolve', 'root'",
                default="fsolve"
            )
        ] = "ls"
    ) -> dict:
        """Calculates the fugacity of a gas-phase component at given temperature and pressure"""
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
                model_source=model_source,
                solver_method=solver_method
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to calculate fugacity: {e}") from e

    def calc_liquid_component_fugacity(
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
        solver_method: Annotated[
            Literal['ls', 'fsolve', 'root'],
            Field(
                description="Solver method for fugacity calculation, e.g., 'least-square method', 'fsolve', 'root'",
                default="fsolve"
            )
        ] = "ls",
        liquid_fugacity_mode: Annotated[
            Literal['EOS', 'Poynting'],
            Field(
                description="Mode for liquid fugacity calculation, 'EOS' or 'Poynting'",
                default="EOS"
            )
        ] = "EOS"
    ) -> dict:
        """Calculates the fugacity of a liquid-phase component at given temperature and pressure"""
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

            # NOTE: set phase
            phase = "LIQUID"

            # SECTION: model input
            model_inputs = {
                "phase": phase,
                "component": component_,
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }

            # SECTION: calc
            res = self.eos.cal_fugacity(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source,
                liquid_fugacity_mode=liquid_fugacity_mode,
                solver_method=solver_method
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to calculate fugacity: {e}") from e

    def calc_fugacity_gas_mixture(
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
        """Calculates the fugacity of a gaseous mixture of components at given temperature and pressure."""
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

    def component_eos_roots_analysis(
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
        ]
    ) -> dict:
        """Analyzes the roots of the EOS for a given component at specified temperature and pressure."""
        try:
            # NOTE: extract component name
            (
                component_name, _, _
            ) = component.name, component.formula, component.state

            # SECTION: build model source
            model_source = self.hub.build_component_model_source(
                component=component
            )

            # SECTION: model input
            model_inputs = {
                "component": f"{component_name}-{component.state}",
                "pressure": [pressure.value, pressure.unit],
                "temperature": [temperature.value, temperature.unit]
            }

            # SECTION: calc
            res = self.eos.check_eos_roots_single_component(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to analyze EOS roots: {e}") from e

    def multi_component_eos_roots_analysis(
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
        ]
    ) -> dict:
        """Analyzes the roots of the EOS for a mixture of components at specified temperature and pressure."""
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
            res = self.eos.check_eos_roots_multi_component(
                model_name=eos_model,
                model_input=model_inputs,
                model_source=model_source
            )

            # return
            return res
        except Exception as e:
            raise ValueError(f"Failed to analyze EOS roots: {e}") from e
