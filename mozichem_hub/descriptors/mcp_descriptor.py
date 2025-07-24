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

    @staticmethod
    def mcp_method_dependencies(
        mcp_id: str,
        method_name: str
    ) -> dict:
        """
        Get the method dependencies for a specific mcp method.

        Parameters
        ----------
        mcp_id : str
            The id of the mcp to get the method for.
        method_name : str
            The name of the method to get the descriptor for.

        Returns
        -------
        dict
            A dictionary containing the method descriptor.
        """
        try:
            # NOTE: find mcp name
            mcp_name = next(
                (
                    module['name'] for module in MCP_MODULES
                    if module['id'] == mcp_id
                ),
                None
            )

            # check if mcp name exists
            if not mcp_name:
                raise ValueError(f"MCP with id '{mcp_id}' not found.")

            # NOTE: load the mcp descriptor
            mcp_descriptor = MCPDescriptor().mcp_descriptor(mcp_name)

            return mcp_descriptor[method_name]
        except Exception as e:
            raise ValueError(f"Failed to load MCP method: {e}") from e

    @staticmethod
    def mcp_method_reference_config(
        mcp_id: str,
        method_name: str
    ) -> dict:
        """
        Get the method config for a specific mcp method.

        Parameters
        ----------
        mcp_id : str
            The id of the mcp to get the method for.
        method_name : str
            The name of the method to get the config for.

        Returns
        -------
        dict
            A dictionary containing the method config.
        """
        try:
            # NOTE: find mcp name
            mcp_name = next(
                (
                    module['name'] for module in MCP_MODULES
                    if module['id'] == mcp_id
                ),
                None
            )

            # check if mcp name exists
            if not mcp_name:
                raise ValueError(f"MCP with id '{mcp_id}' not found.")

            # NOTE: load the mcp descriptor
            mcp_descriptor = MCPDescriptor().mcp_descriptor(mcp_name)

            # NOTE: check if method exists
            if method_name not in mcp_descriptor:
                raise ValueError(
                    f"Method '{method_name}' not found in MCP '{mcp_name}'."
                )

            # NOTE: get method config
            config = mcp_descriptor[method_name].get('CONFIG', {})
            if not config:
                raise ValueError(
                    f"No config found for method '{method_name}' in MCP '{mcp_name}'."
                )

            # ! build config for all components
            reference_config = {
                "ALL": config
            }

            # return the reference config
            return reference_config
        except Exception as e:
            raise ValueError(f"Failed to load MCP method config: {e}") from e

    @staticmethod
    def mcp_method_reference_inputs(
        mcp_id: str,
        method_name: str
    ):
        """
        Get all reference inputs for a specific mcp method.

        Parameters
        ----------
        mcp_id : str
            The id of the mcp to get the method for.
        method_name : str
            The name of the method to get the reference link for.

        Returns
        -------
        dict
            A dictionary containing the method data and equations.
        """
        try:
            # NOTE: find mcp name
            mcp_name = next(
                (
                    module['name'] for module in MCP_MODULES
                    if module['id'] == mcp_id
                ),
                None
            )

            # check if mcp name exists
            if not mcp_name:
                raise ValueError(f"MCP with id '{mcp_id}' not found.")

            # NOTE: load the mcp descriptor
            mcp_descriptor = MCPDescriptor().mcp_descriptor(mcp_name)

            # NOTE: check if method exists
            if method_name not in mcp_descriptor:
                raise ValueError(
                    f"Method '{method_name}' not found in MCP '{mcp_name}'."
                )

            # NOTE:reference inputs
            reference_inputs = mcp_descriptor[method_name].get(
                'REFERENCE_INPUTS', {})

            return reference_inputs
        except Exception as e:
            raise ValueError(
                f"Failed to load MCP method reference link: {e}") from e
