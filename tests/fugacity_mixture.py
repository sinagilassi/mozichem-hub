# import libs
from mozichem_hub import (
    __version__,
    create_mozichem_mcp,
    get_mozichem_mcp,
)
from mozichem_hub.executors import ToolExecuter
from mozichem_hub.models import Temperature, Pressure, Component
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
tool_name = "cal_fugacity_mixture"

# arguments for the tool
temperature = Temperature(
    value=298.15,
    unit="K"
)

pressure = Pressure(
    value=10,
    unit="bar"
)

# methane
component_1 = Component(
    name="methane",
    formula="CH4",
    state="g",
    mole_fraction=0.35
)
# ethane
component_2 = Component(
    name="ethane",
    formula="C2H6",
    state="g",
    mole_fraction=0.65
)

components = [component_1, component_2]

eos_model = "SRK"

# SECTION: Execute the tool
result = tool_executer.execute_tool(
    tool_name=tool_name,
    components=components,
    temperature=temperature,
    pressure=pressure,
    eos_model=eos_model
)
print(f"Result of '{tool_name}': {result}")
