# import libs
from mozichem_hub import (
    __version__,
    create_mozichem_mcp,
    get_mozichem_mcp
)
from rich import print

# version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: mcp names
mcp_names = get_mozichem_mcp()
print(f"mcp names: {mcp_names}")

# SECTION: Build the MCP server
thermo_models_mcp = create_mozichem_mcp(name="thermo-models-mcp")

# NOTE: mcp tools
# tools_info = thermo_models_mcp.tools_info()
# print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: Serve the MCP server
# thermo_models_mcp.run(transport='streamable-http')

if __name__ == "__main__":
    # run the MCP server
    # thermo_models_mcp.run(transport='stdio')
    # http transport
    thermo_models_mcp.run(transport='streamable-http')
