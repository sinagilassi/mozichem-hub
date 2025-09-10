# import libs
from pydantic import BaseModel, Field


class ComponentIdentity(BaseModel):
    """
    Model for component identity.
    """
    name_state: str = Field(
        ...,
        description="Component name-state identifier"
    )
    formula_state: str = Field(
        ...,
        description="Component formula-state identifier"
    )
