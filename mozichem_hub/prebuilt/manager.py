# import libs
import logging
from typing import (
    Optional,
    Dict,
    List,
    Union,
    Any
)
from pyThermoDB.models import ComponentConfig
# locals
from ..docs import MCPHub, MoziChemMCP
from ..utils import MCPController


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
    reference_content: Optional[
        Union[str, List[str]]
    ] = None,
    reference_config: Optional[
        Union[
            str,
            Dict[str, Dict[str, ComponentConfig]]
        ]
    ] = None,
    **kwargs
) -> MoziChemMCP:
    """
    Build the mcp server using FastMCP.

    Parameters
    ----------
    name : str
        Name of the mcp server, default is "MoziChemHub"
    reference_content : Optional[Union[str, List[str]]]
        Reference content for the mcp server, default is None.
    reference_config : Optional[Union[str, Dict[str, Dict[str, ComponentConfig]]
        Reference configuration for the mcp server, default is None.
    **kwargs : dict
        Additional keyword arguments for mcp configuration.

    Returns
    -------
    MoziChemMCP
        The MCP server instance.
    """
    try:
        # NOTE: collect mcp parameters
        name = name.strip().lower()

        # SECTION: check if the mcp name is valid
        MCPController_ = MCPController()

        # Check if the provided name is a valid MCP name
        if not MCPController_.check_mcp_name(name):
            logging.error(
                f"'{name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController_.mcp_names())}"
            )
            raise ValueError(
                f"'{name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController_.mcp_names())}"
            )

        # SECTION: Initialize the MoziChemHub instance
        MCPHub_ = MCPHub(
            mcp=name,
            reference_content=reference_content,
            reference_config=reference_config,
            **kwargs
        )

        # SECTION: retrieve the mcp server
        mcp = MCPHub_._build_mozichem_mcp()

        # return the mcp server instance of MoziChemMCP
        return mcp
    except Exception as e:
        logging.error(f"Failed to build mcp server: {e}")
        raise Exception(f"Failed to build mcp server: {e}") from e
