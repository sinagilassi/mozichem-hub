# import libs
from typing import List
from fastmcp.tools import Tool
# local
from ..config import app_settings


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

    def build_mcp_tools(self) -> List[Tool]:
        """
        Build the MCP tools.

        This method is responsible for building the tools that will be
        registered with the MCP server.
        """
        try:
            # SECTION: Build Mozi tools
            mozi_tools = []

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
