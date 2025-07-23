# import libs

# locals

NO_DATABOOK_FOUND_MSG = "No databook found in the reference."
REFERENCE_CONFIG_GEN_ERROR_MSG = "Failed to generate reference config."
COMPONENT_REFERENCE_CONFIG_ERROR_MSG = "Component reference config generation failed."
COMPONENT_REFERENCE_LINK_ERROR_MSG = "Component reference link generation failed."
CUSTOM_REFERENCE_INIT_ERROR_MSG = "Failed to initialize custom reference."
EMPTY_REFERENCE_CONTENT_ERROR_MSG = "Custom reference content cannot be empty. Thus, set it to None."
EMPTY_REFERENCE_CONFIG_ERROR_MSG = "Custom reference config cannot be empty. Thus, set it to None."
INVALID_REFERENCE_CONTENT_TYPE_MSG = "Custom reference content must be a string."
INVALID_REFERENCE_CONFIG_TYPE_MSG = "Custom reference config must be a string."


class NoDatabookFoundError(Exception):
    """Raised when no databook is found in the reference."""
    pass


class ReferenceConfigGenerationError(Exception):
    """Raised when reference config generation fails."""
    pass


class ReferenceLinkGenerationError(Exception):
    """Raised when reference link generation fails."""
    pass


class CustomReferenceInitializationError(Exception):
    """Raised when there's an error initializing a custom reference."""
    pass


class EmptyReferenceContentError(ValueError):
    """Raised when reference content is empty."""
    pass


class EmptyReferenceConfigError(ValueError):
    """Raised when reference config is empty."""
    pass


class InvalidReferenceContentTypeError(TypeError):
    """Raised when reference content is not a string."""
    pass


class InvalidReferenceConfigTypeError(TypeError):
    """Raised when reference config is not a string."""
    pass
