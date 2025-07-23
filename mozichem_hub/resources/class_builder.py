# import libs
import logging
from typing import (
    Optional,
    Union,
)
# local
# class lists
from .ptmcore import PTMCore
from .ptfcore import PTFCore
from .ptdbcore import PTDBCore


class MCPClassBuilder:
    """
    MCPClassBuilder class for building MCP classes.
    """
    # NOTE: attributes
    _mcp_classes = {
        'PTMCore': PTMCore,
        'PTFCore': PTFCore,
        'PTDBCore': PTDBCore
    }

    def __init__(self):
        """
        Initialize the MCPClassBuilder instance.
        """
        # SECTION: Initialize the MCP classes
        self._mcp_classes = MCPClassBuilder._mcp_classes

    @classmethod
    def get_mcp_class(
        cls,
        mcp_name: str
    ) -> Optional[Union[PTMCore, PTFCore, PTDBCore]]:
        """
        Get the MCP class by its name.

        Parameters
        ----------
        mcp_name : str
            The name of the MCP class to retrieve.

        Returns
        -------
        Optional[Union[PTMCore, PTFCore, PTDBCore]]
            The corresponding MCP class or None if not found.
        """
        try:
            return cls._mcp_classes.get(mcp_name, None)
        except Exception as e:
            logging.error(f"Failed to retrieve MCP class '{mcp_name}': {e}")
            return None
