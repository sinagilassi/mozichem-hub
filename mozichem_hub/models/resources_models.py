# # import libs
from typing import Any, List, Set, Callable, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from pyThermoDB import CompBuilder
from pythermodb_settings.models import Component
# local


class MoziToolArg(BaseModel):
    """
    MoziToolArg class for defining arguments for tools in the MoziChem Hub.
    """
    name: str
    description: str
    default: Any = None
    hide: bool = False
    required: bool = False
    type: str


class MoziTool(BaseModel):
    """
    MoziTool class for defining tools in the MoziChem Hub.
    """
    name: str
    fn: Callable[..., Any]  # Function to be executed
    description: str
    args: Optional[List[MoziToolArg]] = None
    tags: Set[str] = set()


# class Temperature(BaseModel):
#     """Temperature model for input validation"""
#     value: float = Field(..., description="Temperature value")
#     unit: str = Field(..., description="Temperature unit, e.g., 'K', 'C', 'F'")


# class Pressure(BaseModel):
#     """Pressure model for input validation"""
#     value: float = Field(..., description="Pressure value")
#     unit: str = Field(
#         ...,
#         description="Pressure unit, e.g., 'bar', 'atm', 'Pa'"
#     )


# class Component(BaseModel):
#     """Component model for input validation"""
#     name: str = Field(..., description="Name of the component")
#     formula: str = Field(..., description="Chemical formula of the component")
#     state: Literal['g', 'l', 's', 'aq'] = Field(
#         ...,
#         description="State of the component: 'g' for gas, 'l' for liquid, 's' for solid"
#     )
#     mole_fraction: float = Field(
#         default=1.0,
#         description="Mole fraction of the component in a mixture, if applicable"
#     )


class ComponentThermoDB(BaseModel):
    """
    Model for component thermodynamic database (ThermoDB).

    Attributes
    ----------
    component: Component
        The component for which the thermodynamic database is built.
    thermodb: CompBuilder
        The thermodynamic database object from pyThermoDB.
    component_key: Literal[
        'Name-State', 'Formula-State', 'Name', 'Formula', 'Name-Formula-State'
    ]
        Key to identify the component in the reference content.
    """
    component: Component
    thermodb: CompBuilder
    component_key: Literal[
        'Name-State', 'Formula-State'
    ] = Field(
        default='Name-State',
        description="Key to identify the component in the reference content."
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow"
    )
