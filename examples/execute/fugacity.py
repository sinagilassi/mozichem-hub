# import libs
from mozichem_hub import (
    __version__,
)
from mozichem_hub.executors import ToolExecuter
from pythermodb_settings.models import (
    Temperature,
    Pressure,
    Component
)
from mozichem_hub.prebuilt import (
    create_mozichem_mcp,
    get_mozichem_mcp
)
# log
from rich import print
import pyThermoDB as ptdb

# NOTE: version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")
# SECTION: pyThermoDB version
print(f"[bold blue]pyThermoDB Version: {ptdb.__version__}[/bold blue]")

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
tool_name = "calc_gas_component_fugacity"

# arguments for the tool
temperature = Temperature(
    value=300.1,
    unit="K"
)

pressure = Pressure(
    value=9.99,
    unit="bar"
)

component = Component(
    name="carbon dioxide",
    formula="CO2",
    state="g"
)

eos_model = "SRK"

# NOTE: prompt for the tool
prompt = f"""Calculate the fugacity of {component.name} at {temperature.value} {temperature.unit}
and {pressure.value} {pressure.unit} using the {eos_model} EOS model."""
print(f"Prompt for '{tool_name}': {prompt}")

# SECTION: Execute the tool
result = tool_executer.execute_tool(
    tool_name=tool_name,
    component=component,
    temperature=temperature,
    pressure=pressure,
    eos_model=eos_model,
)
print(f"Result of '{tool_name}': {result}")
