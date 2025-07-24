# PTM (pyThermoModels) Exception Classes and Messages

class PTMError(Exception):
    """Base exception for all PTM-related errors."""
    pass


class PTMCalculationError(PTMError):
    """Raised when PTM calculation operations fail."""
    pass


class PTMInitializationError(PTMError):
    """Raised when PTM EOS initialization fails."""
    pass


class PTMModelSourceError(PTMError):
    """Raised when building model source for PTM fails."""
    pass


class PTMComponentError(PTMError):
    """Raised when component processing for PTM fails."""
    pass


class PTMFeedSpecificationError(PTMError):
    """Raised when setting feed specification fails."""
    pass


class PTMSolverError(PTMError):
    """Raised when PTM solver operations fail."""
    pass


class PTMReferenceError(PTMError):
    """Raised when custom reference initialization fails."""
    pass


class PTMFugacityError(PTMError):
    """Raised when fugacity calculation fails."""
    pass


class PTMRootsAnalysisError(PTMError):
    """Raised when EOS roots analysis fails."""
    pass


# Error Messages
PTM_CALCULATION_ERROR_MSG = "PTM calculation failed"
PTM_INITIALIZATION_ERROR_MSG = "PTM EOS initialization failed"
PTM_MODEL_SOURCE_ERROR_MSG = "PTM model source building failed"
PTM_COMPONENT_ERROR_MSG = "PTM component processing failed"
PTM_FEED_SPECIFICATION_ERROR_MSG = "PTM feed specification setting failed"
PTM_SOLVER_ERROR_MSG = "PTM solver operation failed"
PTM_REFERENCE_ERROR_MSG = "PTM custom reference initialization failed"
PTM_FUGACITY_ERROR_MSG = "PTM fugacity calculation failed"
PTM_ROOTS_ANALYSIS_ERROR_MSG = "PTM EOS roots analysis failed"
