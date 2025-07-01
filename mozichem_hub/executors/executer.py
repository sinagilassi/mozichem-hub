# import libs
from typing import Dict, Callable, Any
# locals
from ..docs import MoziChemMCP
from ..resources import MoziTool


class ToolExecuter:
    """
    ToolExecuter class for executing tools in the MoziChem Hub.
    """

    def __init__(self, mozichem_mcp: MoziChemMCP):
        """
        Initialize the ToolExecuter with the given MCP instance.
        """
        # NOTE: store the MoziChemMCP instance
        self.mcp = mozichem_mcp

    def get_tools(self) -> Dict[str, Callable[..., Any]]:
        """
        List all available tools in the MoziChem MCP.

        Returns
        -------
        list
            A list of tool names available in the MCP.
        """
        try:
            # SECTION: Retrieve the tools information from the MCP
            tools_info = self.mcp.tools_info()

            # check if tools_info is not None
            if tools_info is None:
                raise Exception("No tools available in the MoziChem MCP.")

            # Extract the functions from the tools information
            mozi_tools = tools_info.get("functions", {})

            if not mozi_tools:
                raise Exception(
                    "No functions found in the MoziChem MCP tools.")

            # SECTION: init tools dictionary
            tools = {}

            # loop through the functions and create a dictionary of tool names and their information
            for mozi_tool in mozi_tools:
                if isinstance(mozi_tool, MoziTool):
                    tool_name = mozi_tool.name
                    tools[tool_name] = mozi_tool.fn
                else:
                    raise TypeError(
                        f"Expected MoziTool instance, got {type(mozi_tool)}")

            return tools
        except Exception as e:
            raise Exception(f"Error retrieving tools: {e}")

    def _get_tool(self, tool_name: str):
        """
        Get the function associated with a tool by its name.

        Parameters
        ----------
        tool_name : str
            The name of the tool to retrieve information for.

        Returns
        -------
        dict
            A dictionary containing the tool's information.
        """
        try:
            # Retrieve the tool information from the MCP
            tools = self.get_tools()

            # check if the tool exists
            if tool_name not in tools.keys():
                raise ValueError(
                    f"Tool '{tool_name}' not found in the MoziChem MCP.")

            # Return the tool function
            return tools[tool_name]

        except Exception as e:
            raise Exception(
                f"Error retrieving tool info for '{tool_name}': {e}")

    def execute_tool(self, tool_name: str, *args, **kwargs):
        """
        Execute a tool by its name with the provided arguments.

        Parameters
        ----------
        tool_name : str
            The name of the tool to execute.
        *args : tuple
            Positional arguments for the tool.
        **kwargs : dict
            Keyword arguments for the tool.

        Returns
        -------
        Any
            The result of the tool execution.
        """
        try:
            # Get the tool function
            tool_function = self._get_tool(tool_name)

            # Execute the tool with the provided arguments
            result = tool_function(*args, **kwargs)

            return result
        except Exception as e:
            raise Exception(f"Error executing tool '{tool_name}': {e}")
