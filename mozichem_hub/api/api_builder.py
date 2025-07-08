# import libs
import uvicorn
from typing import (
    Dict
)
from fastapi import FastAPI
from fastmcp import FastMCP
from contextlib import asynccontextmanager, AsyncExitStack
# local


class MoziChemAPI:
    """
    APIBuilder is a class to build a FastAPI application with optional configuration.
    """
    # NOTE: attributes

    def __init__(
        self,
        mcps: Dict[str, FastMCP],
        host: str = "127.0.0.1",
        port: int = 8000,
        reload: bool = False,
        workers: int = 1,
        log_level: str = "info",
        **kwargs
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
        # NOTE: set
        self.mcps = mcps
        self.host = host
        self.port = port
        self.reload = reload
        self.workers = workers
        self.log_level = log_level
        # NOTE: kwargs
        # Store additional FastAPI configuration parameters
        self._kwargs = kwargs

        # SECTION: mcps setup
        self.mcp_apps = {
            name: mcp.http_app(path="/mcp") for name, mcp in self.mcps.items()
        }

        # SECTION: Create FastAPI app with lifespan passed to constructor
        self.app = FastAPI(lifespan=self._combined_lifespan, **self._kwargs)

        # Mount MCP apps dynamically
        self._mount_mcp_apps()

        # SECTION: Async context manager for cleanup
        # Set combined lifespan
        # self.app.router.lifespan_context = self._combined_lifespan

    def _mount_mcp_apps(self):
        """
        Mount all MCP apps at their respective paths.
        """
        for name, mcp_app in self.mcp_apps.items():
            self.app.mount(f"/{name}", mcp_app)

    @asynccontextmanager
    async def _combined_lifespan(self, app: FastAPI):
        """
        Combine all MCP app lifespans into a single context.
        """
        async with AsyncExitStack() as stack:
            for mcp_app in self.mcp_apps.values():
                await stack.enter_async_context(mcp_app.lifespan(app))
            yield

    def run(self, **uvicorn_kwargs):
        """
        Start the Uvicorn server with optional overrides.

        Parameters
        ----------
        **uvicorn_kwargs : dict
            Optional keyword arguments to override Uvicorn settings.
        """
        uvicorn.run(
            self.app,
            host=uvicorn_kwargs.get("host", self.host),
            port=uvicorn_kwargs.get("port", self.port),
            reload=uvicorn_kwargs.get("reload", self.reload),
            workers=uvicorn_kwargs.get("workers", self.workers),
            log_level=uvicorn_kwargs.get("log_level", self.log_level),
        )
