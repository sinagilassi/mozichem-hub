# import libs
from fastmcp import FastMCP
from typing import (
    Optional,
    Dict,
    List,
    Callable,
    Any,
    Literal,
    Set,
    Union
)
# local
from .registry import RegistryMixin
from .services import ReferenceServices
from .server import MoziServer
from ..tools import ToolManager
from ..references import (
    References,
    Reference,
    ReferenceLink,
    ComponentReferenceConfig
)


class MoziChemMCP(RegistryMixin, ReferenceServices):
    """
    This is the main entry point for the MoziChem MCP application.
    It initializes the MoziChemMCP instance and prepares it for serving.
    custom reference and link can be passed to the MoziChemMCP instance.
    """

    def __init__(
            self,
            name: str,
            description: Optional[str] = None,
            reference_content: Optional[
                Union[str, List[str]]
            ] = None,
            reference_config: Optional[
                Dict[str, Dict[str, str]]
            ] = None,
            component_reference_config: Optional[
                Union[
                    Dict[str, Dict[str, str]],
                    List[Dict[str, Dict[str, str]]]
                ]
            ] = None,
            reference_link: Optional[str] = None,
            local_mcp: Optional[bool] = False,
            **kwargs
    ):
        """
        Initialize the MoziChem MCP.

        Parameters
        ----------
        name : str
            Name of the mcp server.
        description : Optional[str]
            Description of the mcp server, default is None.
        reference_content : Optional[Union[str, List[str]]]
            Content of the reference, can be a string or a list of strings.
        reference_config : Optional[Dict[str, Dict[str, str]]]
            Configuration for the reference, default is None.
        component_reference_config : Optional[Union[ComponentReferenceConfig, List[ComponentReferenceConfig]]]
            Configuration for component references, default is None.
        reference_link : Optional[ReferenceLink]
            Custom reference link for the hub, default is None.
        local_mcp : Optional[bool]
            If True, the mcp will be configured to run locally with local tools.
        **kwargs : dict
            Additional keyword arguments for hub configuration.
        """
        # NOTE: set
        self._name = name
        self._description = description
        # ! reference
        self._reference_content = reference_content
        self._reference_config = reference_config
        self._component_reference_config = component_reference_config
        # ! reference link
        self._reference_link = reference_link

        # NOTE: set reference
        self._references = References(
            contents=reference_content,
            config=reference_config
        )

        # NOTE: set component reference config
        self._component_reference_config = ComponentReferenceConfig(
            properties=component_reference_config
        )

        # NOTE: set reference link
        self._reference_link = ReferenceLink(
            rule=reference_link
        )

        # NOTE: set the mcp name
        self.local_mcp = local_mcp

        # check
        if local_mcp is True:
            # if local_mcp is True, set the mcp name to the name of the hub
            self._mcp_name = name

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

        # SECTION: configure the MCP server
        # ! update the mcp server with local tools
        if local_mcp:
            # call
            self._update()

    @property
    def name(self) -> str:
        """
        Get the name of the mcp.
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        Get the description of the mcp.
        """
        return self._description

    def tools_info(self):
        '''
        Give information about the tools available in the MoziChem MCP.
        '''
        try:
            # SECTION: for local mcp
            if self.local_mcp:
                # retrieve all local functions
                return self.ToolManager_._get_info_local_functions(
                    mcp_name=self._mcp_name
                )
        except Exception as e:
            raise Exception(f"Failed to load tools: {e}") from e

    def _update(self):
        """
        Update the MoziChem mcp for serving. It builds the mcp server,
        adding tools, resources, prompts, and other configurations.
        """
        try:
            # SECTION: manage tools
            # collect the registered functions
            custom_functions: Dict[
                str, Dict[str, Callable[..., Any | str | Set]]
            ] = self._methods

            # NOTE: build the tools
            # build the tools using the ToolManager
            if self.local_mcp:
                # ! local mcp
                tools = self.ToolManager_._build_local_tools(
                    mcp_name=self.name,
                )
            else:
                # ! new mcp
                tools = self.ToolManager_._build_tools(
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
            if self.local_mcp is False:
                self._update()
            else:
                pass  # No need to update for local MCP

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
