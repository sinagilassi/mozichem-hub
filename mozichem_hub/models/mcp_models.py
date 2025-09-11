# import libs
from pydantic import BaseModel, Field
# local


class MCPConfig(BaseModel):
    """
    Model for MCP configuration.

    Attributes
    ----------
    transport : str
        Transport protocol for the MCP server.
    host : str
        Host address for the MCP server.
    port : int
        Port for the MCP server.
    path : str
        Path for the MCP server.
    log_level : str
        Log level for the MCP server.
    """
    transport: str = Field(
        "stdio",
        description="Transport protocol for the MCP server"
    )
    host: str = Field(
        "127.0.0.1",
        description="Host address for the MCP server"
    )
    port: int = Field(
        8000,
        description="Port for the MCP server"
    )
    path: str = Field(
        "/mcp",
        description="Path for the MCP server"
    )
    log_level: str = Field(
        "DEBUG",
        description="Log level for the MCP server"
    )
