# import libs
from typing import (
    Any, List, Set, Callable, Literal, Dict, Union
)
from pydantic import BaseModel, Field
# local


class Reference(BaseModel):
    """
    Model for reference thermodynamic database (ThermoDB).
    """
    content: str = Field(
        ...,
        description=(
            "Reference for the thermodynamic database provided by PyThermoDB"
        )
    )
    config: dict = Field(
        ...,
        description=(
            "Configuration for the thermodynamic database, "
            "which properties should be included"
        )
    )


class ReferenceLink(BaseModel):
    """
    Model for references to functions (tools). This model is used by PyThermoLinkDB.

    Attributes
    ----------
    rule: str
        Reference rule to link between the reference and functions (tools).

    """
    rule: str = Field(
        ...,
        description=(
            "Reference rule to link between the custom reference "
            "and application"
        )
    )


class ReferenceThermoDB(BaseModel):
    """
    Model for component thermodynamic database (ThermoDB).
    """
    reference: Dict[str, List[str]]
