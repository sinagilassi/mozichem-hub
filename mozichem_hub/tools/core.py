# import libs

# local
from ..config import app_settings
from ..utils import ToolsReferences


class MoziTools():
    """
    MoziTools class for managing the core functionalities of the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the MoziTools instance.
        """
        # set
        self._settings = app_settings

        # NOTE: Initialize the ToolsReferences instance
        self.ToolsReferences_ = ToolsReferences()

    def load_tools(self):
        """
        Load tools for the MoziChem MCP.

        This method is responsible for loading the necessary tools
        that will be used in the MoziChem MCP.
        """
        try:
            # Load tools logic here
            tools_references = self.ToolsReferences_.load_references()
            if not tools_references:
                raise ValueError("No tools references found.")
        except Exception as e:
            raise ValueError(f"Failed to load tools: {e}") from e
