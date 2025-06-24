# import libs
from typing import List, Dict, Callable
from fastmcp.tools import Tool
# local
from ..config import app_settings
from ..manager import MoziTool


class ToolBuilder():
    """
    Builder class for managing the core functionalities of the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the MoziTools instance.
        """
        # set
        self._settings = app_settings

    def build_mozi_tools(
        self,
        mozi_tools: List[MoziTool]
    ) -> List[Tool]:
        """
        Build the MCP tools from local resources.

        Parameters
        ----------
        functions : Dict[str, Callable]
            Dictionary of functions to be included in the tools.

        Returns
        -------
        List[Tool]
            List of Tool instances built from the provided functions.
        """
        try:
            # SECTION: Convert MoziTool instances to Tool instances
            mcp_tools: list[Tool] = []

            for mozi_tool in mozi_tools:
                tool_ = Tool.from_function(
                    fn=mozi_tool.fn,  # Pass the function as fn parameter
                    name=mozi_tool.name,
                    description=mozi_tool.description,
                    tags=mozi_tool.tags,
                )
                mcp_tools.append(tool_)

            return mcp_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e

    def build_tools_from_function(
        self,
        functions: Dict[str, Callable]
    ) -> List[Tool]:
        """
        Build the MCP tools from external resources.

        Parameters
        ----------
        functions : Dict[str, Callable]
            Dictionary of functions to be included in the tools.

        Returns
        -------
        List[Tool]
            List of Tool instances built from the provided functions.
        """
        try:
            # SECTION: Convert MoziTool instances to Tool instances
            mcp_tools: list[Tool] = []

            for fn_name, fn in functions.items():
                tool_ = Tool.from_function(
                    fn=fn,  # Pass the function as fn parameter
                    name=fn_name,
                )

                # add tool
                mcp_tools.append(tool_)

            return mcp_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e
