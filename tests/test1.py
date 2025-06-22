# import libs
from mozichem_hub import __version__, build_mcp, serve_mcp
from rich import print

# version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: Build the MCP server
mcp = build_mcp(name="MoziChemHub")

# SECTION: add custom references


# SECTION: add custom functions


# SECTION: Serve the MCP server
serve_mcp(mcp)
