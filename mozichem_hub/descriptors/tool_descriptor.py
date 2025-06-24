# import libs
from ..utils import Loader
# locals
from ..config import MCP_MODULES


class ToolDescriptor:
    """
    Descriptor class for defining tools in the MoziChem Hub.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the ToolDescriptor.

        """
        # SECTION: Initialize the Loader instance
        # used to load app references
        self.Loader_ = Loader()

        # SECTION: Load tools references
        self.tool_descriptors_info = self.Loader_.list_yml_references(
            target_folder='descriptors'
        )

    def tool_descriptor(self, mcp_name: str) -> dict:
        """
        Get the descriptor for a specific tool in the MoziChem Hub.

        Parameters
        ----------
        mcp_name : str
            The name of the mcp to get the descriptor for.

        Returns
        -------
        dict
            A dictionary containing the tool descriptor.
        """
        try:
            # NOTE: get mcp module
            mcp_module = next((
                module for module in MCP_MODULES if module['name'] == mcp_name
            ), None)

            # check if mcp module exists
            if not mcp_module:
                raise ValueError(f"MCP module '{mcp_name}' not found.")

            # set descriptor file
            mcp_descriptor = mcp_module.get('descriptor', None)
            if not mcp_descriptor:
                raise ValueError(
                    f"MCP module '{mcp_name}' does not have a descriptor file defined.")

            # yml file must be provided
            mcp_descriptor = mcp_descriptor if mcp_descriptor.endswith(
                '.yml') else f"{mcp_descriptor}.yml"

            # NOTE: Load tools logic here
            tool_descriptor = self.Loader_.load_yml_references(
                target_file=mcp_descriptor,
                target_folder='descriptors'
            )

            return tool_descriptor
        except Exception as e:
            raise ValueError(f"Failed to load tool descriptor: {e}") from e

    def tool_descriptors(self):
        """
        Get all tool descriptors for the MoziChem Hub.

        Returns
        -------
        list
            A list of dictionaries containing all tool descriptors.
        """
        try:
            # NOTE: Load all tool descriptors
            tool_descriptors = []

            for descriptor_file in self.tool_descriptors_info:
                # Load each descriptor file
                descriptor = self.Loader_.load_yml_references(
                    target_file=descriptor_file,
                    target_folder='descriptors'
                )
                tool_descriptors.append(descriptor)

            return tool_descriptors
        except Exception as e:
            raise ValueError(f"Failed to load tool descriptors: {e}") from e
