# import libs
import logging
from typing import List
# locals
from .mcp_descriptor import MCPDescriptor
from ..config import MCP_MODULES

# NOTE: logger
logger = logging.getLogger(__name__)


def get_mcp_ignore_state_props(
    mcp_name: str,
    method_name: str
):
    """
    Get all properties for which state is ignored in a specific mcp method.

    Parameters
    ----------
    mcp_name : str
        The name of the mcp.
    method_name : str
        The name of the method.

    Returns
    -------
    List[str]
        A list containing the properties for which state is ignored.
    """
    try:
        # check if mcp name exists
        if not mcp_name:
            logger.error(f"MCP with name '{mcp_name}' not found.")
            return []

        # NOTE: load the mcp descriptor
        mcp_descriptor = MCPDescriptor().mcp_descriptor(mcp_name)

        # NOTE: check if method exists
        if method_name not in mcp_descriptor:
            logger.error(
                f"Method '{method_name}' not found in MCP '{mcp_name}'.")
            return []

        # NOTE:reference inputs
        ignore_state_props: List[str] = mcp_descriptor[method_name].get(
            'IGNORE_STATE_PROPS', []
        )

        return ignore_state_props
    except Exception as e:
        logger.error(f"Error loading ignore state props: {e}")
        return []
