# import libs
from typing import Optional
# local
from .core import MoziChemMCP
from ..references import (
    Reference,
    ReferenceLink
)
from ..config import MCP_MODULES


class MCPHub(MoziChemMCP):
    """
    MCPHub class for creating mcp from built-in functions.
    """

    def __init__(
        self,
        mcp: str,
        reference: Optional[Reference] = None,
        reference_link: Optional[ReferenceLink] = None,
        **kwargs
    ):
        """
        Initialize the MCPHub.
        """
        # SECTION: select the name of the mcp available
        mcp = mcp.strip().lower()
        # set the name of the mcp
        self._name = mcp

        # NOTE: check if mcp is available
        # mcp names
        mcp_names = [
            module["name"] for module in MCP_MODULES
        ]

        # check if mcp is available
        if mcp not in mcp_names:
            raise ValueError(
                f"'{mcp}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(mcp_names)}"
            )

        # SECTION: initialize the MoziChemHub
        MoziChemMCP.__init__(
            self,
            name=mcp,
            reference=reference,
            reference_link=reference_link,
            **kwargs
        )

    @property
    def name(self) -> str:
        """
        Get the name of the adapter.
        """
        return self._name
