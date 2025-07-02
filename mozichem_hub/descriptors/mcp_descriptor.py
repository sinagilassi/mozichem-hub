# import libs
import logging
# locals
from ..utils import Loader
from ..config import MCP_MODULES


class MCPDescriptor:
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

    def mcp_all_descriptor(self):
        """
        Get all mcp descriptors

        Returns
        -------
        list
            A list of dictionaries containing all tool descriptors.
        """
        try:
            # NOTE: int reference
            mcp_references = {}

            # SECTION: load from MCP_MODULES
            for mcp_module in MCP_MODULES:
                # get mcp name
                mcp_name = mcp_module.get('name', None)

                if not mcp_name:
                    raise ValueError(
                        "MCP module does not have a name defined.")

                # load reference
                _ref = self.mcp_descriptor(mcp_name)

                if not _ref:
                    raise ValueError(
                        f"Failed to load descriptor for MCP '{mcp_name}'.")

                # add to mcp references
                mcp_references[mcp_name] = _ref

            # NOTE: check if mcp references are empty
            if not mcp_references:
                raise ValueError("No MCP references found.")

            # references
            return mcp_references

        except Exception as e:
            raise ValueError(f"Failed to load tool descriptors: {e}") from e

    def mcp_descriptor(self, mcp_name: str) -> dict:
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
                    f"MCP module '{mcp_name}' does not have a descriptor file defined."
                )

            # NOTE: Load tools logic here
            descriptor = self.Loader_.load_yml_references(
                target_file=mcp_descriptor,
                target_folder='descriptors'
            )

            return descriptor
        except Exception as e:
            raise ValueError(f"Failed to load tool descriptor: {e}") from e

    @staticmethod
    def mcp_instructions(mcp_name: str) -> str:
        """
        Get the instructions for a specific mcp.

        Parameters
        ----------
        mcp_name : str
            The name of the mcp to get the instructions for.

        Returns
        -------
        str
            Instructions for the specified mcp.
        """
        try:
            # NOTE: load the mcp descriptor
            mcp_descriptor = MCPDescriptor().mcp_descriptor(mcp_name)

            # NOTE: check if instructions exist
            instructions = mcp_descriptor.get('INSTRUCTIONS', None)

            if not instructions:
                logging.warning(
                    f"No instructions found for MCP '{mcp_name}'. "
                    "Returning default instructions."
                )

                return (
                    "This is a MoziChem MCP server. "
                    "It is configured to run with the name: "
                    f"{mcp_name}."
                )

            return instructions
        except Exception as e:
            raise ValueError(f"Failed to load MCP instructions: {e}") from e
