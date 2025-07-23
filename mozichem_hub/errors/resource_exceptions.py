# import libs

# Error messages
MODEL_SOURCE_BUILD_ERROR_MSG = "Error building model source."
COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG = "Error building component model source."
HUB_INITIALIZATION_ERROR_MSG = "Error initializing Hub."
THERMODB_REGISTRATION_ERROR_MSG = "Error registering thermodynamic database."
COMPONENT_THERMODB_BUILD_ERROR_MSG = "Error building component thermodynamic database."
FUNCTION_DISPATCHER_ERROR_MSG = "Error in function dispatcher."
TOOL_BUILDER_ERROR_MSG = "Error in tool builder."


class ResourceError(Exception):
    """Base exception for all resource-related errors."""
    pass


class ModelSourceBuildError(ResourceError):
    """Raised when there's an error building a model source."""
    pass


class ComponentModelSourceBuildError(ModelSourceBuildError):
    """Raised when there's an error building a component model source."""
    pass


class HubInitializationError(ResourceError):
    """Raised when there's an error initializing the Hub."""
    pass


class ThermoDBRegistrationError(ResourceError):
    """Raised when there's an error registering a thermodynamic database."""
    pass


class ComponentThermoDBBuildError(ResourceError):
    """Raised when there's an error building a component thermodynamic database."""
    pass


class FunctionDispatcherError(ResourceError):
    """Raised when there's an error in the function dispatcher."""
    pass


class ToolBuilderError(ResourceError):
    """Raised when there's an error in the tool builder."""
    pass
