# import libs

# locals

NO_DATABOOK_FOUND_MSG = "No databook found in the reference."
REFERENCE_CONFIG_GEN_ERROR_MSG = "Failed to generate reference config."
COMPONENT_REFERENCE_CONFIG_ERROR_MSG = "Component reference config generation failed."
COMPONENT_REFERENCE_LINK_ERROR_MSG = "Component reference link generation failed."


class NoDatabookFoundError(Exception):
    """Raised when no databook is found in the reference."""
    pass


class ReferenceConfigGenerationError(Exception):
    """Raised when reference config generation fails."""
    pass


class ReferenceLinkGenerationError(Exception):
    """Raised when reference link generation fails."""
    pass
