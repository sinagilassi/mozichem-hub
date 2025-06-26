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
        "label": "Cp_IG"
    }

    Notes
    -----
    - `databook`: Name of the databook where the property is defined.
    - `table`: Name of the table where the property is defined.
    - `label`: Optional label for the property used in the script, e.g., 'Cp_IG'.
    - `labels`: Optional dictionary of labels for the property used in the script,
    """
    databook: str = Field(
        ...,
        description="Databook name where the property is defined"
    )
    table: str = Field(
        ...,
        description="Table name where the property is defined"
    )
    label: Optional[str] = Field(
        None,
        description="label for the property used in the script, e.g., 'Cp_IG'"
    )
    labels: Optional[Dict[str, str]] = Field(
        None,
        description=(
            "Dictionary of labels for the property used in the script, "
            "e.g., {'Pc': 'Pc', 'Tc': 'Tc', 'AcFa': 'AcFa'}"
        )
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "databook": "databook 1",
                    "table": "table 1",
                    "label": "Cp_IG"
                },
                {
                    "databook": "databook 2",
                    "table": "table 2",
                    "labels": {
                        "Pc": "Pc",
                        "Tc": "Tc",
                        "AcFa": "AcFa"
                    }
                }
            ]
        }
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
                            "": "Cp_IG"
                        },
                        "vapor-pressure": {
                            "databook": "databook 2",
                            "table": "table 2",
                            "symbol": "VaPr"
                        },
                        "general": {
                            "databook": "databook 3",
                            "table": "table 3",
                            "symbols": {
                                "Pc": "Pc",
                                "Tc": "Tc",
                                "AcFa": "AcFa"
                            }
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
    config: Optional[
        Union[
            Dict[str, Dict[str, str]],
            List[Dict[str, Dict[str, str]]]
        ]] = Field(
        [],
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

    @field_validator("config", mode="before")
    @classmethod
    def convert_dict_to_list(cls, v):
        if v is None:
            return []
        if isinstance(v, dict):
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
