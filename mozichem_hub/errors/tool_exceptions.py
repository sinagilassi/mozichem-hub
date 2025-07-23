# import libs

# Error messages
TOOL_BUILDING_ERROR_MSG = "Error building tools."
TOOL_EXECUTION_ERROR_MSG = "Error executing tool."
MCP_TOOL_BUILDING_ERROR_MSG = "Error building MCP tools."
FUNCTION_RETRIEVAL_ERROR_MSG = "Error retrieving function."
FUNCTION_LOADING_ERROR_MSG = "Error loading functions."
TOOL_REGISTRATION_ERROR_MSG = "Error registering tool."
TOOL_NOT_FOUND_ERROR_MSG = "Tool not found."


class ToolError(Exception):
    """Base exception for all tool-related errors."""
    pass


class ToolBuildingError(ToolError):
    """Raised when there's an error building tools."""
    pass


class ToolExecutionError(ToolError):
    """Raised when there's an error executing a tool."""
    pass


class MCPToolBuildingError(ToolError):
    """Raised when there's an error building MCP tools."""
    pass


class FunctionRetrievalError(ToolError):
    """Raised when there's an error retrieving a function."""
    pass


class FunctionLoadingError(ToolError):
    """Raised when there's an error loading functions."""
    pass


class ToolRegistrationError(ToolError):
    """Raised when there's an error registering a tool."""
    pass


class ToolNotFoundError(ToolError):
    """Raised when a tool is not found."""
    pass
