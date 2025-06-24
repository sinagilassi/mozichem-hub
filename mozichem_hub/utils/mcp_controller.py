# import libs
from typing import List, Optional, Dict, Any
# locals
from ..config import MCP_MODULES


class MCPController:
    """
    Controller for managing MCPs in the MoziChem Hub.
    """

    def __init__(self):
        """
        Initialize the MCPController.
        """
        self.mcp_modules = MCP_MODULES

    @staticmethod
    def mcp_names() -> List[str]:
        """
        Get the names of all available MCPs.

        Returns
        -------
        list
            List of MCP names.
        """
        return [module["name"] for module in MCP_MODULES]

    @staticmethod
    def get_mcp_info(mcp_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific MCP.

        Parameters
        ----------
        mcp_name : str
            Name of the MCP to retrieve information for.

        Returns
        -------
        dict or None
            Information about the MCP, or None if not found.
        """
        for module in MCP_MODULES:
            if module["name"] == mcp_name:
                return module
        return None

    def get_all_mcp_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available MCPs.

        Returns
        -------
        list
            List of dictionaries containing information about each MCP.
        """
        return self.mcp_modules

    def check_mcp_name(self, mcp_name: str) -> bool:
        """
        Check if the given MCP name is valid.

        Parameters
        ----------
        mcp_name : str
            Name of the MCP to check.

        Returns
        -------
        bool
            True if the MCP name is valid, False otherwise.
        """
        return mcp_name in MCPController.mcp_names()

    def check_mcp_parameters(
        self,
        properties: Dict[str, Any]
    ) -> bool:
        """
        Check if the provided properties are valid for the MCP server.

        Parameters
        ----------
        properties : dict
            Dictionary containing properties to check.

        Returns
        -------
        bool
            True if the properties are valid, False otherwise.
        """
        try:
            required_keys = [
                "transport", "host", "port", "path", "log_level"
            ]

            # check if other keys are present
            for key in required_keys:
                if key not in properties:
                    return False

            # check if the transport is valid
            if properties["transport"] not in ["stdio", "http"]:
                return False

            # check if the host is valid
            if not isinstance(properties["host"], str):
                return False

            # check if the port is valid
            if (
                not isinstance(properties["port"], int) or
                not (0 < properties["port"] < 65536)
            ):
                return False

            # check if the path is valid
            if not isinstance(properties["path"], str):
                return False

            # check if the log_level is valid
            valid_log_levels = ['debug', 'info',
                                'warning', 'error', 'critical']
            if properties["log_level"] not in valid_log_levels:
                return False

            return True
        except Exception as e:
            print(f"Error checking MCP parameters: {e}")
            return False
