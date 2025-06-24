# import libs
from typing import List, Dict, Callable, Any
# local
from ..utils import Loader
from ..descriptors import MCPDescriptor
from .models import MoziTool, MoziToolArg


class ToolBuilder:
    """
    ToolBuilder class for building MoziFunctions and MoziTools.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the Builder instance.
        """
        # SECTION: Initialize tool descriptor
        self.MCPDescriptor_ = MCPDescriptor()

        # NOTE: Load tools references
        self.mozi_mcp_references = self.load_mozi_mcp_references()

    def load_mozi_mcp_references(self):
        """
        Load all references from the tool descriptor.
        """
        try:
            # Load tools logic here
            tools_references = self.MCPDescriptor_.mcp_all_descriptor()
            if not tools_references:
                raise ValueError("No tools references found.")

            return tools_references
        except Exception as e:
            raise ValueError(f"Failed to load tools: {e}") from e

    def build_mozi_tools(
        self,
        mcp_name: str,
        local_functions: Dict[str, Callable[..., Any]]
    ) -> List[MoziTool]:
        """
        Build the Mozi tools.

        Parameters
        ----------
        local_functions : Dict[str, Callable]
            A dictionary of local functions available in the MoziChem Hub.

        Returns
        -------
        List[MoziTool]
            A list of MoziTool instances built from the tools references.
        """
        try:
            # SECTION: get the tools references
            tool_references = self.mozi_mcp_references.get(mcp_name, None)

            if not tool_references:
                raise ValueError(
                    f"No tools references found for MCP '{mcp_name}'.")

            # NOTE: Mozi tools list
            mozi_tools: List[MoziTool] = []

            # loop through each tool reference
            for tool_ref, tool_value in tool_references.items():
                # Create MoziTool instance
                # NOTE: name
                name_ = tool_value.get('NAME', None)
                if not name_:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid name.")

                # NOTE: reference function
                fn = local_functions.get(name_, None)
                if not fn:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid function.")

                # description
                description_ = tool_value.get('DESCRIPTION', None)
                if not description_:
                    raise ValueError(
                        f"Tool reference '{tool_ref}' does not have a valid description.")

                # tags
                tags_ = tool_value.get('TAGS', ())
                if not isinstance(tags_, (set)):
                    raise ValueError(
                        f"Tool reference '{tool_ref}' tags must be a list.")

                # Create MoziTool instance
                mozi_tool = MoziTool(
                    name=name_,
                    fn=fn,  # Use a dummy function for now
                    description=description_,
                    tags=tags_

                )

                # Append to the list of Mozi tools
                mozi_tools.append(mozi_tool)

            # Return the list of Mozi tools
            return mozi_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e
