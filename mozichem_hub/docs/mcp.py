# import libs
from typing import List
from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.exceptions import ToolError
# local
from ..config import app_settings


class MoziMCP():
    """
    MoziApp class for serving the MoziMCP Hub MCP.
    """
    # NOTE: attributes

    def __init__(self,
                 name: str,
                 transport: str = "stdio",
                 host: str = "127.0.0.1",
                 port: int = 8000,
                 log_level: str = "DEBUG"
                 ):
        """
        Initialize the MoziMCP instance.
        """
        # NOTE: set attributes
        self._name = name
        self._transport = transport
        self._host = host
        self._port = port
        self._log_level = log_level

        # NOTE: Load settings
        self._settings = app_settings

        # NOTE: Initialize the MCP instance
        self._mcp = FastMCP(
            name=name,
        )

    @property
    def mcp(self) -> FastMCP:
        """
        Get the MCP instance.
        """
        if self._mcp is None:
            raise ValueError("MCP instance is not initialized.")
        return self._mcp

    def add_tool(self, tools: List[Tool]) -> bool:
        """
        Add tools to the MCP server.

        Parameters
        ----------
        tools : List[Tool]
            A list of Tool instances to be added to the MCP server.

        """
        try:
            return True
        except Exception as e:
            raise ValueError(f"Failed to add tools: {e}") from e
