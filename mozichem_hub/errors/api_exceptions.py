# import libs

# Error messages
API_CREATION_ERROR_MSG = "Error creating API."
INVALID_MCP_TYPE_ERROR_MSG = "MCPs must be a MoziChemMCP instance or a list of MoziChemMCP instances."
INVALID_MCP_LIST_ITEM_ERROR_MSG = "All items in MCPs list must be instances of MoziChemMCP."
MCP_ADDITION_ERROR_MSG = "Error adding MCPs to API."


class APIError(Exception):
    """Base exception for all API-related errors."""
    pass


class APICreationError(APIError):
    """Raised when there's an error creating the API."""
    pass


class InvalidMCPTypeError(APIError):
    """Raised when the MCP argument has an invalid type."""
    pass


class InvalidMCPListItemError(APIError):
    """Raised when an item in the MCP list is not a MoziChemMCP instance."""
    pass


class MCPAdditionError(APIError):
    """Raised when there's an error adding MCPs to the API."""
    pass
