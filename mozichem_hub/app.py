# import libs
from fastmcp import FastMCP
# local
from .docs import MoziChemHub


def serve():
    """
    Serve the mcp server
    """
    print("Starting Mozichem Hub server...")


def build_mcp(name: str = "MoziChemHub") -> FastMCP:
    """
    Build the mcp server using FastMCP.

    Parameters
    ----------
    name : str
        Name of the mcp server, default is "MoziChemHub"
    """
    try:
        # SECTION: Initialize the MoziChemHub instance
        hub = MoziChemHub(name=name)

        return hub.mcp
    except Exception as e:
        raise Exception(f"Failed to build mcp server: {e}") from e


def serve_mcp(mcp: FastMCP):
    """
    Serve the mcp server.

    Parameters
    ----------
    name : str
        Name of the mcp server, default is "MoziChemHub"
    """
    try:
        # SECTION: Start the mcp server
        mcp.run()
    except Exception as e:
        raise Exception(f"Failed to serve mcp server: {e}") from e
