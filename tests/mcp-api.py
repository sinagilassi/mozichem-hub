# import libs
import uvicorn
from mozichem_hub import (
    __version__,
)
from mozichem_hub.prebuilt import (
    create_mozichem_mcp,
    get_mozichem_mcp
)
from mozichem_hub.api import MoziChemHubAPI
from rich import print

# version
print(f"[bold green]Mozichem Hub Version: {__version__}[/bold green]")

# SECTION: mcp names
mcp_names = get_mozichem_mcp()
print(f"mcp names: {mcp_names}")

# SECTION: Build the MCP server
thermo_models_mcp = create_mozichem_mcp(name="eos-models-mcp")

# NOTE: mcp tools
# tools_info = thermo_models_mcp.tools_info()
# print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: create and run the API
mozichem_api = MoziChemHubAPI()

# NOTE: add the MCP to the API
mozichem_api.add_mozichem_mcp(thermo_models_mcp)

# NOTE: create the API
mcp_api = mozichem_api.create_api()

# NOTE: run the API
if __name__ == "__main__":
    uvicorn.run(
        mcp_api,
        host="127.0.0.1",
        port=8000
    )
