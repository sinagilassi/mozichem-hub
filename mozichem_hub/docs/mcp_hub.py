# import libs
from typing import (
    Optional,
    Dict,
    Any,
    Union,
    List
)
# local
from .core import MoziChemMCP
from ..config import MCP_MODULES
from ..utils import MCPController


class MCPHub(MoziChemMCP):
    """
    MCPHub class for creating mcp from built-in functions.
    """

    def __init__(
        self,
        mcp: str,
        reference_content: Optional[
            Union[str, List[str]]
        ] = None,
        reference_config: Optional[
            Union[str, Dict[str, Dict[str, str]]]
        ] = None,
        reference_link: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the MCPHub.

        Parameters
        ----------
        mcp : str
            Name of the MCP to be used.
        reference_content : Optional[Union[str, List[str]]]
            Content of the reference, can be a string or a list of strings.
        reference_config : Optional[Union[str, Dict[str, Dict[str, str]]]]
            Configuration of the reference, can be a string or a dictionary.
        reference_link : Optional[str]
            Link to the reference, can be a string.
        **kwargs : dict
            Additional keyword arguments for the MCP.
        """
        # SECTION: select the name of the mcp available
        mcp = mcp.strip().lower()
        # set the name of the mcp
        self._name = mcp
        self._mcp_name = mcp

        # NOTE: set the reference and reference link
        self._reference_content = reference_content
        self._reference_config = reference_config
        self._reference_link = reference_link

        # NOTE: check if mcp is available
        # mcp names
        mcp_names = [
            module["name"] for module in MCP_MODULES
        ]

        # check if mcp is available
        if mcp not in mcp_names:
            raise ValueError(
                f"'{mcp}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(mcp_names)}"
            )

        # SECTION: mcp info
        self._mcp_info = MCPController.get_mcp_info(mcp)

    @property
    def name(self) -> str:
        """
        Get the name of the adapter.
        """
        return self._name

    @property
    def info(self) -> Optional[Dict[str, Any]]:
        """
        Get the information about the MCP.

        Returns
        -------
        dict
            Information about the MCP.
        """
        return self._mcp_info

    @property
    def description(self) -> str:
        """
        Get the description of the MCP.

        Returns
        -------
        str
            Description of the MCP.
        """
        source = self.info
        if source is None:
            raise ValueError(
                f"'{self._mcp_name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController.mcp_names())}"
            )

        # return the description from the source
        return source.get("description", "No description available.")

    @property
    def mcp_version(self) -> str:
        """
        Get the version of the MCP.

        Returns
        -------
        str
            Version of the MCP.
        """
        source = self.info
        if source is None:
            raise ValueError(
                f"'{self._mcp_name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController.mcp_names())}"
            )

        # return the version from the source
        return source.get("version", "unknown")

    def tools(self) -> Dict[str, Any]:
        """
        Get the tools available in the MCP.

        Returns
        -------
        dict
            Dictionary containing the tools available in the MCP.
        """
        source = self.info
        if source is None:
            raise ValueError(
                f"'{self._mcp_name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController.mcp_names())}"
            )

        # return the tools from the source
        return source.get("tools", {})

    def resources(self) -> Dict[str, Any]:
        """
        Get the resources available in the MCP.

        Returns
        -------
        dict
            Dictionary containing the resources available in the MCP.
        """
        source = self.info
        if source is None:
            raise ValueError(
                f"'{self._mcp_name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController.mcp_names())}"
            )

        # return the resources from the source
        return source.get("resources", {})

    def prompts(self) -> Dict[str, Any]:
        """
        Get the prompts available in the MCP.

        Returns
        -------
        dict
            Dictionary containing the prompts available in the MCP.
        """
        source = self.info
        if source is None:
            raise ValueError(
                f"'{self._mcp_name}' is not a valid MCP name. "
                f"Available MCPs: {', '.join(MCPController.mcp_names())}"
            )

        # return the prompts from the source
        return source.get("prompts", {})

    def _build_mozichem_mcp(self, **kwargs) -> MoziChemMCP:
        """
        Build the MoziChem MCP server.

        Returns
        -------
        MoziChemMCP
            The MoziChem MCP server instance.
        """
        # NOTE: build the MoziChem MCP server
        return MoziChemMCP(
            name=self.name,
            reference_content=self._reference_content,
            reference_config=self._reference_config,
            reference_link=self._reference_link,
            local_mcp=True,
            **kwargs
        )
