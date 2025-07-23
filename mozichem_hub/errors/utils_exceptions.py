# import libs

# Error messages
LOADER_ERROR_MSG = "Error loading data."
FILE_NOT_FOUND_ERROR_MSG = "File not found."
INVALID_FILE_FORMAT_ERROR_MSG = "Invalid file format."
LOADING_YML_ERROR_MSG = "Error loading YAML file."
LOADING_REFERENCE_ERROR_MSG = "Error loading reference."
LISTING_REFERENCE_ERROR_MSG = "Error listing references."
INVALID_FOLDER_PATH_ERROR_MSG = "Invalid folder path."


class LoaderError(Exception):
    """Base exception for all loader-related errors."""
    pass


class FileNotFoundError(LoaderError):
    """Raised when a file is not found."""
    pass


class InvalidFileFormatError(LoaderError):
    """Raised when a file has an invalid format."""
    pass


class LoadingYmlError(LoaderError):
    """Raised when there's an error loading a YAML file."""
    pass


class LoadingReferenceError(LoaderError):
    """Raised when there's an error loading a reference."""
    pass


class ListingReferenceError(LoaderError):
    """Raised when there's an error listing references."""
    pass


class InvalidFolderPathError(LoaderError):
    """Raised when a folder path is invalid."""
    pass
