# import libs
from fastmcp import FastMCP
# local
from .mcp import MoziMCP


class MoziChemHub:
    """
    MoziChemHub class for managing the core functionalities of the MoziChem Hub.
    """

    def __init__(self, name: str = "MoziChemHub"):
        """
        Initialize the MoziChemHub instance.
        """
        # set
        self._name = name

        # NOTE: Initialize the MCP instance
        self.MoziMCP_ = MoziMCP(name=name)

    @property
    def mcp(self) -> FastMCP:
        """
        Get the MCP instance.
        """
        return self.MoziMCP_.mcp

    @property
    def name(self) -> str:
        """
        Get the name of the server.
        """
        return self._name

    def serve(self):
        """
        Serve the MoziChem Hub server.
        """
        try:
            # log
            print(f"Starting {self._name} server...")

            # NOTE: Start the MCP server
            # mcp
            self.mcp.run()

            # log
            print(f"{self._name} server is running.")
        except Exception as e:
            raise Exception(f"Failed to start {self._name} server: {e}") from e
