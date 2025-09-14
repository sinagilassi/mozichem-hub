# import libs
from mozichem_hub import (
    __version__,
)
from mozichem_hub.executors import ToolExecuter
from pythermodb_settings.models import Temperature, Component, Pressure
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
tool_name = "calc_flash_isothermal_ideal_vapor_ideal_liquid"

# NOTE: arguments for the tool
# temperature
temperature = Temperature(
    value=30,
    unit="C"
)

# NOTE: pressure
pressure = Pressure(
    value=7,
    unit="kPa"
)

# NOTE: components
# water
component_1 = Component(
    name="water",
    formula="H2O",
    state="l",
    mole_fraction=0.50
)
# ethanol
component_2 = Component(
    name="ethanol",
    formula="C2H5OH",
    state="l",
    mole_fraction=0.50
)

components = [component_1, component_2]

# SECTION: Execute the tool
result = tool_executer.execute_tool(
    tool_name=tool_name,
    components=components,
    temperature=temperature,
    pressure=pressure
)
print(f"Result of '{tool_name}': {result}")
