# import libs
from mozichem_hub import (
    __version__,
)
from mozichem_hub.executors import ToolExecuter
from mozichem_hub.models import Temperature, Component
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
flash_calculations_mcp = create_mozichem_mcp(name="flash-calculations-mcp")

# NOTE: mcp tools
# tools_info = thermo_models_mcp.tools_info()
# print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: Create a ToolExecuter instance
tool_executer = ToolExecuter(mozichem_mcp=flash_calculations_mcp)
# all tools
tools_ = tool_executer.get_tools()
print(f"All tools: {tools_}")

# select a tool to execute
tool_name = "calc_bubble_pressure_ideal_vapor_ideal_liquid"

# NOTE: arguments for the tool
# temperature
temperature = Temperature(
    value=80,
    unit="C"
)

# NOTE: components
# benzene
component_1 = Component(
    name="benzene",
    formula="C6H6",
    state="l",
    mole_fraction=0.26
)
# toluene
component_2 = Component(
    name="toluene",
    formula="C7H8",
    state="l",
    mole_fraction=0.74
)

components = [component_1, component_2]

# SECTION: Execute the tool
result = tool_executer.execute_tool(
    tool_name=tool_name,
    components=components,
    temperature=temperature,
)
print(f"Result of '{tool_name}': {result}")
