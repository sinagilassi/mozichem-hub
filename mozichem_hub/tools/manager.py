# import libs
from typing import Dict, Callable, Optional
# local
from .builder import ToolBuilder
from ..manager import FunctionDispatcher


class ToolManager(ToolBuilder):
    """
    ToolManager class for managing tools in the MoziChem Hub.
    """
    # NOTE: attributes
    _tools = []

    def __init__(self):
        """
        Initialize the ToolManager instance.
        """
        # SECTION: Initialize the Builder
        ToolBuilder().__init__()

        # SECTION: Load functions
        self._tools = self._load_mozi_tools()

    def _load_mozi_tools(self):
        """
        Load the MoziChem tools, already defined in the MoziChem Hub.
        """
        try:
            # NOTE: init FunctionDispatcher
            self.FunctionDispatcher_ = FunctionDispatcher()

            # SECTION: Load tools from FunctionDispatcher
            self._tools = self.FunctionDispatcher_.get_functions()
        except Exception as e:
            raise Exception(f"Failed to load MoziChem tools: {e}") from e

    def _build_tools(
        self,
        custom_tools: Optional[Dict[str, Callable]] = None
    ):
        """
        Build the tools for the MoziChem Hub.

        This method is responsible for building the tools that will be
        registered with the MoziChem Hub.
        """
        try:
            # SECTION: Build Mozi tools
            self._tools = self.build_mcp_tools()
            return self._tools
        except Exception as e:
            raise ValueError(f"Failed to build tools: {e}") from e

    def launch(self):
        """
        Launch the ToolManager.

        This method is called to start the ToolManager and prepare it for serving.
        """
        try:
            # SECTION: Build tools
            self._build_tools()
            return self._tools
        except Exception as e:
            raise RuntimeError(f"Failed to launch ToolManager: {e}") from e
