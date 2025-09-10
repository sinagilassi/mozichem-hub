# import libs
import logging
# local
from ..models import Component, ComponentIdentity

# NOTE: logger
logger = logging.getLogger(__name__)


def create_component_id(
    component: Component,
    separator_symbol: str = '-'
) -> ComponentIdentity:
    '''
    Create component name-state and formula-state identifiers.

    Parameters
    ----------
    component : Component
        The component for which to create the identifiers.
    separator_symbol : str, optional
        The symbol to use as a separator between the name/formula and

    Returns
    -------
    ComponentIdentity
        The component identity containing name-state and formula-state
        identifiers.
    '''
    try:
        # NOTE: extract component name
        component_name = component.name.strip()
        component_formula = component.formula.strip()
        component_state = component.state.strip().lower()

        # >> separator
        separator_symbol = separator_symbol.strip()

        # SECTION: create component identifiers
        name_state = f"{component_name}{separator_symbol}{component_state}"
        formula_state = f"{component_formula}{separator_symbol}{component_state}"

        return ComponentIdentity(
            name_state=name_state,
            formula_state=formula_state
        )
    except Exception as e:
        logger.error(
            f"Failed to create component identifiers for "
            f"'{component}': {e}"
        )
        raise e
