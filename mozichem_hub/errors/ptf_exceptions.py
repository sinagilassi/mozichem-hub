# PTF (pyThermoFlash) Exception Classes and Messages

class PTFError(Exception):
    """Base exception for all PTF-related errors."""
    pass


class PTFCalculationError(PTFError):
    """Raised when PTF calculation operations fail."""
    pass


class PTFInitializationError(PTFError):
    """Raised when PTF VLE initialization fails."""
    pass


class PTFModelSourceError(PTFError):
    """Raised when building model source for PTF fails."""
    pass


class PTFComponentError(PTFError):
    """Raised when component processing for PTF fails."""
    pass


class PTFFeedSpecificationError(PTFError):
    """Raised when setting feed specification fails."""
    pass


class PTFSolverError(PTFError):
    """Raised when PTF solver operations fail."""
    pass


# Error Messages
PTF_CALCULATION_ERROR_MSG = "PTF calculation failed"
PTF_INITIALIZATION_ERROR_MSG = "PTF VLE initialization failed"
PTF_MODEL_SOURCE_ERROR_MSG = "PTF model source building failed"
PTF_COMPONENT_ERROR_MSG = "PTF component processing failed"
PTF_FEED_SPECIFICATION_ERROR_MSG = "PTF feed specification setting failed"
PTF_SOLVER_ERROR_MSG = "PTF solver operation failed"
