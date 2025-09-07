# import libs
from mozichem_hub.descriptors import MCPDescriptor, get_mcp_ignore_state_props
from rich import print

# SECTION: get mcp method ignore state props
mcp_id = "PTMCore"
method_name = "calc_gas_component_fugacity"
ignore_state_props = MCPDescriptor.mcp_method_ignore_state_props(
    mcp_id=mcp_id,
    method_name=method_name
)
print(
    f"[bold green]Ignore state props for method '{method_name}' in MCP '{mcp_id}':[/bold green] {ignore_state_props}")

# SECTION: get mcp method ignore state props using function
mcp_name = "eos-models-mcp"
method_name = "calc_gas_component_fugacity"
ignore_state_props = get_mcp_ignore_state_props(
    mcp_name=mcp_name,
    method_name=method_name
)
print(
    f"[bold green]Ignore state props for method '{method_name}' in MCP '{mcp_name}':[/bold green] {ignore_state_props}")
