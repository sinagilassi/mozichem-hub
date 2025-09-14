# import libs
import logging
from typing import (
    List,
    Literal,
    Dict
)
# locals
from pythermodb_settings.models import (
    Component,
)


def set_feed_specification(
    components: List[Component],
    feed_mode: Literal['name', 'formula'] = 'name'
) -> Dict[str, float]:
    """
    Set feed specification for a list of components with their mole fractions.
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


def get_components_formulas(
    components: List[Component]
) -> List[str]:
    """
    Get formulas of components as formula-state.
    """
    try:
        # NOTE: Extract formulas from components
        return [
            f"{component.formula}-{component.state}"
            for component in components
        ]
    except Exception as e:
        logging.error(f"Failed to get component formulas: {e}")
        raise ValueError(f"Failed to get component formulas: {e}") from e


def get_components_names(
    components: List[Component]
) -> List[str]:
    """
    Get names of components as name-state.
    """
    try:
        # NOTE: Extract names from components
        return [
            f"{component.name}-{component.state}"
            for component in components
        ]
    except Exception as e:
        logging.error(f"Failed to get component names: {e}")
        raise ValueError(f"Failed to get component names: {e}") from e


def check_input(
    value: str | int | float
) -> int | float | str:
    """
    If value is a string that represents an int or float, convert and return the appropriate type.
    Otherwise, return value as is.
    """
    try:
        if isinstance(value, int) or isinstance(value, float):
            return value
        if isinstance(value, str):
            value_stripped = value.strip()
            # Try integer first
            try:
                return int(value_stripped)
            except ValueError:
                pass
            # Try float
            try:
                return float(value_stripped)
            except ValueError:
                pass
            # Return original string if not numeric
            return value
        return value
    except Exception as e:
        logging.error(f"Failed to detect digit/float from string: {e}")
        raise ValueError(
            f"Failed to detect digit/float from string: {e}") from e


def convert_str_numeric_to_int(
    value: str | int
) -> int | str:
    """
    Convert a string that represents an integer or float to the appropriate type.
    If the string is not numeric, return it as is.
    """
    try:
        # NOTE: check if value is integer
        if isinstance(value, int):
            return value

        # NOTE: check if value is string
        if isinstance(value, str):
            value_stripped = value.strip()
            # Try integer first
            try:
                # check it has only digits
                if value_stripped.isdigit():
                    return int(value_stripped)
                else:
                    # return original string if not numeric
                    return value
            except ValueError:
                pass
        return value  # Return original value if not a string or not numeric
    except Exception as e:
        logging.error(f"Failed to convert string to numeric: {e}")
        raise ValueError(f"Failed to convert string to numeric: {e}") from e
