# import libs
from typing import (
    List,
    Dict,
    Callable,
    Optional
)
from fastmcp.tools import Tool
from fastmcp import FastMCP
# local
from .mcp import MCP


class MoziServer(MCP):
    """
    MoziServer class for managing the core functionalities of the MoziChem Hub.
    """

    def __init__(self, name: str = "MoziChemHub"):
        """
        Initialize the MoziServer instance.
        """
        # SECTION: initialize MCP
        MCP.__init__(self, name=name)

    @property
    def name(self) -> str:
        """
        Get the name of the server.
        """
        return self._name

    def _update_mcp_with_tools(
        self,
        tools: List[Tool]
    ) -> FastMCP:
        """
        Update the MCP server with tools.

        Returns
        -------
        FastMCP
            The MCP server instance.
        """
        try:
            # SECTION: add tools to the MCP server
            self._add_tools(tools)
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
