# import libs
from typing import List, Dict, Callable
# local
from ..utils import Loader
from .models import MoziTool, MoziToolArg


class ToolBuilder:
    """
    Builder class for building MoziFunctions and MoziTools.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the Builder instance.
        """
        # SECTION: Initialize the Loader instance
        # used to load app references
        self.Loader_ = Loader()

        # NOTE: Load tools references
        self.mozi_tools_references = self.load_mozi_tools_reference()

    def load_mozi_tools_reference(self):
        """
        Load tools for the MoziChem MCP.

        This method is responsible for loading the necessary tools
        that will be used in the MoziChem MCP.
        """
        try:
            # Load tools logic here
            tools_references = self.Loader_.load_references()
            if not tools_references:
                raise ValueError("No tools references found.")

            return tools_references
        except Exception as e:
            raise ValueError(f"Failed to load tools: {e}") from e

    def build_mozi_tools(
        self,
        local_functions: Dict[str, Callable]
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
            # NOTE: Mozi tools list
            mozi_tools = []

            # loop through each tool reference
            for tool_ref, tool_value in self.mozi_tools_references.items():
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

                # tags
                tags_ = tool_value.get('TAGS', ())
                if not isinstance(tags_, set):
                    raise ValueError(
                        f"Tool reference '{tool_ref}' tags must be a list.")

                # Build MoziToolArgs instances
                mozi_args = []
                for arg_name, arg_value in args_.items():
                    # Create MoziToolArgs instance
                    mozi_args.append(MoziToolArg(
                        name=arg_name,
                        type=arg_value.get('type', 'str'),
                        description=arg_value.get('description', ''),
                        default=arg_value.get('default', None),
                        hide=arg_value.get('hide', False),
                        required=arg_value.get('required', False)
                    ))

                # Create MoziTool instance
                mozi_tool = MoziTool(
                    name=name_,
                    fn=fn,  # Use a dummy function for now
                    reference=reference_,
                    description=description_,
                    args=mozi_args,  # Use values to get a list of MoziToolArg instances
                    tags=tags_

                )

                # Append to the list of Mozi tools
                mozi_tools.append(mozi_tool)

            # Return the list of Mozi tools
            return mozi_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e
