# import libs
from fastmcp import FastMCP
from typing import Optional, Dict, List, Callable, Any
# local
from .docs import MCPHub
from .references import Reference, ReferenceLink
from .utils import MCPController


def get_mozichem_mcp() -> List[str]:
    """
    Get the names of all available MCPs.

    Returns
    -------
    list
        List of MCP names.
    """
    return MCPController.mcp_names()


def get_mozichem_mcp_info(mcp_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a specific MCP.

    Parameters
    ----------
    mcp_name : str
        Name of the MCP to retrieve information for.

    Returns
    -------
    dict or None
        Information about the MCP, or None if not found.
    """
    return MCPController.get_mcp_info(mcp_name)


def create_mozichem_mcp(
    name: str,
    reference: Optional[Reference] = None,
    reference_link: Optional[ReferenceLink] = None,
    **kwargs
):
    """
    Build the mcp server using FastMCP.

    Parameters
    ----------
    name : str
        Name of the mcp server, default is "MoziChemHub"
    reference : Reference
        Custom reference for the mcp calculation based on PyThermoDB.
        It includes:
        - content: str
        - config: dict
    reference_link : ReferenceLink
        Custom reference link for the mcp calculation based on PyThermoLinkDB.
    **kwargs : dict
        Additional keyword arguments for mcp configuration.

    Returns
    -------
    FastMCP
        The MCP server instance.
    """
    try:
        # NOTE: collect mcp parameters
        name = name.strip().lower()

        # SECTION: check if the mcp name is valid
        MCPController_ = MCPController()

        # Check if the provided name is a valid MCP name
        if not MCPController_.check_mcp_name(name):
            raise ValueError(
                f"'{name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController_.mcp_names())}"
            )

        # SECTION: Initialize the MoziChemHub instance
        MCPHub_ = MCPHub(
            mcp=name,
            reference=reference,
            reference_link=reference_link,
            **kwargs
        )

        # SECTION: retrieve the mcp server
        mcp = MCPHub_._retrieve_mcp()

        # return the mcp server instance of FastMCP
        return mcp
    except Exception as e:
        raise Exception(f"Failed to build mcp server: {e}") from e
