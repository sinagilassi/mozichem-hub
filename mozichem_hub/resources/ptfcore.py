# import libs
from typing import Dict, Any, Callable, List
import inspect
from typing import Annotated, Literal
from pydantic import Field
import pyThermoFlash as ptf
# local
from .models import (
    Temperature,
    Pressure,
    Component,
)
from .utils import (
    set_feed_specification,
    get_components_formulas,
    get_components_names,
)
from .hub import Hub


class PTFCore:
    """
    Core class for managing pyThermoFlash (PTF) functionalities.
    This class serves as a central point for PTF-related operations.
    """
    # NOTE: attributes
    id = "PTFCore"

    def __init__(self, hub: Hub):
        """
        Initialize the PTFCore instance.
        """
        # NOTE: store the hub instance
        self.hub = hub

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

    def calc_bubble_pressure(
        self,
        components: Annotated[
            List[Component],
            Field(..., description="List of components with their properties")
        ],
        temperature: Annotated[
            Temperature,
            Field(..., description="Temperature of the system")
        ],
        equilibrium_model: Annotated[
            Literal['raoult', 'modified-raoult'],
            Field(
                default='raoult',
                description="Equilibrium model to use for bubble pressure calculation"
            )
        ] = 'raoult'
    ) -> str:
        """Calculates the bubble pressure of a mixture of components at a given temperature."""
        try:
            # SECTION: components id
            # NOTE: formulas
            component_formulas = get_components_formulas(components)
            # NOTE: names
            component_names = get_components_names(components)

            # SECTION: build model source
            model_source = self.hub.build_components_model_source(
                components=components
            )

            # SECTION: initialize ptf
            vle = ptf.vle(component_formulas, model_source=model_source)

            # SECTION: set feed specification
            N0s = set_feed_specification(
                components=components,
                feed_mode="formula"  # or 'name'
            )

            # SECTION: model input
            model_inputs = {
                "mole_fraction": N0s,
                "temperature": [temperature.value, temperature.unit]
            }

            # SECTION: calc
            res = vle.bubble_pressure(
                inputs=model_inputs,
                equilibrium_model=equilibrium_model
            )

            # return
            return str(res)
        except Exception as e:
            raise RuntimeError(
                f"Error calculating bubble pressure: {e}"
            ) from e
