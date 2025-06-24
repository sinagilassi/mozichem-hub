# import libs
from fastmcp.tools import Tool
from typing import (
    Dict,
    Callable,
    Optional,
    List
)
# local
from .builder import ToolBuilder
from ..manager import FunctionDispatcher, MoziTool
from ..references import (
    ReferenceThermoDB,
    Reference,
    ReferenceLink
)


class ToolManager(ToolBuilder):
    """
    ToolManager class for managing tools in the MoziChem Hub.
    """
    # NOTE: attributes
    _tools = []

    def __init__(
        self,
        reference_thermodb: ReferenceThermoDB,
        reference: Reference,
        reference_link: ReferenceLink
    ):
        """
        Initialize the ToolManager instance.
        """
        # SECTION: Initialize the Builder
        ToolBuilder().__init__()

        # SECTION: set references
        self._reference_thermodb = reference_thermodb
        self._reference = reference
        self._reference_link = reference_link

        # SECTION: init FunctionDispatcher
        self.FunctionDispatcher_ = FunctionDispatcher(
            reference_thermodb=self._reference_thermodb,
            reference=self._reference,
            reference_link=self._reference_link
        )

    def _retrieve_all_local_functions(self) -> Dict[str, List[MoziTool]]:
        """
        Retrieve all local functions.
        """
        try:
            # NOTE: Load function from FunctionDispatcher
            return self.FunctionDispatcher_.retrieve_all_mozi_tools()
        except Exception as e:
            raise Exception(f"Failed to load MoziChem functions: {e}") from e

    def _retrieve_local_functions(self, mcp_name) -> List[MoziTool]:
        """
        Retrieve local functions for the given mcp.
        """
        try:
            # NOTE: Load function from FunctionDispatcher
            return self.FunctionDispatcher_.retrieve_mozi_tools(mcp_name)
        except Exception as e:
            raise Exception(f"Failed to load MoziChem functions: {e}") from e

    def _build_local_tools(
        self,
        mcp_name: str,
    ) -> List[Tool]:
        """
        Build the tools for the MoziChem Hub.

        This method is responsible for building the tools that will be
        registered with the MoziChem Hub.

        Parameters
        ----------
        mcp_name : Optional[str], optional
            The name of the mcp to build tools for, by default None.

        Returns
        -------
        List[Tool]
            A list of Tool instances built from the MoziChem functions.
        """
        try:
            # SECTION: local resources
            local_tools = []  # Ensure local_tools is always initialized

            # Retrieve functions
            # ! get MoziTool
            _functions = self._retrieve_local_functions(mcp_name)

            # check if functions are empty
            if not _functions:
                raise ValueError(
                    f"No functions found for MCP '{mcp_name}' in local resources.")

            # NOTE: Build local tools
            # ! convert MoziTool to FastMCP Tool
            local_tools = self.build_mozi_tools(_functions)

            # return the tools
            return local_tools
        except Exception as e:
            raise ValueError(f"Failed to build tools: {e}") from e

    def _build_tools(
        self,
        mcp_name: Optional[str] = None,
        custom_functions: Optional[Dict[str, Callable]] = None
    ) -> List[Tool]:
        """
        Build the tools for the MoziChem Hub.

        This method is responsible for building the tools that will be
        registered with the MoziChem Hub.

        Parameters
        ----------
        custom_functions : Optional[Dict[str, Callable]], optional
            Custom functions to be included in the tools, by default None

        Returns
        -------
        List[Tool]
            A list of Tool instances built from the MoziChem functions.
        """
        try:
            # SECTION: local resources
            local_tools = []  # Ensure local_tools is always initialized

            if mcp_name is not None:
                # Retrieve functions
                _functions = self._retrieve_all_local_functions()

                # selected function
                _function = _functions.get(mcp_name, None)

                if _function is None:
                    raise ValueError(
                        f"Function '{mcp_name}' not found in local resources.")

                # NOTE: Build local tools
                local_tools = self.build_mozi_tools(_function)

            # SECTION: Build external tools
            external_tools = []  # Ensure external_tools is always initialized

            if custom_functions:
                # NOTE: This is a placeholder for building external tools
                external_tools = self.build_tools_from_function(
                    custom_functions
                )

            # NOTE: Combine local and external tools
            self._tools = local_tools + external_tools

            # return the tools
            return self._tools
        except Exception as e:
            raise ValueError(f"Failed to build tools: {e}") from e

    def launch(self):
        """
        Launch the ToolManager.

        This method is called to start the ToolManager and prepare it for serving.
        """
        try:
            # SECTION: Build tools
            self._build_tools()
            return self._tools
        except Exception as e:
            raise RuntimeError(f"Failed to launch ToolManager: {e}") from e
