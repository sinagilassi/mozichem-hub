# import libs
from typing import (
    Any,
    List,
    Set,
    Callable,
    Literal,
    Dict,
    Union,
    Optional
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator
)
# local


class ComponentProperty(BaseModel):
    """
    Model for component property. This model is used by PyThermoLinkDB.

    Example
    -------
    Example of a component property configuration:
    {
        "databook": "databook 1",
        "table": "table 1",
        "symbol": "Cp_IG"
    }
    """
    databook: str = Field(
        ...,
        description="Databook name where the property is defined"
    )
    table: str = Field(
        ...,
        description="Table name where the property is defined"
    )
    symbol: Optional[str] = Field(
        None,
        description="Symbol for the property, e.g., 'Cp_IG'"
    )


class ComponentReferenceConfig(BaseModel):
    """
    Model for component reference. This model is used by PyThermoLinkDB.
    """
    properties: Optional[
        Dict[
            str, ComponentProperty
        ] | List[
            Dict[str, ComponentProperty]
        ]
    ] = Field(
        default_factory=list,
        description=(
            "Set of properties to be included in the reference."
        )
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "properties": {
                        "heat-capacity": {
                            "databook": "databook 1",
                            "table": "table 1",
                        },
                        "vapor-pressure": {
                            "databook": "databook 2",
                            "table": "table 2",
                        },
                        "general": {
                            "databook": "databook 3",
                            "table": "table 3"
                        }
                    }
                }
            ]
        }
    )


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
    config: Dict[str, Any] = Field(
        ...,
        description=(
            "Configuration for the thermodynamic database, "
            "which properties should be included"
        )
    )


class References(BaseModel):
    """
    Model for references thermodynamic database (ThermoDB).
    """
    contents: Optional[List[str] | str] = Field(
        [],
        description=(
            "List of references for the thermodynamic database provided by "
            "PyThermoDB"
        )
    )
    config: Optional[Dict[str, Any]] = Field(
        {},
        description=(
            "Configuration for the thermodynamic database, "
            "which properties should be included"
        )
    )

    @field_validator("contents", mode="before")
    @classmethod
    def convert_str_to_list(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return v


class ReferenceLink(BaseModel):
    """
    Model for references to functions (tools). This model is used by PyThermoLinkDB.

    Attributes
    ----------
    rule: str
        Reference rule to link between the reference and functions (tools).

    """
    rule: Optional[str] = Field(
        None,
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
