# import libs
from pyThermoDB import CompBuilder
from typing import Any, List, Literal
from pydantic import BaseModel, Field
# local


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


class CustomReference(BaseModel):
    content: str = Field(
        ...,
        description="Reference for the thermodynamic database, e.g., 'CUSTOM-REF-1'"
    )
    config: dict = Field(
        ...,
        description="Configuration for the thermodynamic database, which properties should be included"
    )
    rule: str = Field(
        ...,
        description="Reference rule to connect properties of the custom reference using "
    )


# NOTE: available mozichem references
MOZICHEM_REFERENCES = {
    'temperature': Temperature,
    'pressure': Pressure,
    'component': Component
}
