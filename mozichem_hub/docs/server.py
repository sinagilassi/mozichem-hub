# import libs
from fastmcp import FastMCP
# local
from .mcp import MoziMCP


class MoziServer:
    """
    MoziServer class for managing the core functionalities of the MoziChem Hub.
    """

    def __init__(self, name: str = "MoziChemHub"):
        """
        Initialize the MoziServer instance.
        """
        # set
        self._name = name

        # Return the MCP instance
        # NOTE: Initialize the MCP instance
        self.MoziMCP_ = MoziMCP(name=self.name)

    @property
    def name(self) -> str:
        """
        Get the name of the server.
        """
        return self._name

    def _build_mcp(self) -> FastMCP:
        """
        Build the MCP server using FastMCP.

        Returns
        -------
        FastMCP
            The MCP server instance.
        """
        try:
            # Return the MCP instance
            return self.MoziMCP_.get_mcp()
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
            self.MoziMCP_.run()

            # log
            print(f"{self._name} server is running.")
        except Exception as e:
            raise Exception(f"Failed to start {self._name} server: {e}") from e
