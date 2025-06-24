# import libs
from mozichem_hub import __version__, MoziChemMCP
from rich import print

# version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: create app

app = MoziChemMCP(name="mcp1")


# SECTION: add custom functions


# SECTION: run
app.run()
