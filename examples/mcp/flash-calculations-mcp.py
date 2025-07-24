# import libs
from mozichem_hub import (
    __version__,
)
from mozichem_hub.prebuilt import (
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
flash_calculations_mcp = create_mozichem_mcp(name="flash-calculations-mcp")

# NOTE: mcp tools
# tools_info = flash_calculations_mcp.tools_info()
# print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: add custom references

# SECTION: Serve the MCP server
# flash_calculations_mcp.run(transport='stdio')
# flash_calculations_mcp.run(transport='streamable-http')

if __name__ == "__main__":
    # run the MCP server
    flash_calculations_mcp.run(transport='stdio')
    # http transport
    # flash_calculations_mcp.run(transport='streamable-http')
