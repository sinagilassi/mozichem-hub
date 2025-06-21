# import libs
from typing import Any, List, Set, Callable
from pydantic import BaseModel
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
    fn: Callable
    reference: str
    description: str
    args: List[MoziToolArg]
    tags: Set[str] = set()
