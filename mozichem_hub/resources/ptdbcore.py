# import libs
from typing import Dict, Any, Callable, List
import inspect
from typing import Annotated, Literal
from pydantic import Field
import pyThermoDB as ptdb
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


class PTDBCore:
    """
    Core class for managing PyThermoDB (PTDB) functionalities.
    This class serves as a central point for PTDB-related operations.
    """
    # NOTE: attributes
    id = "PTDBCore"

    def __init__(self, hub: Hub):
        """
        Initialize the PTDBCore instance.
        """
        # NOTE: store the hub instance
        self.hub = hub

        # NOTE: initialize the PTDB database
        self.tdb = ptdb.init()

    def list_functions(self) -> Dict[str, Callable[..., Any]]:
        return {
            name: getattr(self, name)
            for name, obj in inspect.getmembers(
                self.__class__, predicate=inspect.isfunction
            )
            if not name.startswith('__') and name != 'list_functions'
        }

    def verify_component_thermodynamic_properties_availability(
        self,
        component: Annotated[
            Component,
            Field(..., description="Component name and properties")
        ],
    ) -> str:
        """Verify the availability of thermodynamic properties for a given component in the database."""
        try:
            # NOTE: extract component name
            (
                component_name, component_formula, _
            ) = component.name, component.formula, component.state

            # SECTION: search term
            search_terms = [component_name, component_formula]

            # SECTION: check
            res = self.tdb.search_databook(
                search_terms,
                res_format='json',
                search_mode='exact'
            )

            # return
            return str(res)
        except Exception as e:
            raise RuntimeError(
                f"Failed to verify component thermodynamic properties: {e}") from e
