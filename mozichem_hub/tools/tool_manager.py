# import libs
import logging
from fastmcp.tools import Tool
from typing import (
    Dict,
    Callable,
    Optional,
    List,
    Any,
    Set
)
# local
from .tool_builder import ToolBuilder
from ..resources import FunctionDispatcher
from ..models import MoziTool
from ..models import (
    ReferencesThermoDB,
)
from ..errors import (
    FunctionRetrievalError,
    FunctionLoadingError,
    ToolBuildingError,
    ToolExecutionError,
    FUNCTION_RETRIEVAL_ERROR_MSG,
    FUNCTION_LOADING_ERROR_MSG,
    TOOL_BUILDING_ERROR_MSG,
    TOOL_EXECUTION_ERROR_MSG
)


class ToolManager(ToolBuilder):
    """
    ToolManager class for managing tools in the MoziChem Hub.
    """
    # NOTE: attributes
    _tools = []

    def __init__(
        self,
        references_thermodb: ReferencesThermoDB,
    ):
        """
        Initialize the ToolManager instance.
        """
        # SECTION: Initialize the Builder
        ToolBuilder().__init__()

        # SECTION: set references
        self._references_thermodb = references_thermodb

        # SECTION: init FunctionDispatcher
        self.FunctionDispatcher_ = FunctionDispatcher(
            references_thermodb=self._references_thermodb
        )

    def _retrieve_all_local_functions(self) -> Dict[str, List[MoziTool]]:
        """
        Retrieve all local functions.
        """
        try:
            # NOTE: Load function from FunctionDispatcher
            return self.FunctionDispatcher_.retrieve_all_mozi_tools()
        except Exception as e:
            raise FunctionRetrievalError(
                f"{FUNCTION_RETRIEVAL_ERROR_MSG} {e}") from e

    def _retrieve_local_functions(self, mcp_name: str) -> List[MoziTool]:
        """
        Retrieve local functions for the given mcp.

        Parameters
        ----------
        mcp_name : str
            The name of the mcp to retrieve functions for.
        """
        try:
            # NOTE: Load function from FunctionDispatcher
            return self.FunctionDispatcher_.retrieve_mozi_tools(mcp_name)
        except Exception as e:
            raise FunctionRetrievalError(
                f"{FUNCTION_RETRIEVAL_ERROR_MSG} {e}") from e

    def _get_info_local_functions(self, mcp_name: str) -> Dict[str, Any]:
        """
        Retrieve information about local functions for the given mcp.

        Parameters
        ----------
        mcp_name : str
            The name of the mcp to retrieve information for.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing information about the local functions.
        """
        try:
            # Retrieve local functions
            local_functions = self._retrieve_local_functions(mcp_name)

            # Return the information
            return {
                "mcp_name": mcp_name,
                "functions": local_functions
            }
        except Exception as e:
            raise FunctionLoadingError(
                f"{FUNCTION_LOADING_ERROR_MSG} {e}") from e

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
            # Ensure local_tools is always initialized
            local_tools: List[Tool] = []

            # Retrieve functions
            # ! get MoziTool
            _functions = self._retrieve_local_functions(mcp_name)

            # check if functions are empty
            if not _functions:
                logging.warning(
                    f"No local functions found for mcp '{mcp_name}'. "
                    "Please ensure the mcp is registered correctly."
                )
                return local_tools

            # NOTE: Build local tools
            # ! convert MoziTool to FastMCP Tool
            local_tools = self.build_tools_from_mozi_tools(_functions)

            # return the tools
            return local_tools
        except Exception as e:
            raise ToolBuildingError(f"{TOOL_BUILDING_ERROR_MSG} {e}") from e

    def _build_tools(
        self,
        mcp_name: Optional[str] = None,
        custom_functions: Optional[
            Dict[
                str, Dict[str, Callable[..., Any | str | Set]]
            ]
        ] = None
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
                    raise FunctionRetrievalError(
                        f"{FUNCTION_RETRIEVAL_ERROR_MSG} Function '{mcp_name}' not found in local resources.")

                # NOTE: Build local tools
                local_tools = self.build_tools_from_mozi_tools(_function)

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
            raise ToolBuildingError(f"{TOOL_BUILDING_ERROR_MSG} {e}") from e

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
            raise ToolExecutionError(f"{TOOL_EXECUTION_ERROR_MSG} {e}") from e
