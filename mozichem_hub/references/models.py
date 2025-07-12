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
    field_validator,
    model_validator
)
# local


class ComponentPropertySource(BaseModel):
    """
    Model for component property source. This model is used by PyThermoLinkDB.

    Example
    -------
    Example of a component property configuration:
    {
        "databook": "databook 1",
        "table": "table 1",
        "label": "Cp_IG",
        "labels": None
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
    mode: Literal["DATA", "EQUATIONS"] = Field(
        ...,
        description=(
            "Mode of the property, either 'DATA' for data properties or "
            "'EQUATIONS' for equation properties"
        )
    )
    label: Optional[str] = None
    labels: Optional[Dict[str, str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "databook": "databook 1",
                    "table": "table 1",
                    "mode": "EQUATIONS",
                    "label": "Cp_IG"
                },
                {
                    "databook": "databook 2",
                    "table": "table 2",
                    "mode": "DATA",
                    "labels": {
                        "Pc": "Pc",
                        "Tc": "Tc",
                        "AcFa": "AcFa"
                    }
                }
            ]
        }
    )

    @model_validator(mode="after")
    def check_exclusive_label_fields(self):
        if self.label is not None and self.labels is not None:
            raise ValueError(
                "Only one of 'label' or 'labels' should be provided.")
        if self.label is None and self.labels is None:
            raise ValueError("Either 'label' or 'labels' must be provided.")
        return self


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
    config: Optional[Dict[str, Any] | str] = Field(
        None,
        description=(
            "Configuration for the thermodynamic database, "
            "which properties should be included"
        )
    )


class References(BaseModel):
    """
    Model for references thermodynamic database (ThermoDB).

    Notes
    -----
    - Case 1: user provides a single reference as a string, the app config is set to the default configuration.
    - Case 2: user provides a list of references as a list of strings, the app config is set to the default configuration.
    - case 3: user only provides a configuration without any references, the app references the default configuration.
    """
    contents: Optional[List[str]] = None
    config: Optional[Dict[str, Dict[str, ComponentPropertySource]]] = None
    link: Optional[str] = None

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
    def convert_str_to_dict(cls, v):
        if v is None:
            return {}
        if isinstance(v, dict):
            return v


class ReferenceThermoDB(BaseModel):
    """
    Model for component thermodynamic database (ThermoDB).
    """
    reference: Dict[str, List[str]]
    contents: List[str]
    config: Dict[str, Dict[str, Dict[str, str]]]
    link: Dict[str, Dict[str, Dict[str, str]]]
