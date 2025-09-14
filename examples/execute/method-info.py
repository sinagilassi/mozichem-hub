# import libs
from mozichem_hub import (
    __version__,
)
from mozichem_hub.executors import ToolExecuter
from pythermodb_settings.models import Temperature, Pressure, Component
from mozichem_hub.prebuilt import (
    create_mozichem_mcp,
    get_mozichem_mcp
)
# log
from rich import print

# NOTE: version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: mcp names
mcp_names = get_mozichem_mcp()
print(f"mcp names: {mcp_names}")

# SECTION: Build the MCP server
thermo_models_mcp = create_mozichem_mcp(name="eos-models-mcp")

# NOTE: mcp tools
# tools_info = thermo_models_mcp.tools_info()
# print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: Create a ToolExecuter instance
tool_executer = ToolExecuter(mozichem_mcp=thermo_models_mcp)
# all tools
tools_ = tool_executer.get_tools()
print(f"All tools in 'eos-models-mcp': {tools_}")

# select a tool to execute
tool_name = "get_method_reference_inputs"

# arguments for the tool
# method name
method_name = "calc_gas_component_fugacity"


# NOTE: prompt for the tool
prompt = f"""Execute the tool '{tool_name}' with method '{method_name}'.
This tool retrieves the reference configuration for the specified method."""


# SECTION: Execute the tool
result = tool_executer.execute_tool(
    tool_name=tool_name,
    method_name=method_name
)
print(f"Result of '{tool_name}': {result}")
