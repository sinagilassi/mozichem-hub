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
my_mcp = create_mozichem_mcp(name="thermodynamic-properties-mcp")

# NOTE: mcp tools
# tools_info = my_mcp.tools_info()
# print(f"Tools available: {tools_info}")

# SECTION: add custom references

# SECTION: Serve the MCP server
# my_mcp.run(transport='streamable-http')

if __name__ == "__main__":
    # run the MCP server
    my_mcp.run(transport='stdio')
    # http transport
    # my_mcp.run(transport='streamable-http')
