# import libs
from typing import (
    List,
    Optional
)
from fastmcp.tools import Tool
# local
from .mcp import MCP
from ..errors import (
    ToolRegistrationError,
    MCPExecutionError,
    TOOL_REGISTRATION_ERROR_MSG,
    MCP_EXECUTION_ERROR_MSG
)


class MoziServer(MCP):
    """
    MoziServer class for managing the core functionalities of the MoziChem MCP.
    """

    def __init__(
        self,
        name: str = "MoziChemMCP",
        instructions: Optional[str] = None
    ):
        """
        Initialize the MoziServer instance.

        Parameters
        ----------
        name : str
            Name of the MoziChem server, default is "MoziChemMCP".
        instructions : Optional[str]
            Instructions for the MoziChem server, default is None.
        """
        # SECTION: initialize MCP
        MCP.__init__(self, name=name, instructions=instructions)

    @property
    def name(self) -> str:
        """
        Get the name of the server.
        """
        return self._name

    def _update_mcp_with_tools(
        self,
        tools: List[Tool]
    ):
        """
        Update the MCP server with tools.

        Parameters
        ----------
        tools : List[Tool]
            List of tools to be added to the MCP server.

        Raises
        ------
        ToolRegistrationError
            If there is an error while adding tools to the MCP server.
        """
        try:
            # SECTION: add tools to the MCP server
            self._add_tools(tools)
        except Exception as e:
            raise ToolRegistrationError(
                f"{TOOL_REGISTRATION_ERROR_MSG} Failed to build mcp server: {e}") from e

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
            raise MCPExecutionError(
                f"{MCP_EXECUTION_ERROR_MSG} Failed to start {self._name} server: {e}") from e
