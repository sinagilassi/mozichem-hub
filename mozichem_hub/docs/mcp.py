# import libs
from typing import (
    List,
    Literal,
    Dict,
    Any,
    Optional
)
from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.exceptions import ToolError
# local
from ..config import app_settings


class MCP():
    """
    MCP class for serving the MCP Hub MCP.
    """
    # NOTE: attributes
    server_parameters: Dict[str, Any] = {
        "transport": "stdio",  # Must be one of: 'stdio', 'streamable-http'
        "host": "127.0.0.1",
        "port": 8000,
        "path": "/mcp",
        "log_level": "DEBUG"
    }

    def __init__(
        self,
        name: str,
        instructions: Optional[str] = None
    ):
        """
        Initialize the MCP instance.
        """
        # NOTE: set attributes
        self._name = name
        self._instructions = instructions

        # NOTE: Load settings
        self._settings = app_settings

        # NOTE: Initialize the MCP instance
        self._mcp = self.create_mcp()

    @property
    def transport(self) -> Literal['stdio', 'streamable-http']:
        """
        Get the transport type of the MCP server.
        """
        return self.server_parameters["transport"]

    @transport.setter
    def transport(self, value: Literal['stdio', 'streamable-http']):
        """
        Set the transport type of the MCP server.
        """
        if value not in ['stdio', 'streamable-http']:
            raise ValueError(
                "Transport must be one of: 'stdio', 'streamable-http'")
        self.server_parameters["transport"] = value

    @property
    def host(self) -> str:
        """
        Get the host address of the MCP server.
        """
        return self.server_parameters["host"]

    @host.setter
    def host(self, value: str):
        """
        Set the host address of the MCP server.
        """
        if not isinstance(value, str):
            raise ValueError("Host must be a string.")
        self.server_parameters["host"] = value

    @property
    def port(self) -> int:
        """
        Get the port number of the MCP server.
        """
        return self.server_parameters["port"]

    @port.setter
    def port(self, value: int):
        """
        Set the port number of the MCP server.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Port must be a positive integer.")
        self.server_parameters["port"] = value

    @property
    def path(self) -> str:
        """
        Get the path for the MCP server.
        """
        return self.server_parameters["path"]

    @path.setter
    def path(self, value: str):
        """
        Set the path for the MCP server.
        """
        if not isinstance(value, str):
            raise ValueError("Path must be a string.")
        self.server_parameters["path"] = value

    def create_mcp(self):
        """
        Create the MCP instance.

        Returns
        -------
        FastMCP
            The MCP instance with registered tools.
        """
        try:
            # NOTE: Initialize the MCP instance
            return FastMCP(
                name=self._name,
                instructions=self._instructions
            )
        except ToolError as e:
            raise RuntimeError(f"Failed to register tools: {e}") from e

    def get_mcp(self) -> FastMCP:
        """
        Get the MCP instance.

        Returns
        -------
        FastMCP
            The MCP instance.
        """
        try:
            # NOTE: Ensure the MCP instance is initialized
            if not isinstance(self._mcp, FastMCP):
                raise TypeError("MCP instance is not of type FastMCP.")

            # NOTE: Check if MCP instance is initialized
            if self._mcp is None:
                raise ValueError("MCP instance is not initialized.")

            # NOTE: add tools to the MCP server
            return self._mcp
        except Exception as e:
            raise RuntimeError(f"Failed to get MCP instance: {e}") from e

    def run(self):
        """
        Run the MCP server.
        """
        try:
            # NOTE: extract server parameters
            transport_str = self.server_parameters["transport"]
            host = self.server_parameters["host"]
            port = self.server_parameters["port"]
            path = self.server_parameters["path"]
            log_level = self.server_parameters["log_level"]

            # check if transport is valid
            valid_transports = ['stdio', 'streamable-http']
            if transport_str not in valid_transports:
                raise ValueError(
                    f"Invalid transport: {transport_str}. Must be one of: {valid_transports}"
                )

            # Cast str to Literal type after validation
            transport: Literal[
                'stdio', 'streamable-http',
            ] = transport_str  # type: ignore

            # NOTE: Start the MCP server
            self._mcp.run(
                transport=transport,
                host=host,
                port=port,
                path=path,
                log_level=log_level
            )
        except Exception as e:
            raise RuntimeError(f"Failed to run MCP server: {e}") from e

    def _add_tools(self, tools: List[Tool]):
        """
        Add the tools for the MCP.

        Parameters
        ----------
        tools : List[Tool]
            A list of tools to be added to the MCP server.

        Returns
        -------
        List[Tool]
            A list of tools to be registered with the MCP server.
        """
        try:
            # NOTE: check tools
            if len(tools) == 0:
                return

            # NOTE: add tools to the MCP server
            for tool in tools:
                if not isinstance(tool, Tool):
                    raise TypeError(
                        f"Expected Tool instance, got {type(tool)}")

                # Register each tool with the MCP server
                self._mcp.add_tool(tool)
        except Exception as e:
            raise Exception(f"Failed to build tools: {e}") from e
