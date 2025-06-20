# import libs
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
    unit: str = Field(...,
                      description="Pressure unit, e.g., 'bar', 'atm', 'Pa'")


class Component(BaseModel):
    """Component model for input validation"""
    name: str = Field(..., description="Name of the component")
    formula: str = Field(..., description="Chemical formula of the component")
    state: Literal['g', 'l', 's'] = Field(
        ..., description="State of the component: 'g' for gas, 'l' for liquid, 's' for solid")
