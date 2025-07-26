# import libs

# Error messages
MODEL_SOURCE_BUILD_ERROR_MSG = "Error building model source."
COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG = "Error building component model source."
HUB_INITIALIZATION_ERROR_MSG = "Error initializing Hub."
THERMODB_REGISTRATION_ERROR_MSG = "Error registering thermodynamic database."
COMPONENT_THERMODB_BUILD_ERROR_MSG = "Error building component thermodynamic database."
FUNCTION_DISPATCHER_ERROR_MSG = "Error in function dispatcher."
TOOL_BUILDER_ERROR_MSG = "Error in tool builder."

# Hub-specific error messages
HUB_THERMO_HUB_BUILD_ERROR_MSG = "Error building ThermoHub instance."
HUB_THERMO_HUB_CLEAN_ERROR_MSG = "Error cleaning ThermoHub instance."
HUB_COMPONENT_REFERENCE_CONFIG_ERROR_MSG = (
    "Error setting component reference configuration."
)
HUB_COMPONENT_REFERENCE_RULE_ERROR_MSG = (
    "Error setting component reference rule."
)
HUB_COMPONENT_THERMODB_REGISTRATION_ERROR_MSG = (
    "Error registering component thermodynamic database."
)
HUB_COMPONENTS_THERMODB_REGISTRATION_ERROR_MSG = (
    "Error registering multiple component thermodynamic databases."
)
HUB_COMPONENT_MODEL_SOURCE_BUILD_ERROR_MSG = (
    "Error building component model source."
)
HUB_COMPONENTS_MODEL_SOURCE_BUILD_ERROR_MSG = (
    "Error building components model source."
)


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
    """Raised when there's an error building a component thermodynamic
    database."""
    pass


class FunctionDispatcherError(ResourceError):
    """Raised when there's an error in the function dispatcher."""
    pass


class ToolBuilderError(ResourceError):
    """Raised when there's an error in the tool builder."""
    pass


# Hub-specific exceptions
class HubThermoHubBuildError(HubInitializationError):
    """Raised when there's an error building the ThermoHub instance."""
    pass


class HubThermoHubCleanError(ResourceError):
    """Raised when there's an error cleaning the ThermoHub instance."""
    pass


class HubComponentReferenceConfigError(ResourceError):
    """Raised when there's an error setting component reference config."""
    pass


class HubComponentReferenceRuleError(ResourceError):
    """Raised when there's an error setting component reference rule."""
    pass


class HubComponentThermoDBRegistrationError(ThermoDBRegistrationError):
    """Raised when there's an error registering component thermoDB."""
    pass


class HubComponentsThermoDBRegistrationError(ThermoDBRegistrationError):
    """Raised when there's an error registering multiple component
    thermoDBs."""
    pass


class HubComponentModelSourceBuildError(ComponentModelSourceBuildError):
    """Raised when there's an error building component model source."""
    pass


class HubComponentsModelSourceBuildError(ModelSourceBuildError):
    """Raised when there's an error building components model source."""
    pass
