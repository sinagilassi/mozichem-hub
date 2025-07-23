# import libs

# Error messages
MCP_INITIALIZATION_ERROR_MSG = "Error initializing MCP."
MCP_EXECUTION_ERROR_MSG = "Error executing MCP."
MCP_UPDATE_ERROR_MSG = "Error updating MCP."
MCP_NOT_FOUND_ERROR_MSG = "MCP not found."
MCP_INVALID_CONFIG_ERROR_MSG = "Invalid MCP configuration."
MCP_REGISTRATION_ERROR_MSG = "Error registering MCP."


class MCPError(Exception):
    """Base exception for all MCP-related errors."""
    pass


class MCPInitializationError(MCPError):
    """Raised when there's an error initializing an MCP."""
    pass


class MCPExecutionError(MCPError):
    """Raised when there's an error executing an MCP."""
    pass


class MCPUpdateError(MCPError):
    """Raised when there's an error updating an MCP."""
    pass


class MCPNotFoundError(MCPError):
    """Raised when an MCP is not found."""
    pass


class MCPInvalidConfigError(MCPError):
    """Raised when an MCP configuration is invalid."""
    pass


class MCPRegistrationError(MCPError):
    """Raised when there's an error registering an MCP."""
    pass
