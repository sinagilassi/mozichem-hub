# import libs
from typing import Any, List, Set, Callable, Literal
from pydantic import BaseModel, Field, ConfigDict
from pyThermoDB import CompBuilder
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
    args: List[MoziToolArg]
    tags: Set[str] = set()


class Temperature(BaseModel):
    """Temperature model for input validation"""
    value: float = Field(..., description="Temperature value")
    unit: str = Field(..., description="Temperature unit, e.g., 'K', 'C', 'F'")


class Pressure(BaseModel):
    """Pressure model for input validation"""
    value: float = Field(..., description="Pressure value")
    unit: str = Field(
        ...,
        description="Pressure unit, e.g., 'bar', 'atm', 'Pa'"
    )


class Component(BaseModel):
    """Component model for input validation"""
    name: str = Field(..., description="Name of the component")
    formula: str = Field(..., description="Chemical formula of the component")
    state: Literal['g', 'l', 's'] = Field(
        ...,
        description="State of the component: 'g' for gas, 'l' for liquid, 's' for solid"
    )


class ComponentThermoDB(BaseModel):
    """
    Model for component thermodynamic database (ThermoDB).

    Attributes
    ----------
    component: Component
        The component for which the thermodynamic database is built.
    property_source: dict
        Source of properties for the component.
    build_mode: Literal['name', 'formula']
        Mode to build the thermodynamic database, either by name or formula.
    """
    component: Component
    thermodb: CompBuilder
    build_mode: Literal['name', 'formula'] = 'name'

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
