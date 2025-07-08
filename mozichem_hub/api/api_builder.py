# import libs
from typing import (
    List,
    Dict
)
from fastapi import FastAPI
from fastmcp import FastMCP
from contextlib import asynccontextmanager, AsyncExitStack
# local
from ..docs import MoziChemMCP


class APIBuilder:
    """
    APIBuilder is a class to build a FastAPI application with optional configuration.
    """
    # NOTE: attributes

    def __init__(
        self,
        mcps: Dict[str, FastMCP],

    ):
        """
        Initialize the APIBuilder with optional parameters.

        Parameters
        ----------
        mcps : Dict[str, FastMCP]
            A dictionary of FastMCP instances where the key is the MCP name and the value is

        Notes
        -----
        The `kwargs` can include FastAPI parameters such as:
        - `title`: Title of the API.
        - `version`: Version of the API.
        - `description`: Description of the API.
        - `openapi_url`: URL for the OpenAPI schema.
        - `docs_url`: URL for the Swagger UI documentation.
        - `redoc_url`: URL for the ReDoc documentation.
        - `debug`: Whether to enable debug mode.

        """
        # NOTE:
        self.mcps = mcps

        # NOTE: mcps
        self.mcp_apps = {
            name: mcp.http_app(path="/mcp") for name, mcp in self.mcps.items()
        }
