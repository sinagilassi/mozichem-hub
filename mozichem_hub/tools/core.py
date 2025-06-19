# import libs
from typing import List
from fastmcp.tools import Tool
from fastmcp.tools.tool_transform import ArgTransform
# local
from ..config import app_settings
from ..utils import ToolsReferences
from .models import MoziTool, MoziToolArgs


class ToolsCore():
    """
    ToolsCore class for managing the core functionalities of the MoziChem MCP.
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

            return tools_references
        except Exception as e:
            raise ValueError(f"Failed to load tools: {e}") from e

    def build_mozi_tools(self,
                         tools_references: dict
                         ) -> List[MoziTool]:
        """
        Build the Mozi tools.

        Parameters
        ----------
        tools_references : dict
            A dictionary containing the tools references.

        Returns
        -------
        List[MoziTool]
            A list of MoziTool instances built from the tools references.
        """
        try:
            # NOTE: Mozi tools list
            mozi_tools = []

            # loop through each tool reference
            for tool_ref, tool_value in tools_references.items():
                # Create MoziTool instance
                # NOTE: name
                name_ = tool_value.get('NAME', None)
                if not name_:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid name.")

                # reference
                reference_ = tool_value.get('REFERENCE', None)
                if not reference_:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid reference.")

                # description
                description_ = tool_value.get('DESCRIPTION', None)
                if not description_:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid description.")

                # args
                args_ = tool_value.get('ARGS', {})
                if not isinstance(args_, dict):
                    raise ValueError(
                        f"Tool reference '{tool_ref}' args must be a dictionary.")

                # Build MoziToolArgs instances
                mozi_args = {}
                for arg_name, arg_value in args_.items():
                    # Create MoziToolArgs instance
                    mozi_args[arg_name] = MoziToolArgs(
                        type=arg_value.get('type', 'str'),
                        description=arg_value.get('description', ''),
                        default=arg_value.get('default', None),
                        required=arg_value.get('required', False)
                    )

                # Create MoziTool instance
                mozi_tool = MoziTool(
                    name=name_,
                    reference=reference_,
                    description=description_,
                    args=mozi_args
                )

                # Append to the list of Mozi tools
                mozi_tools.append(mozi_tool)

            # Return the list of Mozi tools
            return mozi_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e

    def build_mcp_tools(self) -> List[Tool]:
        """
        Build the MCP tools.

        This method is responsible for building the tools that will be
        registered with the MCP server.
        """
        try:
            # NOTE: Load tools references
            tools_references = self.load_tools()

            # NOTE: Build Mozi tools
            mozi_tools = self.build_mozi_tools(tools_references)

            # Convert MoziTool instances to Tool instances
            mcp_tools: list[Tool] = []

            for mozi_tool in mozi_tools:
                tool_ = Tool.from_function(
                    fn=mozi_tool.reference,  # Pass the function as fn parameter
                    name=mozi_tool.name,
                    description=mozi_tool.description,
                    arg_transforms={  # Use arg_transforms instead of args
                        arg_name: ArgTransform(
                            type=arg.type,
                            description=arg.description,
                            default=arg.default,
                            required=arg.required
                        ) for arg_name, arg in mozi_tool.args.items()
                    }
                )
                mcp_tools.append(tool_)

            return mcp_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e
