# import libs
from typing import Any, List
from pydantic import BaseModel, Field
# local


class MoziToolArg(BaseModel):
    """
    MoziToolArgs class for defining arguments for tools in the MoziChem Hub.
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
    reference: str
    description: str
    args: List[MoziToolArg]
    tags: List[str] = []
