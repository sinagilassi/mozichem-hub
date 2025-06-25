# import libs

# locals
from ..docs import MoziChemMCP


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

    def list_tools(self):
        """
        List all available tools in the MoziChem MCP.

        Returns
        -------
        list
            A list of tool names available in the MCP.
        """
        return self.mcp.tools_info()

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
        pass
