# import libs
from typing import List, Dict, Callable, Any, Set
from fastmcp.tools import Tool
# local
from ..config import app_settings
from ..resources import MoziTool


class ToolBuilder():
    """
    Builder class for managing the core functionalities of the MoziChem MCP.
    """
    # NOTE: attributes

    def __init__(self):
        """
        Initialize the MoziTools instance.
        """
        # set
        self._settings = app_settings

    def build_mozi_tools(
        self,
        mozi_tools: List[MoziTool]
    ) -> List[Tool]:
        """
        Build the MCP tools from local resources.

        Parameters
        ----------
        functions : Dict[str, Callable]
            Dictionary of functions to be included in the tools.

        Returns
        -------
        List[Tool]
            List of Tool instances built from the provided functions.

        Notes
        -----
        This method converts a list of MoziTool instances to Tool instances.
        The original function arguments are not used in this conversion,
        as the MoziTool instances already contain the necessary function references.
        """
        try:
            # SECTION: Convert MoziTool instances to Tool instances
            mcp_tools: list[Tool] = []

            for mozi_tool in mozi_tools:
                tool_ = Tool.from_function(
                    fn=mozi_tool.fn,  # Pass the function as fn parameter
                    name=mozi_tool.name,
                    description=mozi_tool.description,
                    tags=mozi_tool.tags,
                )
                mcp_tools.append(tool_)

            return mcp_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e

    def build_tools_from_function(
        self,
        functions: Dict[str, Dict[str, Callable[..., Any | str | Set]]]
    ) -> List[Tool]:
        """
        Build the MCP tools from external resources.

        Parameters
        ----------
        functions : Dict[str, Callable]
            Dictionary of functions to be included in the tools.

        Returns
        -------
        List[Tool]
            List of Tool instances built from the provided functions.
        """
        try:
            # SECTION: Convert MoziTool instances to Tool instances
            mcp_tools: list[Tool] = []

            for fn_name, fn_elements in functions.items():
                # get the function
                fn = fn_elements.get('fn', None)
                description = fn_elements.get(
                    'description', 'No description provided.')
                tags = fn_elements.get('tags', ())

                # check if function is provided
                if not fn:
                    raise ValueError(f"Function '{fn_name}' is not provided.")

                if not callable(fn):
                    raise ValueError(f"Function '{fn_name}' is not callable.")

                if not isinstance(fn_name, str):
                    raise ValueError(
                        f"Function name '{fn_name}' is not a string.")

                if not isinstance(description, str):
                    raise ValueError(
                        f"Description for function '{fn_name}' is not a string.")

                if not isinstance(tags, set):
                    raise ValueError(
                        f"Tags for function '{fn_name}' must be a set or list.")

                tool_ = Tool.from_function(
                    fn=fn,
                    name=fn_name,
                    description=description,
                    tags=tags,
                )

                # add tool
                mcp_tools.append(tool_)

            return mcp_tools
        except Exception as e:
            raise ValueError(f"Failed to build MCP tools: {e}") from e
