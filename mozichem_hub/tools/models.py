# import libs
from typing import Dict, Any
from pydantic import BaseModel
# local


class MoziToolArgs(BaseModel):
    """
    MoziToolArgs class for defining arguments for tools in the MoziChem Hub.
    """
    type: str
    description: str
    default: Any = None
    required: bool = False


class MoziTool(BaseModel):
    """
    MoziTool class for defining tools in the MoziChem Hub.
    """
    name: str
    reference: str
    description: str
    args: Dict[str, MoziToolArgs]
