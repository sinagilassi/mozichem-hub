# import libs
from fastmcp import FastMCP
from typing import (
    Optional,
    Dict,
    List,
    Callable,
    Any,
    Literal
)
# local
from .registry import RegistryMixin
from .services import ReferenceServices
from .server import MoziServer
from ..tools import ToolManager
from ..references import (
    Reference,
    ReferenceLink,
)


class MoziChemMCP(RegistryMixin, ReferenceServices):
    """
    This is the main entry point for the MoziChem Hub application.
    It initializes the MoziChemHub instance and prepares it for serving.
    custom reference and link can be passed to the MoziChemHub instance.
    """

    def __init__(
            self,
            name: str,
            reference: Optional[Reference] = None,
            reference_link: Optional[ReferenceLink] = None,
            **kwargs
    ):
        """
        Initialize the MoziChemHub.

        Parameters
        ----------
        name : str
            Name of the mcp server
        reference : Optional[Reference]
            Custom reference for the hub, default is None. It includes
            - content: str
            - config: dict
        reference_link : Optional[ReferenceLink]
            Custom reference link for the hub, default is None.
        **kwargs : dict
            Additional keyword arguments for hub configuration.
        """
        # NOTE: set
        self._name = name
        self._reference = reference
        self._reference_link = reference_link

        # NOTE: kwargs
        self.mcp_name = kwargs.get('mcp_name', None)

        # SECTION: initialize the registry
        RegistryMixin.__init__(self)

        # SECTION: initialize the ReferenceServices
        ReferenceServices.__init__(
            self,
            reference=reference,
            reference_link=reference_link
        )

        # SECTION: initialize the MoziServer
        self.MoziServer_ = MoziServer(name=name)

        # SECTION: initialize the ToolManager with references
        self.ToolManager_ = ToolManager(
            reference_thermodb=self.reference_thermodb,
            reference=self.reference,
            reference_link=self.reference_link
        )

    @property
    def name(self) -> str:
        """
        Get the name of the hub.
        """
        return self._name

    def _update(self):
        """
        Update the MoziChem mcp for serving. It builds the mcp server, adding tools, resources, prompts, and other configurations.
        """
        try:
            # SECTION: manage tools
            # collect the registered functions
            custom_functions: Dict[str, Callable[..., Any]] = self._methods

            # NOTE: build the tools
            # build the tools using the ToolManager
            tools = self.ToolManager_._build_tools(
                mcp_name=self.mcp_name,
                custom_functions=custom_functions
            )

            # NOTE: update the MCP server with tools
            if len(tools) > 0:
                self.MoziServer_._update_mcp_with_tools(
                    tools=tools
                )

            # SECTION: manage resources
            # collect the registered resources

            # SECTION: manage prompts
            # collect the registered prompts

        except Exception as e:
            raise RuntimeError(f"Failed to launch {self.name}: {e}") from e

    def _retrieve_mcp(self) -> FastMCP:
        """
        Retrieve the mcp server.
        """
        try:
            # NOTE: add tools/resources/prompts to the MCP server
            self._update()

            # NOTE: return the MCP server instance
            return self.MoziServer_.get_mcp()
        except Exception as e:
            raise RuntimeError(f"Failed to run {self.name}: {e}") from e

    def run(
        self,
        transport: Optional[Literal['stdio', 'streamable-http']] = None,
        **transport_kwargs
    ):
        """
        Run the MoziChem MCP server.

        Parameters
        ----------
        transport : Optional[Literal['stdio', 'streamable-http']]
            The transport method for the MCP server. Default is 'stdio'.
        **transport_kwargs : dict
            Additional keyword arguments for the transport configuration.
        """
        try:
            # NOTE: retrieve the mcp server
            mcp = self._retrieve_mcp()

            # NOTE: run the MCP server
            mcp.run(
                transport=transport or 'stdio',
                **transport_kwargs
            )
        except Exception as e:
            raise RuntimeError(f"Failed to run {self.name}: {e}") from e
