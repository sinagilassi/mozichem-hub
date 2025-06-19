# import libs
from fastmcp import FastMCP
# local
from .docs import MoziServer


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
        MoziServer_ = MoziServer(name=name)

        return MoziServer_._build_mcp()
    except Exception as e:
        raise Exception(f"Failed to build mcp server: {e}") from e


def serve_mcp(mcp: FastMCP, **kwargs):
    """
    Serve the mcp server.

    Parameters
    ----------
    mcp : FastMCP
        The mcp server instance to serve.
    **kwargs : dict
        Additional keyword arguments for serving the mcp server.
        - transport : str
            The transport protocol to use, default is 'stdio'.
        - host : str
            The host address to bind the server, default is '127.0.0.1'.
        - port : int
            The port number to bind the server, default is 8000.
        - path : str
            The path for the server, default is '/mcp'.
        - log_level : str
            The logging level for the server, default is 'DEBUG'.
    """
    try:
        # SECTION: Server parameters
        transport = kwargs.get("transport", "stdio")
        host = kwargs.get("host", "127.0.0.1")
        port = kwargs.get("port", 8000)
        path = kwargs.get("path", "/mcp")
        log_level = kwargs.get("log_level", "DEBUG")

        # SECTION: Start the mcp server
        mcp.run(
            transport=transport,
            host=host,
            port=port,
            path=path,
            log_level=log_level
        )
    except Exception as e:
        raise Exception(f"Failed to serve mcp server: {e}") from e
