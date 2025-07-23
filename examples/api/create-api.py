# import libs
import uvicorn
from mozichem_hub import (
    __version__,
)
from mozichem_hub import create_api
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
# NOTE: eos-models-mcp
eos_models_mcp = create_mozichem_mcp(
    name="eos-models-mcp"
)
# NOTE: flash-calculation-mcp
flash_calculations_mcp = create_mozichem_mcp(
    name="flash-calculations-mcp"
)
# NOTE: thermodynamic-properties-mcp
thermodynamic_properties_mcp = create_mozichem_mcp(
    name="thermodynamic-properties-mcp"
)

# SECTION: mcp tools
tools_info = eos_models_mcp.tools_info()
print(f"Tools available in 'thermo-models-mcp': {tools_info}")

# SECTION: create and run the API
# NOTE: create the API
mcp_api = create_api(
    mcps=[
        eos_models_mcp,
        flash_calculations_mcp,
        thermodynamic_properties_mcp
    ],
    title="MoziChem Hub API",
    description="API for MoziChem Hub with multiple MCPs.",
    version=__version__
)

# NOTE: run the API
if __name__ == "__main__":
    uvicorn.run(
        mcp_api,
        host="127.0.0.1",
        port=8000
    )
