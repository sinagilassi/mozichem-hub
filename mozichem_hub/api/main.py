# import libs
from fastapi import FastAPI
from typing import List, Dict
from ..docs import MoziChemMCP
# local


class MozichemHubAPI:
    """
    MoziChemHub API is a class to build a RESTful API using MCP.
    """
    # NOTE: attributes
    mcps: Dict[str, MoziChemMCP] = {}

    def __init__(self, **kwargs):
        """
        Initialize the MoziChemHub API with optional parameters.

        Parameters
        ----------
        **kwargs : dict
            Optional keyword arguments for configuration.
            For example, you can pass 'host', 'port', 'debug', etc.
        """
        # NOTE: initialize attributes
        self._kwargs = kwargs

    def add_mcp(self, mcp: MoziChemMCP):
        """
        Add a MoziChem MCP to the API.

        Parameters
        ----------
        mcp : MoziChemMCP
            An instance of a MoziChem MCP to be added to the API.
        """
        if not isinstance(mcp, MoziChemMCP):
            raise TypeError("mcp must be an instance of MoziChemMCP")
        self.mcps[mcp.name] = mcp

    def remove_mcp(self, mcp_name: str):
        """
        Remove a MoziChem MCP from the API.

        Parameters
        ----------
        mcp_name : str
            The name of the MoziChem MCP to be removed.
        """
        if mcp_name in self.mcps:
            del self.mcps[mcp_name]
        else:
            raise KeyError(f"MCP '{mcp_name}' not found in the API.")

    def remove_all_mcps(self):
        """
        Remove all MoziChem MCPs from the API.
        """
        self.mcps.clear()

    def create_api(self) -> FastAPI:
        """
        Create a FastAPI instance with the registered MoziChem MCPs.

        Returns
        -------
        FastAPI
            An instance of FastAPI with the registered MoziChem MCPs.
        """
        app = FastAPI(**self._kwargs)

        return app
