# import libs
import logging
from typing import Any, List, Set, Callable, Literal, Optional, Dict
# locals
from .models import (
    Component,
    Temperature,
    Pressure,
)


def set_feed_specification(
    components: List[Component],
    feed_mode: Literal['name', 'formula'] = 'name'
) -> Dict[str, float]:
    """
    Set feed specification for a list of components.
    """
    try:
        # NOTE: Initialize feed specification dictionary
        feed_spec = {}

        # NOTE: Iterate over components to set feed specification
        for i, component in enumerate(components):
            # set
            name_ = component.name
            formula_ = component.formula
            state_ = component.state

            # Check if mole_fraction is provided, otherwise skip
            if component.mole_fraction is None:
                logging.warning(
                    f"Component {name_} does not have a mole fraction defined. Skipping.")
                continue

            # NOTE: Set feed specification
            if feed_mode == 'name':
                feed_spec[f"{name_}-{state_}"] = component.mole_fraction
            elif feed_mode == 'formula':
                feed_spec[f"{formula_}-{state_}"] = component.mole_fraction
            else:
                # raise ValueError("Invalid feed_mode. Use 'name' or 'formula'.")
                logging.error(
                    f"Invalid feed_mode: {feed_mode}. Use 'name' or 'formula'.")

        return feed_spec
    except Exception as e:
        logging.error(f"Failed to set feed specification: {e}")
        raise ValueError(f"Failed to set feed specification: {e}") from e
