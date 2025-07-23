# import libs
from typing import List
from fastapi import FastAPI
from fastmcp import FastMCP
from typing import Dict
from ..docs import MoziChemMCP
# local
from .api_builder import MoziChemAPI
from ..utils import print_ascii_art
from ..config import __version__


class MoziChemHubAPI:
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

    def add_mozichem_mcp(self, mcp: MoziChemMCP):
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

    def add_mozichem_mcps(self, mcps: List[MoziChemMCP]):
        """
        Add multiple MoziChem MCPs to the API.

        Parameters
        ----------
        mcps : List[MoziChemMCP]
            A list of MoziChem MCP instances to be added to the API.
        """
        for mcp in mcps:
            if not isinstance(mcp, MoziChemMCP):
                raise TypeError("All items must be instances of MoziChemMCP")
            self.mcps[mcp.name] = mcp

    def get_mcp_names(self) -> Dict[str, MoziChemMCP]:
        """
        Get the names of all MoziChem MCPs in the API.

        Returns
        -------
        Dict[str, MoziChemMCP]
            A dictionary where keys are MCP names and values are MoziChemMCP instances.
        """
        return self.mcps

    def get_mozichem_mcp(self, mcp_name: str) -> MoziChemMCP:
        """
        Get a MoziChem MCP by its name.

        Parameters
        ----------
        mcp_name : str
            The name of the MoziChem MCP to retrieve.

        Returns
        -------
        MoziChemMCP
            The MoziChem MCP instance associated with the given name.
        """
        if mcp_name in self.mcps:
            return self.mcps[mcp_name]
        else:
            raise KeyError(f"MCP '{mcp_name}' not found in the API.")

    def remove_mozichem_mcp(self, mcp_name: str):
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

    def remove_all_mozichem_mcps(self):
        """
        Remove all MoziChem MCPs from the API.
        """
        self.mcps.clear()

    def retrieve_mcp(self, mcp_name: str) -> FastMCP:
        """
        Retrieve a FastMCP by its name.

        Parameters
        ----------
        mcp_name : str
            The name of the MoziChem MCP to retrieve.

        Returns
        -------
        FastMCP
            The MoziChem MCP instance associated with the given name.
        """
        try:
            # Retrieve the MCP by name
            mozichem_mcp = self.mcps[mcp_name]
            if not isinstance(mozichem_mcp, MoziChemMCP):
                raise TypeError(
                    f"MCP '{mcp_name}' is not an instance of MoziChemMCP.")

            # fastmcp instance
            return mozichem_mcp.get_mcp()
        except KeyError:
            raise KeyError(
                f"MCP '{mcp_name}' not found in the API. Available MCPs: {list(self.mcps.keys())}")

    def retrieve_all_mcps(self) -> Dict[str, FastMCP]:
        """
        Retrieve all MoziChem MCPs in the API.

        Returns
        -------
        Dict[str, FastMCP]
            A dictionary where keys are MCP names and values are FastMCP instances.
        """
        return {name: mcp.get_mcp() for name, mcp in self.mcps.items()}

    def _get_all_mcps(self) -> List[str]:
        """
        Get the names of all registered MoziChem MCPs.

        Returns
        -------
        List[str]
            A list of names of all registered MoziChem MCPs.
        """
        return list(self.mcps.keys())

    def create_api(self, welcome_message: bool = True) -> FastAPI:
        """
        Create a FastAPI instance with the registered MoziChem MCPs.

        Returns
        -------
        FastAPI
            An instance of FastAPI with the registered MoziChem MCPs.
        """
        try:
            # SECTION: retrieve MCPs
            if not self.mcps:
                raise ValueError("No MoziChem MCPs registered in the API.")

            # NOTE: get fastmcp instances
            mcps = self.retrieve_all_mcps()
            if not mcps:
                raise ValueError("No FastMCP instances available.")

            # SECTION: Create APIBuilder instance
            MoziChemAPI_ = MoziChemAPI(mcps=mcps, **self._kwargs)

            # NOTE: print welcome message
            if welcome_message:
                # line
                line_1 = f"Welcome to MoziChemHub API {__version__}."
                # Adjust spacing to align properly with ASCII art border
                line_2 = "🧪 Available MCPs:"
                lines = [line_1, line_2]

                # Add each MCP on a separate indented line with emoji
                for mcp_name in self._get_all_mcps():
                    # Ensure consistent indentation for proper alignment
                    lines.append(f"  ⚗️ {mcp_name}")

                print_ascii_art(lines)

            return MoziChemAPI_.app
        except Exception as e:
            raise RuntimeError(f"Failed to create API: {str(e)}") from e
