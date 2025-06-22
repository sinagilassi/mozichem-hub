# import libs
from typing import List, Dict, Callable, Optional
from fastmcp.tools import Tool
from fastmcp import FastMCP
# local
from .mcp import MoziMCP
from ..tools import ToolManager


class MoziServer(MoziMCP):
    """
    MoziServer class for managing the core functionalities of the MoziChem Hub.
    """

    def __init__(self, name: str = "MoziChemHub"):
        """
        Initialize the MoziServer instance.
        """
        # SECTION: initialize MoziMCP
        MoziMCP.__init__(self, name=name)

        # SECTION: initialize the ToolManager
        self.ToolManager_ = ToolManager()

    @property
    def name(self) -> str:
        """
        Get the name of the server.
        """
        return self._name

    def _build_mcp(
        self,
        tools: Optional[Dict[str, Callable]] = None
    ) -> FastMCP:
        """
        Build the MCP server using FastMCP.

        Returns
        -------
        FastMCP
            The MCP server instance.
        """
        try:
            # SECTION: convert tools to MCP tools
            tools_: List[Tool] = self.ToolManager_._build_tools()

            # SECTION: add tools to the MCP server
            self._add_tools(tools_)

            # SECTION: Return the MCP instance
            return self.get_mcp()
        except Exception as e:
            raise Exception(f"Failed to build mcp server: {e}") from e

    def _serve(self):
        """
        Serve the MoziChem Hub server.
        """
        try:
            # log
            print(f"Starting {self._name} server...")

            # NOTE: Start the MCP server
            # mcp
            self.run()

            # log
            print(f"{self._name} server is running.")
        except Exception as e:
            raise Exception(f"Failed to start {self._name} server: {e}") from e
